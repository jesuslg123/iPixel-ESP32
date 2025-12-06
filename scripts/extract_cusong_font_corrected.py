#!/usr/bin/env python3
"""
Extract Cusong font glyphs in the CORRECT format matching the iPixel protocol.
Based on actual Bluetooth sniff data showing the exact byte format the device expects.

The protocol format for 7px Cusong font:
- Each character is 10 bytes of glyph data
- Each byte represents a horizontal row of pixels (MSB = leftmost pixel)
- Height is always 10 bytes (padded with 0x00 if needed)
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
FONT_PATH = SCRIPT_DIR / '../refactor/cusong16_zitidi.com.ttf'
OUTPUT_DIR = SCRIPT_DIR / '../include'

# Target font size
FONT_SIZE = 11  # Render at slightly larger size for better quality

# Characters to extract
CHARACTERS = (
    # Space and punctuation
    ' !(),-.:;?'
    # Numbers
    '0123456789'
    # Uppercase letters
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Lowercase letters  
    'abcdefghijklmnopqrstuvwxyz'
    # Special brackets
    '[]{}' 
)


def render_character_bitmap(font, char):
    """
    Render a character and extract its bitmap in the correct protocol format.
    
    Returns:
        width: Character width in pixels
        bitmap_bytes: List of 10 bytes, each representing a horizontal row
    """
    # Get character bounding box
    bbox = font.getbbox(char)
    char_width = max(bbox[2] - bbox[0], 1)
    char_height = max(bbox[3] - bbox[1], 1)
    
    # Special case for space
    if char == ' ':
        return 6, [0x00] * 10
    
    # Create image with padding
    img_width = char_width + 4
    img_height = 10  # Fixed height for protocol
    
    img = Image.new('L', (img_width, img_height), 0)  # Grayscale
    draw = ImageDraw.Draw(img)
    
    # Draw character (centered vertically if needed)
    y_offset = (img_height - char_height) // 2
    draw.text((2, y_offset), char, fill=255, font=font)
    
    # Convert to bitmap bytes (one byte per row)
    bitmap_bytes = []
    pixels = img.load()
    
    for y in range(img_height):
        row_byte = 0
        for x in range(min(8, img_width)):  # Max 8 pixels wide (1 byte)
            if pixels[x, y] > 128:  # Threshold
                row_byte |= (0x80 >> x)  # MSB first
        bitmap_bytes.append(row_byte)
    
    # Calculate actual character width (trim padding)
    actual_width = 0
    for x in range(img_width - 1, -1, -1):
        for y in range(img_height):
            if pixels[x, y] > 128:
                actual_width = max(actual_width, x + 1)
                break
        if actual_width > 0:
            break
    
    # Ensure minimum width
    if actual_width == 0:
        actual_width = 1
    
    # Cap at reasonable width
    actual_width = min(actual_width, 7)
    
    return actual_width, bitmap_bytes


def verify_against_sniff(glyphs):
    """
    Verify extracted glyphs against known sniffed data.
    """
    print("\n" + "="*70)
    print("VERIFICATION AGAINST BLUETOOTH SNIFF DATA")
    print("="*70)
    
    # Known good data from Bluetooth sniff
    reference_data = {
        'H': [0x63, 0x63, 0x63, 0x63, 0x7F, 0x63, 0x63, 0x63, 0x63, 0x63],
        'e': [0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x7F, 0x03, 0x63, 0x3E],
        'l': [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x38],
        'o': [0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x63, 0x63, 0x3E],
    }
    
    for char, ref_bytes in reference_data.items():
        if char not in glyphs:
            print(f"\n❌ '{char}': NOT FOUND in extracted glyphs")
            continue
        
        extracted = glyphs[char]['bytes']
        
        print(f"\n'{char}':")
        print(f"  Reference : {' '.join(f'{b:02X}' for b in ref_bytes)}")
        print(f"  Extracted : {' '.join(f'{b:02X}' for b in extracted)}")
        
        if extracted == ref_bytes:
            print(f"  ✅ MATCH!")
        else:
            print(f"  ❌ MISMATCH")
            print(f"  Visual comparison:")
            for i in range(10):
                ref_bits = format(ref_bytes[i], '08b').replace('0', '·').replace('1', '█')
                ext_bits = format(extracted[i], '08b').replace('0', '·').replace('1', '█')
                print(f"    Row {i}: {ref_bits}  vs  {ext_bits}")


def generate_compact_header(glyphs):
    """
    Generate the compact C++ header file.
    """
    lines = [
        "#pragma once",
        "#include <cstdint>",
        "#include <algorithm>",
        "",
        "// Cusong Font - 7px height (COMPACT VERSION)",
        "// Extracted from: cusong16_zitidi.com.ttf",
        "// Uses static array + binary search instead of std::map for minimal RAM overhead",
        "",
        "struct CompactFontChar {",
        "    char ascii;",
        "    uint8_t width;",
        "    uint16_t data[10];  // 7px height = 10 uint16_t words max",
        "};",
        "",
        "// PROGMEM - stored in flash, not RAM",
        "static const CompactFontChar CUSONG_7PX_DATA[] PROGMEM = {",
    ]
    
    # Sort characters by ASCII value
    sorted_chars = sorted(glyphs.keys(), key=lambda c: ord(c))
    
    for char in sorted_chars:
        glyph = glyphs[char]
        width = glyph['width']
        bytes_data = glyph['bytes']
        
        # Convert bytes to uint16_t (store byte in high byte, 0x00 in low byte)
        words = [f"0x{byte:02X}00" for byte in bytes_data]
        words_str = ', '.join(words)
        
        # Escape special characters
        if char == "'":
            char_display = "\\'"
        elif char == '\\':
            char_display = "\\\\"
        else:
            char_display = char
        
        lines.append(f"    {{'{char_display}', {width}, {{ {words_str} }}}},")
    
    lines.extend([
        "};",
        "",
        "static const int CUSONG_7PX_COUNT = sizeof(CUSONG_7PX_DATA) / sizeof(CompactFontChar);",
        "",
        "// Lookup function - binary search in PROGMEM array",
        "inline const CompactFontChar* getCusong7pxChar(char c) {",
        "    int left = 0, right = CUSONG_7PX_COUNT - 1;",
        "    while (left <= right) {",
        "        int mid = (left + right) / 2;",
        "        char mid_char = pgm_read_byte(&CUSONG_7PX_DATA[mid].ascii);",
        "        if (mid_char == c) {",
        "            return &CUSONG_7PX_DATA[mid];",
        "        } else if (mid_char < c) {",
        "            left = mid + 1;",
        "        } else {",
        "            right = mid - 1;",
        "        }",
        "    }",
        "    return nullptr;  // Not found",
        "}",
        "",
    ])
    
    return '\n'.join(lines)


def generate_standard_header(glyphs):
    """
    Generate the standard C++ header file (for compatibility).
    """
    lines = [
        "#pragma once",
        "#include <map>",
        "#include <vector>",
        "#include <cstdint>",
        "",
        "// Cusong Font - 7px height",
        "// Extracted from: cusong16_zitidi.com.ttf",
        "// FontChar struct defined in Font.h",
        "// PROGMEM version to save RAM for WiFi stack",
        "const std::map<char, FontChar> FONT_CUSONG_7PX PROGMEM = {",
    ]
    
    sorted_chars = sorted(glyphs.keys(), key=lambda c: ord(c))
    
    for char in sorted_chars:
        glyph = glyphs[char]
        width = glyph['width']
        bytes_data = glyph['bytes']
        
        # Convert to uint16_t words
        words = [f"0x{byte:02X}00" for byte in bytes_data]
        words_str = ', '.join(words)
        
        # Escape special characters
        if char == "'":
            char_display = "\\'"
        elif char == '\\':
            char_display = "\\\\"
        else:
            char_display = char
        
        ascii_val = ord(char)
        lines.append(f"    {{'{char_display}', {{{width}, {{ {words_str} }}}}}},  // ASCII {ascii_val}")
    
    lines.extend([
        "};",
        "",
    ])
    
    return '\n'.join(lines)


def main():
    print("\n" + "="*70)
    print("CUSONG FONT EXTRACTION (CORRECTED)")
    print("="*70)
    print(f"Font: {FONT_PATH.name}")
    print(f"Characters: {len(CHARACTERS)}")
    
    # Check font file exists
    if not FONT_PATH.exists():
        print(f"\n❌ ERROR: Font file not found: {FONT_PATH}")
        return False
    
    # Load font
    try:
        font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
        print(f"✓ Loaded font at {FONT_SIZE}px")
    except Exception as e:
        print(f"\n❌ ERROR: Failed to load font: {e}")
        return False
    
    # Extract glyphs
    print("\nExtracting glyphs...")
    glyphs = {}
    
    for i, char in enumerate(CHARACTERS):
        try:
            width, bitmap_bytes = render_character_bitmap(font, char)
            glyphs[char] = {
                'width': width,
                'bytes': bitmap_bytes
            }
            
            # Show visual preview for first few chars
            if i < 5:
                print(f"\n  '{char}' (width={width}):")
                for row_idx, byte_val in enumerate(bitmap_bytes):
                    bits = format(byte_val, '08b').replace('0', '·').replace('1', '█')
                    print(f"    Row {row_idx}: {bits}  (0x{byte_val:02X})")
        
        except Exception as e:
            print(f"  ❌ Failed to extract '{char}': {e}")
    
    print(f"\n✓ Extracted {len(glyphs)} characters")
    
    # Verify against known good data
    verify_against_sniff(glyphs)
    
    # Generate headers
    print("\n" + "="*70)
    print("GENERATING HEADER FILES")
    print("="*70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate compact header
    compact_file = OUTPUT_DIR / 'Font_CUSONG_7PX_COMPACT.h'
    compact_code = generate_compact_header(glyphs)
    with open(compact_file, 'w', encoding='utf-8') as f:
        f.write(compact_code)
    print(f"✓ Generated: {compact_file}")
    print(f"  Size: {len(compact_code)} bytes")
    
    # Generate standard header
    standard_file = OUTPUT_DIR / 'Font_CUSONG_7PX.h'
    standard_code = generate_standard_header(glyphs)
    with open(standard_file, 'w', encoding='utf-8') as f:
        f.write(standard_code)
    print(f"✓ Generated: {standard_file}")
    print(f"  Size: {len(standard_code)} bytes")
    
    print("\n✅ Font extraction complete!")
    print("\nNext steps:")
    print("  1. Review the verification output above")
    print("  2. Test with your device")
    print("  3. Adjust FONT_SIZE parameter if glyphs don't match")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
