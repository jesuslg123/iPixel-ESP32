# iPixel BLE Protocol

This document describes the BLE protocol for controlling iPixel LED screens, based on the analysis of the `DonKracho/ESPHome-external-component-for-iPixel-ble-devices` repository.

## 1. General Command Structure

Most commands follow a structure starting with a length/type indicator.
Multi-byte values are often Little Endian.

## 2. Set Mode / Basic Commands

### Set Clock Mode
Sets the display to show the clock.
**Bytes:** `0x0B 0x00 0x06 0x01 <Style> <Format24> <ShowDate> <Year> <Month> <Day> <DayOfWeek>`
*   `Style`: 1-8
*   `Format24`: 0x01 for 24h, 0x00 for 12h
*   `ShowDate`: 0x01 to show, 0x00 to hide
*   `Year`: 0-99
*   `Month`: 1-12
*   `Day`: 1-31
*   `DayOfWeek`: 1-7

### Set Time
**Bytes:** `0x08 0x00 0x01 0x80 <Hour> <Minute> <Second> 0x00`

### Clear Screen
**Bytes:** `0x04 0x00 0x03 0x80`

### Set Brightness
**Bytes:** `0x05 0x00 0x04 0x80 <Brightness>`
*   `Brightness`: 0-100

### Turn LED On/Off
*   **On:** `0x05 0x00 0x07 0x01 0x01`
*   **Off:** `0x05 0x00 0x07 0x01 0x00`

## 3. Set Color (Fill Screen)

There is no dedicated single-byte command to fill the screen. To fill the screen with a color, you must either:
1.  **Set every pixel individually** (Slow)
    *   **Command:** `0x0A 0x00 0x05 0x01 0x00 <R> <G> <B> <X> <Y>`
2.  **Send a solid color image** (Recommended)
    *   Construct a PNG or GIF image of the screen size filled with the desired color and send it using the Image Upload protocol.

## 4. Send Text

Sending text is complex and involves a Header, CRC, Save Slot, and Payload.

**Structure:** `[Header] [CRC32] [SaveSlot] [Payload]`

### Header (9 Bytes)
Calculated based on text length and font.
*   `HEADER_1_MG = 0x1D`
*   `HEADER_3_MG = 0x0E`
*   `header_gap = CHAR_HEADER + CHAR_BYTES` (Depends on font)
*   `val1 = HEADER_1_MG + (TextLength * header_gap)`
*   `val3 = HEADER_3_MG + (TextLength * header_gap)`

**Bytes:**
`<val1_LB> <val1_HB> 0x00 0x01 0x00 <val3_LB> <val3_HB> 0x00 0x00`
*(LB = Low Byte, HB = High Byte)*

### CRC32 (4 Bytes)
CRC32 checksum of the **Payload**.
**Bytes:** `<CRC_LB> <CRC_MB1> <CRC_MB2> <CRC_HB>` (Little Endian)

### Save Slot (2 Bytes)
**Bytes:** `<Slot_LB> <Slot_HB>`
*   `Slot`: 1-10

### Payload (Variable Length)
**Structure:**
1.  `<TextLength>` (1 Byte)
2.  `0x00 0x01 0x01` (Fixed Prefix)
3.  `<Animation>` (1 Byte, 0-6)
4.  `<Speed>` (1 Byte, 0-100)
5.  `<RainbowMode>` (1 Byte, 0-9)
6.  `0xFF 0xFF 0xFF 0x00 0x00 0x00 0x00` (Fixed Separator)
7.  `<EncodedChars>` (Variable)

**EncodedChars:**
Characters are encoded into bitmaps based on the selected font (8x16, 16x16, etc.), then bits are reversed and bytes are swapped/inverted.

## 5. Checksum Algorithm

The protocol uses **CRC32**.
*   **Polynomial:** Standard CRC32 (0x04C11DB7 / 0xEDB88320)
*   **Initial Value:** `0xFFFFFFFF` (Standard)
*   **Final XOR:** `0xFFFFFFFF` (Standard)
*   **Byte Order:** The result is sent in **Little Endian** order (Reverse of standard Big Endian output).

**Example Implementation (C++):**
```cpp
uint32_t crc = crc32Update(data.data(), data.size(), 0xFFFFFFFF);
crc = crc32Final(crc); // XOR with 0xFFFFFFFF
// Send: (crc >> 0) & 0xFF, (crc >> 8) & 0xFF, ...
```

## 6. Image Upload (PNG/GIF)

**Note: This is the recommended method for full-screen updates.**
Sending pixels individually (`0x0A`) is too slow for animations. To update the whole screen, encode the frame as a PNG and send it.

**Implementation Note:**
To implement this on ESP32, you need:
1.  **`lodepng` library**: To encode raw RGB buffers into PNG format in memory.
2.  **`ErriezCRC32` library**: To calculate the required checksum.

To send an image (like for filling the screen):

**Structure:**
`0xFF 0xFF 0x02 0x00 0x00 <Size_LB> <Size_HB> <CRC_LB>...<CRC_HB> 0x00 0x65 <ImageData>`

*   `0xFF 0xFF`: Placeholder (sometimes replaced by frame size)
*   `0x02 0x00 0x00`: Prefix for PNG (`0x03` for GIF)
*   `Size`: Image data size (Little Endian)
*   `CRC`: CRC32 of Image Data
*   `0x00 0x65`: Mid separator (`0x02 0x01` for GIF)
*   `ImageData`: Raw PNG/GIF bytes
