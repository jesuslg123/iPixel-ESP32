# Screen Size Support Changes - iPixel-ESP32 Develop Branch

**Comparison Base:** `main` branch vs `develop` branch (19 commits difference)

## Executive Summary

The develop branch introduces **comprehensive support for multiple screen sizes and variable font heights** through a refactored architecture. The original codebase assumed fixed 16×16 screens with a single font (VCR_OSD_MONO_16PX). The new implementation supports LED matrices ranging from 16×16 to 32×448 pixels with 3 font options optimized for different screen dimensions.

---

## 1. FONT SYSTEM OVERHAUL

### New Multi-Font Architecture

**3 Fonts Now Supported:**

| Font | Size | Purpose | Supported Screen Sizes |
|------|------|---------|----------------------|
| **Cusong 7px (Compact)** | 7×10 bytes | Chinese characters, small/narrow screens | 16×32, 20×64, 32×96, 16×144, 16×192 |
| **Pixeloid Sans 10px** | 10×10 bytes | Medium text, general purpose | All except small 16×16 |
| **Pixeloid Sans 16px** | 16×16 bytes | Large text, big displays | Large screens 32×192+, 32×256+ |

### Font Selection Logic (in `iPixelCommands.cpp`)

```cpp
SelectedFont selectFont(int font_height) {
    switch (font_height) {
        case 7:   return { nullptr, 7, true };     // Cusong 7px Compact
        case 10:  return { &FONT_PIXELOID_SANS_10PX, 10, false };
        case 16:  return { &FONT_PIXELOID_SANS_16PX, 16, false };
        default:  throw std::invalid_argument("Unsupported font height");
    }
}
```

### New Font Files Added

- [Font_CUSONG_7PX_COMPACT.h](include/Font_CUSONG_7PX_COMPACT.h) - 131 lines
  - Compact binary representation of Cusong font
  - Uses `CompactFontChar` struct with `uint16_t[20]` glyph data
  - Extracted via `extract_cusong_font_corrected.py`

- [Font_PIXELOID_SANS_10PX.h](include/Font_PIXELOID_SANS_10PX.h) - 1,343 lines
  - Standard `FontChar` struct: `int width` + `std::vector<uint16_t> data[16]`
  - Generated from TrueType font via `font_converter.py`

- [Font_PIXELOID_SANS_16PX.h](include/Font_PIXELOID_SANS_16PX.h) - 1,877 lines
  - Same structure as 10px version, higher resolution

### Changed Font Registration

**[include/Font.h](include/Font.h)**
- Added includes for new Pixeloid fonts
- Kept original `FONT_VCR_OSD_MONO_16PX` for backward compatibility
- Disabled old Cusong 7px (commented out)

---

## 2. SENDTEXT COMMAND REFACTORING

### API Changes

**[src/iPixelDevice.h](src/iPixelDevice.h) - Function Signature**

```cpp
// OLD: Fixed font size (16px assumed)
void sendText(const String& text, int animation, int save_slot, int speed, 
              uint8_t colorR, uint8_t colorG, uint8_t colorB, int rainbow_mode, int matrix_height);

// NEW: Variable font height support
void sendText(const String& text, int animation, int save_slot, int speed, 
              uint8_t colorR, uint8_t colorG, uint8_t colorB, int rainbow_mode, 
              int matrix_height, int font_height = 16);
```

**New Parameter:** `font_height` (default 16 for backward compatibility)
- Determines which font to use (7, 10, or 16)
- Validated to fit within `matrix_height`

### Text Encoding Refactored

**[src/iPixelCommands.cpp](src/iPixelCommands.cpp) - Dual Encoding Paths**

#### 1. **Compact Font Path** (`encodeTextCompact`)
```cpp
// For Cusong 7px font
for (char character : text) {
    const CompactFontChar* fontChar = getCusong7pxChar(character);
    uint8_t char_width = pgm_read_byte(&fontChar->width);
    // Extract 20 bytes of glyph data from PROGMEM
    for (int i = 0; i < 20; i++) {
        uint16_t word = pgm_read_word(&fontChar->data[i]);
        frame.push_back((uint8_t)((word >> 8) & 0xFF));
    }
}
```

#### 2. **Standard Font Path** (`encodeText`)
```cpp
// For Pixeloid Sans fonts (10px, 16px)
const std::array<uint8_t, 7> header = { 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00 };
const std::array<uint8_t, 3> trailer = { 0x00, 0x00, 0x00 };

for (char character : text) {
    auto it = font.find(character);
    const FontChar& fontChar = it->second;
    int rows = std::min((int)fontChar.data.size(), font_height);
    
    // Build character bitmap
    for (int row = 0; row < rows; row++) {
        uint16_t line_data = fontChar.data[row];
        char_bytes.push_back((uint8_t)((line_data >> 8) & 0xFF));
        char_bytes.push_back((uint8_t)(line_data & 0xFF));
    }
    
    // Apply bit transformations
    char_bytes = Helpers::switchEndian(char_bytes);
    char_bytes = Helpers::logicReverseBitsOrder(char_bytes);
    
    // Wrap with header/trailer
    frame.insert(frame.end(), header.begin(), header.end());
    frame.insert(frame.end(), char_bytes.begin(), char_bytes.end());
    frame.insert(frame.end(), trailer.begin(), trailer.end());
}
```

### Header Calculation Changes

**Dynamic Header Size Based on Font Type**

```cpp
uint16_t header_gap = selectedFont.isCompact
    ? (uint16_t)(0x06 + selectedFont.height * 0x02)  // Cusong: 6 + 2×height
    : (uint16_t)(0x0A + selectedFont.height * 0x02); // Standard: 10 + 2×height

// Total header size calculation
uint16_t header_1_val = HEADER_1_MG + text.length() * header_gap;
uint16_t header_3_val = HEADER_3_MG + text.length() * header_gap;
```

### Payload Validation

**New Validation in `sendText`**

```cpp
// Validate font height
checkRange("font_height", font_height, 0, 255);

// Choose font and validate it fits
SelectedFont selectedFont = selectFont(font_height);
if (matrix_height < selectedFont.height) {
    throw std::invalid_argument("Font height exceeds matrix height");
}
```

### Payload Construction Changes

**Separator Sequence Updated**

```cpp
// OLD: 0xFF FF FF 00 00 00
// NEW: 0xFF FF FF 01 00 00 00
payload.push_back(0xFF); payload.push_back(0xFF); payload.push_back(0xFF);
payload.push_back(0x01); payload.push_back(0x00); payload.push_back(0x00);
payload.push_back(0x00);
```

---

## 3. WEB API ENDPOINT CHANGES

### New sendText Endpoint

**[src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h)**

```cpp
GET /control/raw/sendText
Parameters:
  - text              : String
  - animation         : int (0-7)
  - save_slot         : int (1-10)
  - speed             : int
  - colorR, colorG, colorB : int (0-255)
  - rainbow_mode      : int (0-9)
  - matrix_height     : int (0-255)
  - font_height       : int (7, 10, or 16) [OPTIONAL, default=16]
```

**Example Calls:**

```bash
# Using default 16px font
/control/raw/sendText?device=paired_device&text=Hello&matrix_height=20&font_height=16

# Using compact 7px font for narrow screen
/control/raw/sendText?device=paired_device&text=你好&matrix_height=20&font_height=7

# Using 10px font for balanced display
/control/raw/sendText?device=paired_device&text=Test&matrix_height=32&font_height=10
```

---

## 4. ARCHITECTURE RESTRUCTURING

### File Organization Changes

**Old Structure:** `src/web/` → **New Structure:** `src/webserver/`, `src/wifi/`, `src/bluetooth/`, `src/control/`

```
src/
├── web/
│   ├── Webserver.cpp/h
│   ├── Endpoint.h
│   ├── Helpers.h
│   └── device/
│       └── raw/sendText.h
└── wifi/
    └── network/pair/

↓ REFACTORED TO:

src/
├── webserver/
│   ├── server.cpp/h
│   ├── endpoint.h
│   ├── helpers.h
│   ├── setup.h
│   └── index.h
├── control/
│   ├── helpers.h
│   ├── index.h
│   └── endpoints/raw/sendText.h
├── wifi/
│   ├── setup.h
│   ├── loop.h
│   ├── registry.h
│   ├── state.h
│   └── endpoints/pairings/
├── bluetooth/
│   ├── setup.h
│   ├── loop.h
│   ├── registry.h
│   └── endpoints/pairings/
└── parser/
    └── GenericRegistry.h
```

### Task-Based Architecture

**New [src/Tasking.h](src/Tasking.h)**

- Replaces callback-heavy approach with task registry
- Organizes code into `setup` and `loop` tasks
- Enables cleaner separation of concerns

**Simplified main.cpp**

```cpp
// OLD: Direct initialization + callbacks
void setup_wifi_pre() { ... }
void setup_improv() { ... }
void setup_connected() { init_bluetooth(); init_webserver(); }
void loop_connected() { loop_deviceregistry(); }

// NEW: Task-based
void setup() {
    Task::runAllOf("setup");  // Executes all registered setup tasks
}

void loop() {
    Task::runAllOf("loop");   // Executes all registered loop tasks
    delay(1);
}
```

---

## 5. CONFIGURATION & BUILD CHANGES

### platformio.ini Changes

**Build Flags:**
```diff
- -fexceptions
+ -std=c++14
```

**Monitor Settings:**
```diff
- monitor_speed = 921600
- monitor_filters = esp32_exception_decoder
+ monitor_speed = 115200
  [removed exception decoder filter]
```

**ESP32-S3 Specific:**
```diff
- -DARDUINO_USB_CDC_ON_BOOT=1
+ -DARDUINO_USB_CDC_ON_BOOT=0
+ -DARDUINO_USB_MODE=1
```

---

## 6. DOCUMENTATION & TOOLS

### New Documentation Files

| File | Purpose | Size |
|------|---------|------|
| [Size.md](Size.md) | Comprehensive BLE protocol + screen size specs | 1,791 lines |
| [SENDTEXT_REFACTOR_PLAN.md](SENDTEXT_REFACTOR_PLAN.md) | Detailed refactoring notes | 508 lines |
| [FONT_CONVERSION_SUMMARY.md](FONT_CONVERSION_SUMMARY.md) | Font generation process | 298 lines |
| [FONT_CONVERTER_QUICKSTART.md](FONT_CONVERTER_QUICKSTART.md) | How-to guide | 106 lines |
| [CUSONG_FONT_SOLUTION.md](CUSONG_FONT_SOLUTION.md) | Cusong font handling | 150 lines |
| [MISSING_CHARACTERS.md](MISSING_CHARACTERS.md) | Character support analysis | 272 lines |
| [IMPLEMENTATION_INDEX.md](IMPLEMENTATION_INDEX.md) | Code organization reference | 337 lines |
| [iPixel_PROTOCOL.md](iPixel_PROTOCOL.md) | BLE protocol specification | 119 lines |

### New Scripts (Python Font Tools)

| Script | Purpose |
|--------|---------|
| [font_converter.py](scripts/font_converter.py) | Convert TrueType fonts to C++ headers |
| [extract_cusong_font_corrected.py](scripts/extract_cusong_font_corrected.py) | Extract Cusong glyphs from sniffs |
| [build_cusong_from_sniff.py](scripts/build_cusong_from_sniff.py) | Build font from Bluetooth sniffs |
| [sniff_extractor.py](scripts/sniff_extractor.py) | Parse BLE protocol packets |
| [cleanup_spaces.py](scripts/cleanup_spaces.py) | Font data formatting |

---

## 7. KEY TECHNICAL IMPROVEMENTS

### 1. **Memory Efficiency**
- Compact font storage using `uint16_t[20]` instead of full `FontChar` struct
- Reduced header size for compact fonts (6 vs 10 bytes base)
- PROGMEM storage for font data (flash instead of RAM)

### 2. **Scalability**
- Font selection mechanism allows easy addition of new fonts
- Header calculations adjust dynamically per font type
- Validation ensures fonts fit within screen dimensions

### 3. **Protocol Compliance**
- Updated separator sequence matches official device behavior
- Variable header gap accounts for different font sizes
- Support for all screen types (16×16 to 32×448)

### 4. **Backward Compatibility**
- `font_height` parameter defaults to 16 (original behavior)
- Original `FONT_VCR_OSD_MONO_16PX` kept in codebase
- Existing API calls continue to work

---

## 8. TESTING & VALIDATION

### New Test Artifacts

- [test/encode_text_native/encode_text](test/encode_text_native/encode_text) - Native binary test executable (84KB)
- Reference sniff files in [refactor/](refactor/) directory for protocol validation

### Commit History (Develop Only Features)

19 commits beyond main branch:

1. New task/webserver system + initial wifi & bluetooth pairing
2. Removed old implementations
3. Fix crash when device is unknown
4. Add API documentation and improve WiFi handling
5. **Add iPixel BLE Protocol documentation** ← Protocol specs
6. **Add font converter script and PixeloidSans font file** ← Font tools
7. **Refactor Bluetooth Sniffing Logs and Enhance Text Sending** ← SendText improvements
8. Testing hardcoded
9. Fix pixel data alignment in character encoding
10. Fix trailing zeros in pixel data array
11. CRC working, length packet matter
12. Refactor CRC calculation
13. Refactor save slot handling
14. **Add scripts for Cusong font extraction** ← Font generation
15. **Add extended glyph support and cleanup for Cusong font** ← Cusong implementation
16. Fonts process ← Font system finalization
17. **Refactor code structure for improved readability** ← Architecture changes
18. Various bug fixes and optimizations

---

## 9. MIGRATION GUIDE

### For API Consumers

**To use specific font sizes, add the `font_height` parameter:**

```bash
# Small text (7px) on narrow screens
GET /control/raw/sendText?device=DEV&text=Hi&matrix_height=20&font_height=7

# Medium text (10px) on mid-size screens  
GET /control/raw/sendText?device=DEV&text=Hello&matrix_height=32&font_height=10

# Large text (16px) on big screens
GET /control/raw/sendText?device=DEV&text=Big&matrix_height=64&font_height=16
```

### For Firmware Developers

1. Always call `selectFont()` before encoding text
2. Validate that `matrix_height >= font_height`
3. Use appropriate encoding path based on `isCompact` flag
4. Account for different header gap calculations

---

## 10. SUMMARY OF CHANGES

| Category | Original | New | Impact |
|----------|----------|-----|--------|
| **Font Count** | 1 (16px only) | 3 (7px, 10px, 16px) | Full flexibility for screen sizes |
| **Screen Support** | Fixed | Dynamic | 20 different screen sizes |
| **Text Encoding** | Single path | Dual path | Optimized for each font type |
| **Header Size** | Fixed | Variable | Efficient payload sizes |
| **API Flexibility** | Hardcoded | Parameterized | User control via `font_height` |
| **Documentation** | Minimal | Extensive | +3,700 lines of specs & guides |
| **Code Organization** | Monolithic | Modular | Clear separation of concerns |
| **Backward Compat** | N/A | Maintained | Existing code still works |

---

**Total Changes:** 126 files changed, 11,000+ insertions, 945 deletions across 19 commits.
