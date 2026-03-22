# iPixel-ESP32

A pure BLE library for controlling iPixel LED matrix displays. Integrate this C++ library into your own ESP32 or third-party application to communicate with iPixel devices via Bluetooth.

## What This Is

- **BLE Command Library:** Core BLE command generation and transmission to iPixel displays
- **Multi-Font Support:** Pre-generated font data (Cusong 7px, PixeloidSans 10px/16px)
- **Minimal Dependencies:** Only NimBLE-Arduino and ErriezCRC32—no HTTP server or WiFi overhead
- **Memory Efficient:** Library-only builds consume ~30% flash and ~9% RAM vs full firmware

## Quick Start

### 1. Include the Client API

```cpp
#include "iPixelBleClient.h"

// Create a client instance
iPixelBleClient::Client client;

// In setup()
client.connect(BLEAddress("AA:BB:CC:DD:EE:FF"));

// In loop()
client.loop();

// Send commands
client.setBrightness(200);
client.sendText("Hello", Font::CUSONG_7PX_COMPACT);
```

### 2. PlatformIO Configuration

Add to `platformio.ini`:

```ini
[env:my_app]
platform = espressif32@6.12.0
framework = arduino
board = esp32-s3-devkitc-1

lib_deps =
  h2zero/NimBLE-Arduino@^2.1.0
  erriez/ErriezCRC32@^1.0.1

; Adjust for your board
board_build.flash_mode = qio
board_build.psram_type = qio
```

Copy `src/` (excluding `examples/`) into your project.

## Architecture

**Core BLE Stack:**
- `iPixelDevice.h/cpp` — Low-level BLE connection and command queuing
- `iPixelCommands.h` — Command frame generation and encoding
- `iPixelBleClient.h/cpp` — High-level C++ API facade for third-party integration

**Supporting Files:**
- `Helpers.h/cpp` — CRC32 and utility functions
- `Tasking.h` — Optional task scheduler (used in example firmware)
- `include/Font_*.h` — Pre-rendered font data

## Device APIs

### `iPixelBleClient::Client`

Connect to and control a single iPixel device:

```cpp
class Client {
  bool connect(BLEAddress deviceAddr);
  void disconnect();
  void loop();  // Call frequently in your main loop
  
  void setBrightness(int brightness);
  void setSpeed(int speed);
  void sendText(String text, Font font);
  void sendPNG(const uint8_t* pngData, size_t length);
  void sendGIF(const uint8_t* gifData, size_t length);
  void setPixel(int x, int y, uint8_t r, uint8_t g, uint8_t b);
  void clear();
  // ... and more control methods
};
```

### Low-Level APIs

For advanced use, access `iPixelDevice` directly:

```cpp
iPixelDevice device(BLEAddress("AA:BB:CC:DD:EE:FF"));
device.connect();
device.onConnected([](iPixelDevice* d) { /* handle */ });
device.enqueueCommand(CommandType::SET_BRIGHTNESS, 200);
```

## Build Targets

### Default Firmware

```bash
platformio run -e esp32s3dev    # Full firmware with task runner
```

### Library-Only Example

```bash
platformio run -e esp32s3_ble_only_example  # Minimal BLE client example
```

### Hardware Variants

- `esp32dev`, `esp32c3dev` — Standard ESP32 variants
- `esp32s3dev` — ESP32-S3 with PSRAM (default)
- `esp32s3supermini` — ESP32-S3 mini without PSRAM
## Repository Structure

- `src/Helpers.h/cpp` — Utility functions (CRC32, bit transforms, parsing)
- `src/Tasking.h` — Optional task scheduler for background execution
- `src/iPixelDevice.h/cpp` — Low-level BLE connection management
- `src/iPixelCommands.h` — Command frame builders and encoding
- `src/iPixelBleClient.h/cpp` — High-level C++ API facade
- `src/bluetooth/` — BLE connection state and loop management
- `src/examples/ble_only_main.cpp` — Minimal example firmware
- `include/Font_*.h` — Pre-rendered font data for text rendering
- `scripts/` — Font conversion and asset generation tools
- `test/` — Native unit test scaffolding

## Memory Usage

Library-only builds are significantly more memory-efficient:

| Configuration | RAM | Flash |
|---|---|---|
| BLE-only library | 9.1% (29.8 KB) | 30.2% (633.6 KB) |
| Full example | 15.5% (50.8 KB) | 55.8% (1.2 MB) |

The library-only approach saves ~53% flash and ~40% RAM for embedded deployments.

## Building

### Prerequisites

- PlatformIO CLI or VS Code extension

### Default Build

```bash
platformio run -e esp32s3dev
```

### Library-Only Example

```bash
platformio run -e esp32s3_ble_only_example
```

### Upload

```bash
platformio run -e esp32s3dev -t upload
platformio device monitor -b 115200
```

## Available Hardware Targets

- `esp32dev` — Generic ESP32
- `esp32c3dev` — ESP32-C3
- `esp32s3dev` — ESP32-S3 with PSRAM (default, 4MB flash)
- `esp32s3supermini` — ESP32-S3 mini without PSRAM
- `esp32s3_ble_only_example` — BLE library demonstration

## Protocol & Documentation

- [iPixel_PROTOCOL.md](iPixel_PROTOCOL.md) — BLE frame structure and command format
- [FONT_CONVERSION_SUMMARY.md](FONT_CONVERSION_SUMMARY.md) — Font generation and bundling
- [IMPLEMENTATION_INDEX.md](IMPLEMENTATION_INDEX.md) — Implementation notes
- [GFX.md](GFX.md) — Graphics pipeline details

## Community & Credits

Protocol reverse-engineering builds on community research:

- https://github.com/lucagoc/iPixel-CLI
- https://github.com/DonKracho/ESPHome-external-component-for-iPixel-ble-devices
