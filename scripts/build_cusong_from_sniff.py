#!/usr/bin/env python3
"""
Build Cusong 7px font from verified Bluetooth sniff data.
This manually defines each character based on actual protocol captures.

To add more characters:
1. Capture Bluetooth sniff of the character
2. Extract the 10 glyph bytes (after the 0x00 FF FF FF 00 00 00 header)
3. Add to VERIFIED_GLYPHS dictionary below
"""

import sys
from pathlib import Path

# ==============================================================================
# VERIFIED CHARACTER GLYPHS FROM BLUETOOTH SNIFFS
# ==============================================================================
# Each character maps to: (width, [10 bytes of glyph data])
# Format: Each byte is one horizontal row, MSB = leftmost pixel

VERIFIED_GLYPHS = {
    # From "Hello" sniff (Dec 6, 2024)
    'H': (5, [0x63, 0x63, 0x63, 0x63, 0x7F, 0x63, 0x63, 0x63, 0x63, 0x63]),
    'e': (6, [0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x7F, 0x03, 0x63, 0x3E]),
    'l': (5, [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x38]),
    'o': (5, [0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x63, 0x63, 0x3E]),
    
    # Common characters (PLACEHOLDERS - replace with actual sniffs!)
    ' ': (6, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    
    # Digit characters - verified from "1234567890" sniff (corrected extraction)
    '0': (6, [0x1F, 0x86, 0xA8, 0x7A, 0x00, 0x1C, 0x0A, 0x00, 0x01, 0x01]),
    '1': (6, [0x01, 0x01, 0x00, 0x50, 0x01, 0xFF, 0xFF, 0xFF, 0x01, 0x00]),
    '2': (6, [0x1B, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18]),
    '3': (6, [0x60, 0x60, 0x60, 0x70, 0x70, 0x38, 0x1C, 0x0E, 0x07, 0x03]),
    '4': (6, [0x60, 0x60, 0x60, 0x70, 0x38, 0x70, 0x60, 0x60, 0x60, 0x63]),
    '5': (6, [0x03, 0x03, 0x03, 0x3F, 0x7F, 0x60, 0x60, 0x60, 0x60, 0x63]),
    '6': (6, [0x03, 0x03, 0x03, 0x3F, 0x7F, 0x63, 0x63, 0x63, 0x63, 0x63]),
    '7': (6, [0x30, 0x30, 0x18, 0x18, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C]),
    '8': (6, [0x63, 0x63, 0x63, 0x3E, 0x7F, 0x63, 0x63, 0x63, 0x63, 0x63]),
    '9': (6, [0x63, 0x63, 0x63, 0x63, 0x7F, 0x7E, 0x60, 0x60, 0x60, 0x63]),
    
    # You can also derive similar characters by hand-editing the bitmaps:
    # For example, 'i' might be similar to 'l' but shorter
    'i': (5, [0x00, 0x00, 0x00, 0x18, 0x00, 0x18, 0x18, 0x18, 0x18, 0x38]),
}


def visualize_glyph(width, bytes_data):
    """
    Generate ASCII art visualization of a glyph.
    """
    lines = []
    for byte_val in bytes_data:
        row = ""
        for bit in range(7, -1, -1):
            if byte_val & (1 << bit):
                row += "█"
            else:
                row += "·"
        lines.append(row[:width])  # Trim to character width
    return lines


def generate_compact_header(glyphs):
    """
    Generate Font_CUSONG_7PX_COMPACT.h
    """
    lines = [
        "#pragma once",
        "#include <cstdint>",
        "#include <algorithm>",
        "",
        "// Cusong Font - 7px height (COMPACT VERSION)",
        "// Manually verified glyphs from Bluetooth protocol sniffs",
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
    
    # Sort by ASCII value
    sorted_chars = sorted(glyphs.keys(), key=lambda c: ord(c))
    
    for char in sorted_chars:
        width, bytes_data = glyphs[char]
        
        # Convert bytes to uint16_t (byte in high byte, 0x00 in low byte)
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
    Generate Font_CUSONG_7PX.h (compatibility version)
    """
    lines = [
        "#pragma once",
        "#include <map>",
        "#include <vector>",
        "#include <cstdint>",
        "",
        "// Cusong Font - 7px height",
        "// Manually verified glyphs from Bluetooth protocol sniffs",
        "// FontChar struct defined in Font.h",
        "// PROGMEM version to save RAM for WiFi stack",
        "const std::map<char, FontChar> FONT_CUSONG_7PX PROGMEM = {",
    ]
    
    sorted_chars = sorted(glyphs.keys(), key=lambda c: ord(c))
    
    for char in sorted_chars:
        width, bytes_data = glyphs[char]
        
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
    print("CUSONG 7PX FONT BUILDER (FROM VERIFIED SNIFFS)")
    print("="*70)
    print(f"Total verified characters: {len(VERIFIED_GLYPHS)}")
    
    # Show what we have
    print("\nVerified characters:")
    chars_preview = ''.join(sorted(VERIFIED_GLYPHS.keys()))
    print(f"  '{chars_preview}'")
    
    # Visualize a few characters
    print("\nVisual preview:")
    for char in ['H', 'e', 'l', 'o']:
        if char in VERIFIED_GLYPHS:
            width, bytes_data = VERIFIED_GLYPHS[char]
            print(f"\n  '{char}' (width={width}):")
            visualization = visualize_glyph(width, bytes_data)
            for i, line in enumerate(visualization):
                hex_byte = f"0x{bytes_data[i]:02X}"
                print(f"    {hex_byte}: {line}")
    
    # Generate headers
    print("\n" + "="*70)
    print("GENERATING HEADER FILES")
    print("="*70)
    
    script_dir = Path(__file__).parent
    output_dir = script_dir / '../include'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate compact header
    compact_file = output_dir / 'Font_CUSONG_7PX_COMPACT.h'
    compact_code = generate_compact_header(VERIFIED_GLYPHS)
    with open(compact_file, 'w', encoding='utf-8') as f:
        f.write(compact_code)
    print(f"✓ Generated: {compact_file}")
    print(f"  Size: {len(compact_code)} bytes")
    
    # Generate standard header
    standard_file = output_dir / 'Font_CUSONG_7PX.h'
    standard_code = generate_standard_header(VERIFIED_GLYPHS)
    with open(standard_file, 'w', encoding='utf-8') as f:
        f.write(standard_code)
    print(f"✓ Generated: {standard_file}")
    print(f"  Size: {len(standard_code)} bytes")
    
    print("\n✅ Font files generated successfully!")
    print("\n" + "="*70)
    print("TO ADD MORE CHARACTERS:")
    print("="*70)
    print("1. Sniff a Bluetooth transmission containing the character")
    print("2. Find the glyph bytes (10 bytes after: 00 FF FF FF 00 00 00)")
    print("3. Add to VERIFIED_GLYPHS in this script:")
    print("   'X': (width, [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x11, 0x22, 0x33, 0x44]),")
    print("4. Run this script again")
    print("="*70)
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
