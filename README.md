# iPixel-ESP32

A C++ BLE library for controlling iPixel LED matrix displays from an ESP32.
Add it to any PlatformIO project via `lib_deps` and control any iPixel display directly over Bluetooth — no HTTP server, no WiFi stack.

---

## Installation

Add the library to your `platformio.ini` using the GitHub repository and branch:

```ini
lib_deps =
  https://github.com/ToBiDi0410/iPixel-ESP32.git#develop
```

PlatformIO will automatically download the library and its bundled dependencies (`lodepng`). You also need to declare the external library deps the library relies on:

```ini
lib_deps =
  https://github.com/ToBiDi0410/iPixel-ESP32.git#develop
  h2zero/NimBLE-Arduino@^2.1.0
  erriez/ErriezCRC32@^1.0.1
  adafruit/Adafruit GFX Library@^1.12.3
```

### Complete `platformio.ini` example

```ini
[env:my_app]
platform = espressif32@6.12.0
framework = arduino
board = esp32-s3-devkitc-1    ; adjust to your board

board_build.flash_mode = qio
board_build.psram_type = qio  ; remove this line if your board has no PSRAM

build_flags =
  -std=c++14

lib_deps =
  https://github.com/ToBiDi0410/iPixel-ESP32.git#develop
  h2zero/NimBLE-Arduino@^2.1.0
  erriez/ErriezCRC32@^1.0.1
  adafruit/Adafruit GFX Library@^1.12.3
```

> **Find your iPixel MAC address** using a BLE scanner app such as [nRF Connect](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-mobile).

---

## Quick Start

```cpp
#include "iPixelBleClient.h"

// Replace with your iPixel device MAC address
iPixelBLE::Client matrix("AA:BB:CC:DD:EE:FF");

void setup() {
  Serial.begin(115200);

  // Initialize the BLE stack once. Set your device's advertised BLE name.
  iPixelBLE::Client::init("MyApp");

  // Reconnect automatically when the device drops (default: true)
  matrix.setAutoReconnect(true);

  // Start non-blocking connection attempt
  matrix.connect();
}

void loop() {
  // REQUIRED: call every loop iteration.
  // Handles reconnection and flushes the outbound command queue.
  matrix.loop();

  if (matrix.isConnected()) {
    matrix.setBrightness(80);
    matrix.sendText("Hello!", 0, 1, 50, 255, 255, 255, 0, 16, 16);
  }

  delay(1);
}
```

See [src/examples/ble_only_main.cpp](src/examples/ble_only_main.cpp) for a complete working example.

---

## API Reference

### Static initialization

```cpp
// Call once before connecting any Client. Sets the BLE device name.
iPixelBLE::Client::init("MyApp");
```

This must be called exactly once per firmware. Calling it multiple times is safe (it is a no-op after the first call).

---

### `Client` — constructor

```cpp
iPixelBLE::Client matrix("AA:BB:CC:DD:EE:FF");   // MAC address as string
iPixelBLE::Client matrix(NimBLEAddress addr);     // NimBLE address object
```

---

### Connection

| Method | Description |
|---|---|
| `connect()` | Start async connection attempt |
| `disconnect()` | Disconnect immediately |
| `setAutoReconnect(bool)` | Auto-reconnect on drop. Default: `true` |
| `isConnected()` | Returns `bool` |
| `mac()` | Returns MAC address as `String` |
| `queuedCommands()` | Returns count of pending commands in the queue |
| `loop()` | **Must be called every `loop()` iteration** |

---

### Display commands

All commands are **non-blocking** — they are queued and transmitted asynchronously. Call `matrix.loop()` every iteration to drain the queue.

---

#### `setBrightness(int brightness)`
```cpp
matrix.setBrightness(80);  // 0–100
```

---

#### `setSpeed(int speed)`
Animation and scroll speed.
```cpp
matrix.setSpeed(50);  // 0–100
```

---

#### `clear()`
Clear all content from the display.
```cpp
matrix.clear();
```

---

#### `setLED(bool on)`
Turn the LED panel on or off.
```cpp
matrix.setLED(true);
```

---

#### `setOrientation(int orientation)`
```cpp
matrix.setOrientation(0);  // 0 = normal, 1 = 180°
```

---

#### `setTime(int hour, int minute, int second)`
Sync the device clock.
```cpp
matrix.setTime(14, 30, 0);
```

---

#### `setFunMode(bool value)`
Toggle built-in fun mode animations.
```cpp
matrix.setFunMode(true);
```

---

#### `deleteScreen(int screen)`
Delete a saved screen from the device's storage.
```cpp
matrix.deleteScreen(1);  // slot 1-n
```

---

#### `setPixel(int x, int y, uint8_t r, uint8_t g, uint8_t b)`
Set a single pixel. Origin `(0, 0)` is top-left.
```cpp
matrix.setPixel(0, 0, 255, 0, 0);  // red pixel at [0,0]
```

---

#### `sendText(text, animation, saveSlot, speed, r, g, b, rainbow, matrixHeight, fontHeight)`

Display scrolling or static text.

```cpp
matrix.sendText(
  "Hello",  // text
  0,        // animation style (0 = scroll left)
  1,        // save slot on device (1–n)
  50,       // scroll speed (0–100)
  255,      // red
  255,      // green
  255,      // blue
  0,        // rainbow mode: 0 = off, 1 = on
  16,       // matrix height in pixels (usually 16)
  16        // font height (see table below)
);
```

**Font height values:**

| `fontHeight` | Font |
|---|---|
| `7` | Cusong 7px Compact — fits small text on 16px tall displays |
| `10` | Pixeloid Sans 10px |
| `16` | Pixeloid Sans 16px (default, fills the full height) |

---

#### `sendPNG(const std::vector<uint8_t>& pngData)`

Send a PNG image to the display.

```cpp
#include <vector>

// Example: image embedded as a C array
extern const uint8_t my_image[] = { /* raw PNG bytes */ };
const size_t my_image_size = sizeof(my_image);

matrix.sendPNG(std::vector<uint8_t>(my_image, my_image + my_image_size));
```

---

#### `sendGIF(const std::vector<uint8_t>& gifData)`

Send a GIF animation. Same usage as `sendPNG`.

---

#### `setClockMode(style, dayOfWeek, year, month, day, showDate, format24)`

Display a clock face.

```cpp
matrix.setClockMode(
  0,     // clock face style (0–n)
  1,     // day of week: 0 = Sunday … 6 = Saturday
  2026,  // year
  3,     // month (1–12)
  22,    // day (1–31)
  true,  // show date below time
  true   // 24h format; false = 12h AM/PM
);
```

---

#### `setRhythmLevelMode(int style, const int levels[11])`

Display an equalizer-style bar animation with 11 frequency bands.

```cpp
int levels[11] = {10, 20, 40, 60, 80, 100, 80, 60, 40, 20, 10};
matrix.setRhythmLevelMode(0, levels);  // style 0–n
```

---

#### `setRhythmAnimationMode(int style, int frameNumber)`

Step through a rhythm animation manually.

```cpp
matrix.setRhythmAnimationMode(0, 3);  // style 0–n, frame index
```

---

#### `queueRaw(const std::vector<uint8_t>& command)`

Queue a pre-built raw BLE command frame. For advanced use when protocol-level control is needed.

```cpp
matrix.queueRaw({0x01, 0x02, 0x03, /* ... */});
```

See [iPixel_PROTOCOL.md](iPixel_PROTOCOL.md) for frame structure details.

---

## Memory Footprint

Measured on ESP32-S3 with a clean library-only build:

| | RAM | Flash |
|---|---|---|
| Used | 19 KB (5.8%) | 404 KB (19.3%) |

---

## Credits

Protocol reverse-engineered from community work:

- https://github.com/lucagoc/iPixel-CLI
- https://github.com/DonKracho/ESPHome-external-component-for-iPixel-ble-devices
