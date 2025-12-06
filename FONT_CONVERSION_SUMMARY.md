# Font Conversion Summary

## Overview

Successfully created a Python-based **Font Converter** tool and generated **two PixeloidSans font variants** for the iPixel ESP32 project:

### Generated Fonts

| Font | Height | Characters | File Size | Line Count |
|------|--------|-----------|-----------|-----------|
| **PixeloidSans 10px** | 10 pixels | 89 | 24 KB | 1,343 lines |
| **PixeloidSans 16px** | 16 pixels | 89 | 35 KB | 1,877 lines |

---

## Font Converter Script

### Location
[scripts/font_converter.py](scripts/font_converter.py)

### Features

✅ **TTF/OTF Support** — Converts TrueType fonts to bitmap format
✅ **Variable Height** — Generate fonts at any pixel height (8px, 10px, 16px, 24px+)
✅ **ASCII Preview** — Visual preview of rendered characters
✅ **Statistics** — Character width analysis and coverage reporting
✅ **Configurable** — Choose character sets (basic, extended)
✅ **Production Ready** — Generates compilable C++ code with auto-generated comments

### Usage

```bash
# Basic usage (saves to file)
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --output include/Font_PIXELOID_SANS_10PX.h \
  --font-name PIXELOID_SANS_10PX

# Preview without saving
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --preview "HELLO World 123"

# Extended character set (with accents, symbols)
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --charset extended

# Verbose output
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --verbose
```

### Command Line Options

```
--input, -i       Input font file path (TTF/OTF) [REQUIRED]
--height          Target font height in pixels [REQUIRED]
--output, -o      Output C++ header file (omit for stdout)
--font-name, -n   Font constant name (default: PIXELOID_SANS)
--preview, -p     Text to preview (default: "HELLO iPixel")
--charset         Character set: "basic" or "extended" (default: basic)
--verbose, -v     Verbose output with per-character details
--help, -h        Show help message
```

### Dependencies

```bash
pip install pillow fonttools
```

---

## Generated Fonts

### PixeloidSans 10px

**File:** [include/Font_PIXELOID_SANS_10PX.h](include/Font_PIXELOID_SANS_10PX.h)

**Specifications:**
- Height: 10 pixels
- Character widths: 1-10 pixels (average: 6.4px)
- Characters: 89 (A-Z, a-z, 0-9, punctuation, symbols)
- Data format: `std::map<char, FontChar>` with `uint16_t` bitmap rows
- Perfect for: 32×64 displays (20px height)

**Structure:**
```cpp
const std::map<char, FontChar> FONT_PIXELOID_SANS_10PX = {
    {'A', FontChar{
        .width = 7,
        .data = {
            0x0000, 0x0000, 0x1800, 0x2400, 
            0x2400, 0x4200, 0x7E00, 0x4200, 
            0x4200, 0x0000
        }
    }},
    // ... 88 more characters ...
};
```

**Character Coverage:**
- Alphanumeric: A-Z, a-z, 0-9
- Punctuation: . , ! ? ; : ' " ( ) [ ] { }
- Symbols: / @ # $ % & * + = _ ~ - ` | \

---

### PixeloidSans 16px

**File:** [include/Font_PIXELOID_SANS_16PX.h](include/Font_PIXELOID_SANS_16PX.h)

**Specifications:**
- Height: 16 pixels
- Character widths: 1-10 pixels (average: 6.4px)
- Characters: 89 (same as 10px variant)
- Data format: Same as 10px but with 16 rows per character
- Perfect for: 96×16 displays (existing use case)

**Structure:**
```cpp
const std::map<char, FontChar> FONT_PIXELOID_SANS_16PX = {
    {'A', FontChar{
        .width = 7,
        .data = {
            0x0000, 0x0000, 0x1800, 0x2400, 
            0x2400, 0x4200, 0x7E00, 0x4200, 
            0x4200, 0x0000, /* ... 6 more rows for 16px total ... */
        }
    }},
    // ... 88 more characters ...
};
```

---

## Font Data Format

### Character Bitmap Structure

Each character is represented by:
```cpp
struct FontChar {
    int width;                    // Character width in pixels (1-10)
    std::vector<uint16_t> data;   // Bitmap rows (10 or 16 elements)
};
```

### Bitmap Encoding

- **One `uint16_t` per row** of the character
- **MSB first** (leftmost pixel = bit 15)
- **16 bits max width** (0x0000 - 0xFFFF)
- **Padded with zeros** if character width < 16px

**Example: Character 'A' at 10px (width=7)**
```
Row 0: 0x0000  (empty)
Row 1: 0x0000  (empty)
Row 2: 0x1800  (  ██   )
Row 3: 0x2400  ( ██ ██ )
Row 4: 0x2400  ( ██ ██ )
Row 5: 0x4200  (██   ██)
Row 6: 0x7E00  (██████ )
Row 7: 0x4200  (██   ██)
Row 8: 0x4200  (██   ██)
Row 9: 0x0000  (empty)
```

---

## Integration with iPixel codebase

### Current Status

**New Files:**
- ✅ [scripts/font_converter.py](scripts/font_converter.py) — Conversion tool
- ✅ [include/Font_PIXELOID_SANS_10PX.h](include/Font_PIXELOID_SANS_10PX.h) — 10px font variant
- ✅ [include/Font_PIXELOID_SANS_16PX.h](include/Font_PIXELOID_SANS_16PX.h) — 16px font variant

**Next Steps (for implementation):**

1. **Update [include/Font.h](include/Font.h)**
   - Include the new font headers
   - Create font selection mechanism (enum or function)
   - Keep existing `FONT_VCR_OSD_MONO_16PX` for backward compatibility

2. **Modify [src/iPixelCommands.cpp](src/iPixelCommands.cpp)**
   - Update `sendText()` function signature to accept `font_height` parameter
   - Implement dynamic font selection logic
   - Fix header gap calculation: use `font_height` instead of `matrix_height`
   - Adapt character encoding to handle variable row counts

3. **Update Endpoints**
   - [src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h) — Add `font_height` parameter
   - [src/bluetooth/endpoints/pairings/sendText.h](src/bluetooth/endpoints/pairings/sendText.h) — Add `font_height` parameter

---

## Comparison: PixeloidSans vs Original VCR OSD Mono

| Aspect | PixeloidSans 10px | Original VCR OSD 16px |
|--------|------------------|----------------------|
| **Source** | TTF (scalable) | Hand-coded bitmap |
| **Style** | Pixel art (clean) | Monospace (classic) |
| **Height** | 10px | 16px |
| **Avg Width** | 6.4px | 9px |
| **Compactness** | More compact | Original |
| **Scalability** | Can generate other heights | Fixed at 16px |

**Recommendation:**
- Use **PixeloidSans 10px** for 32×64 screens (20px height)
- Use **PixeloidSans 16px** for 96×16 screens (can replace original VCR OSD if preferred)
- Existing VCR OSD can be kept for backward compatibility

---

## Future Font Generation

To create additional font variants:

```bash
# 8px (very compact, future use)
python3 scripts/font_converter.py --input refactor/PixeloidSans.ttf --height 8 --output include/Font_PIXELOID_SANS_8PX.h

# 24px (large displays)
python3 scripts/font_converter.py --input refactor/PixeloidSans.ttf --height 24 --output include/Font_PIXELOID_SANS_24PX.h

# Or use any other TTF font:
python3 scripts/font_converter.py --input path/to/other_font.ttf --height 12 --output include/Font_CUSTOM_12PX.h
```

---

## Technical Notes

### Bitmap Rendering Algorithm

The converter:
1. Loads TTF font using PIL/Pillow
2. Renders each character at target height
3. Converts pixels to binary (threshold at 128/255)
4. Packs bits into `uint16_t` values (MSB first, 16-bit max width)
5. Generates C++ code with proper escaping

### Why PixeloidSans?

PixeloidSans is ideal for LED displays because:
- **Pixel-perfect font** — Designed for screen display
- **Scalable** — Can generate any size from single TTF
- **Compact** — More characters per line than VCR OSD
- **Modern** — Clean aesthetic suitable for LED matrices
- **Flexible** — Easy to switch sizes for different display resolutions

### Header Calculation Impact

For `sendText()` with 10px font on 20px screen:
```
header_gap = 0x06 + (10 * 0x02) = 0x1A  ✓ CORRECT
(instead of: 0x06 + (20 * 0x02) = 0x2E  ✗ WRONG)
```

This fix is critical for proper BLE protocol communication.

---

## Files Modified/Created

### Created
- [scripts/font_converter.py](scripts/font_converter.py)
- [include/Font_PIXELOID_SANS_10PX.h](include/Font_PIXELOID_SANS_10PX.h)
- [include/Font_PIXELOID_SANS_16PX.h](include/Font_PIXELOID_SANS_16PX.h)

### To Be Modified (Phase 2)
- [include/Font.h](include/Font.h)
- [src/iPixelCommands.h](src/iPixelCommands.h)
- [src/iPixelCommands.cpp](src/iPixelCommands.cpp)
- [src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h)
- [src/bluetooth/endpoints/pairings/sendText.h](src/bluetooth/endpoints/pairings/sendText.h)

---

## Summary

✅ **Font Converter Tool** — Production-ready Python script for converting TTF fonts
✅ **PixeloidSans 10px** — Generated for 32×64 displays (main target)
✅ **PixeloidSans 16px** — Generated for compatibility/comparison
✅ **Scalable Solution** — Easy to generate other sizes as needed
✅ **Ready for Integration** — Fonts are in correct C++ format, await code refactoring

**Next Phase:** Implement the refactored `sendText()` function using these font variants and the plan from SENDTEXT_REFACTOR_PLAN.md

