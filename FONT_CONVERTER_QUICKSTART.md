# Font Converter Quick Start Guide

## Installation

### One-time setup:
```bash
cd /Users/jesus/Jesus/repositories/Padel/iPixel-ESP32
python3 -m pip install pillow fonttools
```

## Basic Usage

### Generate a 10px font:
```bash
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --output include/Font_PIXELOID_SANS_10PX.h
```

### Generate a 16px font:
```bash
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 16 \
  --output include/Font_PIXELOID_SANS_16PX.h
```

### Preview font without saving:
```bash
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --preview "Test Text 123"
```

## Common Tasks

### Generate multiple sizes at once:
```bash
for size in 8 10 12 16 20 24; do
  python3 scripts/font_converter.py \
    --input refactor/PixeloidSans.ttf \
    --height $size \
    --output "include/Font_PIXELOID_SANS_${size}PX.h" \
    --font-name "PIXELOID_SANS_${size}PX"
done
```

### Use extended character set (with accents):
```bash
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --output include/Font_PIXELOID_SANS_10PX_EXTENDED.h \
  --charset extended
```

### Verbose output for debugging:
```bash
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --verbose \
  --output include/Font_PIXELOID_SANS_10PX.h
```

### Use a different TTF font:
```bash
python3 scripts/font_converter.py \
  --input path/to/your_font.ttf \
  --height 12 \
  --output include/Font_CUSTOM_12PX.h \
  --font-name CUSTOM_12PX
```

## Output Format

The script generates a C++ header file with:
```cpp
const std::map<char, FontChar> FONT_PIXELOID_SANS_10PX = {
    {'A', FontChar{
        .width = 7,
        .data = { 0x0000, 0x0000, ... }
    }},
    // ... more characters ...
};
```

Ready to include and use in `include/Font.h`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'PIL'` | Run: `pip install pillow` |
| Font file not found | Use absolute path or check file exists: `ls refactor/PixeloidSans.ttf` |
| Output file permission denied | Check directory permissions: `mkdir -p include/` |
| Characters look distorted | Try different height value (8, 10, 12, 16, 20, 24) |

## Already Generated

✅ `include/Font_PIXELOID_SANS_10PX.h` — 10px, 89 characters
✅ `include/Font_PIXELOID_SANS_16PX.h` — 16px, 89 characters

Ready to be integrated into `include/Font.h`
