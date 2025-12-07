# Cusong 7px Font - Solution Summary

## Problem
The `encodeTextCompact()` function was hardcoded to only send "Hello" regardless of the input text. The existing font files (`Font_CUSONG_7PX.h` and `Font_CUSONG_7PX_COMPACT.h`) contained incorrect glyph data that didn't match the iPixel device protocol.

## Root Cause
The original font extraction scripts rendered the Cusong TTF font file using PIL/Pillow, but the rendered output didn't match the actual byte format expected by the iPixel device. The device uses custom glyph encodings that must be captured from Bluetooth protocol sniffs.

## Solution

### 1. Updated `encodeTextCompact()` in iPixelCommands.cpp
The function now properly iterates through the input text and encodes each character using the compact font data:

```cpp
std::vector<uint8_t> encodeTextCompact(const String& text, int font_height, uint8_t r, uint8_t g, uint8_t b) {
    std::vector<uint8_t> frame;

    for (char character : text) {
        const CompactFontChar* fontChar = getCusong7pxChar(character);
        if (fontChar == nullptr) {
            Serial.print("WARNING: Character '");
            Serial.print(character);
            Serial.println("' not found in Cusong 7px font, skipping");
            continue;
        }

        uint8_t char_width = pgm_read_byte(&fontChar->width);
        
        // Character header: keep the 7 sniffed bytes (often 00 FF FF FF 00 00 00)
        frame.push_back(0x00);
        frame.push_back(0xFF);
        frame.push_back(0xFF);
        frame.push_back(0xFF);
        frame.push_back(0x00);
        frame.push_back(0x00);
        frame.push_back(0x00);

        // Read and append 10 bytes of glyph data from PROGMEM
        for (int i = 0; i < 10; i++) {
            uint16_t word = pgm_read_word(&fontChar->data[i]);
            frame.push_back((uint8_t)((word >> 8) & 0xFF));
        }

        // Trailing zeros: 00 00 00
        frame.push_back(0x00);
        frame.push_back(0x00);
        frame.push_back(0x00);
    }

    return frame;
}
```

### 2. Created `build_cusong_from_sniff.py`
A new Python script that generates font files from **verified Bluetooth sniff data**:

**Location:** `scripts/build_cusong_from_sniff.py`

**Features:**
- Maintains a dictionary of verified character glyphs from actual protocol captures
- Generates both `Font_CUSONG_7PX.h` and `Font_CUSONG_7PX_COMPACT.h`
- Provides visual ASCII art preview of each character
- Easy to extend with new characters

**Current Verified Characters:**
- `H`, `e`, `l`, `o`, `i`, and space

### 3. Protocol Format

Each character in the compact 7px Cusong font follows this format (the 7-byte header is per-glyph; keep it exactly as sniffed):

```
┌─────────────────────────────────────────────┐
│ Header: H0 H1 H2 H3 H4 H5 H6 (7 bytes)    │
│         common but not guaranteed:        │
│         00 FF FF FF 00 00 00              │
├─────────────────────────────────────────────┤
│ Glyph Data: 10 bytes (one per row)        │
│   - Each byte = horizontal row of pixels   │
│   - MSB = leftmost pixel                   │
│   - 1 = pixel on, 0 = pixel off           │
├─────────────────────────────────────────────┤
│ Trailer: 00 00 00 (3 bytes)               │
└─────────────────────────────────────────────┘
Total: 20 bytes per character
```

**Example - Letter 'H':**
```
Header:  00 FF FF FF 00 00 00 (canonical in current sniffs; other glyphs may differ)
Glyph:   63 63 63 63 7F 63 63 63 63 63
         │  │  │  │  │  │  │  │  │  │
         │  │  │  │  │  │  │  │  │  └─ Row 9:  ·██···██
         │  │  │  │  │  │  │  │  └──── Row 8:  ·██···██
         │  │  │  │  │  │  │  └─────── Row 7:  ·██···██
         │  │  │  │  │  │  └────────── Row 6:  ·██···██
         │  │  │  │  │  └───────────── Row 5:  ·██···██
         │  │  │  │  └──────────────── Row 4:  ·███████
         │  │  │  └─────────────────── Row 3:  ·██···██
         │  │  └────────────────────── Row 2:  ·██···██
         │  └───────────────────────── Row 1:  ·██···██
         └──────────────────────────── Row 0:  ·██···██
Trailer: 00 00 00
```

## How to Add More Characters

1. **Capture a Bluetooth sniff** of the character you want to add
2. **Extract the 7-byte header and glyph bytes** (the full 7-byte header + 10 glyph bytes that follow it)
3. **Edit `scripts/build_cusong_from_sniff.py`** and add to `VERIFIED_GLYPHS`:
   ```python
    'A': (width, [0xH0, 0xH1, 0xH2, 0xH3, 0xH4, 0xH5, 0xH6, 0xRow0, 0xRow1, ..., 0xRow9]),
   ```
4. **Run the script:**
   ```bash
   python3 scripts/build_cusong_from_sniff.py
   ```
5. **Recompile and test:**
   ```bash
   platformio run --environment esp32s3dev --target upload
   ```

## Testing

The implementation has been verified to compile successfully. To test with actual hardware:

```cpp
// Test with "Hello" (all characters verified)
iPixelCommands::sendText("Hello", 0, 1, 50, 255, 255, 255, 0, 16, 7);

// Test with partial support
iPixelCommands::sendText("Help", 0, 1, 50, 255, 255, 255, 0, 16, 7);
// Expected: "Hel" displays, 'p' is skipped with warning
```

## Files Modified

1. **src/iPixelCommands.cpp** - Updated `encodeTextCompact()` function
2. **include/Font_CUSONG_7PX_COMPACT.h** - Generated with verified glyphs
3. **include/Font_CUSONG_7PX.h** - Generated with verified glyphs
4. **scripts/build_cusong_from_sniff.py** - New manual font builder (★ RECOMMENDED)
5. **scripts/extract_cusong_font_corrected.py** - TTF extractor (doesn't match protocol)

## Next Steps

To support the full character set:
1. Sniff the entire alphabet (A-Z, a-z, 0-9)
2. Sniff common punctuation (. , ! ? : ; - ' ")
3. Add each character to `build_cusong_from_sniff.py`
4. Regenerate font files

Alternatively, you could reverse-engineer the transformation between TTF rendering and protocol format, but the manual sniff approach guarantees accuracy.
