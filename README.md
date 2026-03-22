# iPixel-ESP32

ESP32 firmware that exposes a REST API to control iPixel BLE LED matrices.

The project combines:

- BLE command generation and queued transmission to iPixel displays
- On-device HTTP API (ESPAsyncWebServer)
- Persistent pairing registries (LittleFS JSON) for Bluetooth devices and WiFi credentials
- Multi-font text rendering pipeline (including compact 7px and 10px/16px variants)

## Current Status

- Development branch is active and API is still evolving.
- `esp32-s3-devkitc-1` is the primary target (`platformio.ini` default environment).
- Other ESP32 environments are configured but should be treated as secondary.

## Runtime Architecture

Execution is task-driven:

- `setup()` runs all setup tasks: filesystem mount, WiFi/BLE/webserver initialization.
- `loop()` runs scheduled loop tasks with priorities and intervals.

Core task groups:

- WiFi: credential loading, STA connect attempts, AP fallback (`iPixel-ESP32` / `123456789`).
- Bluetooth: pairing loading, client connect loop, command queue flushing.
- Webserver: endpoint registry bootstrap and route attachment.

The API endpoint system is static-registration based: each endpoint declares an `Endpoint` object, and the webserver setup iterates the registry and attaches handlers.

## API Model

The API is ID-based, not MAC-in-path.

1. Add/list/update/remove Bluetooth pairings.
2. Use the pairing `id` as `device` query parameter on control endpoints.
3. Commands are encoded into BLE frames and pushed to a per-device queue.

Main endpoint groups:

- Bluetooth pairings: `/bluetooth/pairings/*`
- WiFi pairings and scan: `/wifi/pairings/*`, `/wifi/scan/*`
- Raw control: `/control/raw/*`

Raw control endpoints include:

- `clear`, `deleteScreen`, `setBrightness`, `setSpeed`, `setTime`, `setFunMode`, `setLED`, `setOrientation`, `setPixel`
- `setClockMode`, `setRhythmAnimationMode`, `setRhythmLevelMode`
- `sendText`, `sendPNG`, `sendGIF`

Notes:

- All control requests require `device=<pairing_id>`.
- Binary image/text payloads are passed as encoded query values and transformed into protocol frames server-side.
- Parameter validation throws exceptions that are mapped to HTTP error codes by the webserver wrapper.

## Library-First BLE API (Step 1)

A new additive facade is available for app-style usage without depending on webserver or WiFi modules:

- `src/iPixelBleClient.h`
- `src/iPixelBleClient.cpp`

This is intentionally non-breaking: existing REST endpoints and firmware flow remain unchanged.

Minimal usage:

```cpp
#include "iPixelBleClient.h"

iPixelBLE::Client matrix("19:2D:FE:55:52:AA");

void setup() {
	Serial.begin(115200);
	iPixelBLE::Client::init("MyController");

	matrix.connect();
	matrix.setBrightness(80);
	matrix.sendText("Hello", 0, 1, 50, 255, 255, 255, 0, 16, 16);
}

void loop() {
	matrix.loop();
}
```

Why this helps the cleanup plan:

- Third-party apps can now consume a direct BLE API layer first.
- We can remove webserver/WiFi/demo modules later, after parity is validated.

## Repository Map

- `src/main.cpp`: firmware entrypoint and task runner.
- `src/Tasking.h`: lightweight scheduler and task registry.
- `src/webserver/`: HTTP server, endpoint registration, request param helpers.
- `src/bluetooth/`: Bluetooth pairing model, persistence, connect/queue loops, pairing endpoints.
- `src/wifi/`: WiFi pairing model, persistence, scan endpoints, connect strategy.
- `src/control/`: raw device control endpoints.
- `src/iPixelCommands.*`: protocol frame builders and input range checks.
- `src/Helpers.*`: CRC32, endian/bit transforms, hex parsing, PNG encoding helpers.
- `include/Font*.h`: bundled font data used by text command encoding.
- `scripts/`: font conversion and maintenance tooling.
- `test/`: native test scaffolding.

## Build and Flash

Prerequisites:

- PlatformIO CLI or VS Code PlatformIO extension

Common commands:

```bash
# Build default target (esp32s3dev)
pio run

# Upload firmware
pio run -t upload

# Serial monitor
pio device monitor -b 115200
```

Available environments in `platformio.ini`:

- `esp32s3dev` (default)
- `esp32dev`
- `esp32c3dev`

## Key Documentation

- `README_API.md`: current API-oriented usage and examples.
- `iPixel_PROTOCOL.md`: protocol notes and frame structure.
- `GFX.md`: early GFX ideas and payload shape.
- `SENDTEXT_REFACTOR_PLAN.md`: sendText architecture and migration details.
- `IMPLEMENTATION_INDEX.md`: index for font + sendText workstream.

## Credits

Protocol reverse-engineering work builds on community research, especially:

- https://github.com/lucagoc/iPixel-CLI
- https://github.com/DonKracho/ESPHome-external-component-for-iPixel-ble-devices
