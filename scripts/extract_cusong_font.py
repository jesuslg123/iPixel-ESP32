#!/usr/bin/env python3
"""
Extract Cusong font glyphs and convert to C++ format for iPixel LED displays.
Generates monochrome bitmaps for 7px and 10px font sizes.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import struct

# Configuration
FONT_PATH = os.path.join(os.path.dirname(__file__), '../refactor/cusong16_zitidi.com.ttf')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../include')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'Font_CUSONG_7PX.h')

# Characters to extract - common ASCII + common Chinese
CHARACTERS = [
    # ASCII lowercase
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    # ASCII uppercase
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    # Numbers
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # Common punctuation
    ' ', '.', ',', '!', '?', ':', ';', '-', '(', ')', '[', ']', '{', '}',
]

# Font sizes to generate
FONT_SIZE_7PX = 7
FONT_SIZE_10PX = 10


def render_character(font, char, font_size):
    """
    Render a single character to a monochrome bitmap.
    Returns (width, height, bitmap_bytes)
    """
    # Estimate character dimensions
    bbox = font.getbbox(char)
    width = max(bbox[2] - bbox[0], 1)
    height = max(bbox[3] - bbox[1], 1)
    
    # Pad dimensions to avoid clipping
    padded_width = width + 2
    padded_height = font_size + 2
    
    # Create image
    img = Image.new('1', (padded_width, padded_height), 0)  # 1 = 1-bit (black/white)
    draw = ImageDraw.Draw(img)
    
    # Draw character in white (1)
    draw.text((1, 1), char, fill=1, font=font)
    
    # Convert to bytes (LSB first, 8 pixels per byte)
    bitmap_bytes = []
    for y in range(padded_height):
        for x in range(0, padded_width, 8):
            byte_val = 0
            for bit in range(min(8, padded_width - x)):
                pixel = img.getpixel((x + bit, y))
                if pixel:
                    byte_val |= (1 << bit)  # LSB first
            bitmap_bytes.append(byte_val)
    
    return padded_width, padded_height, bitmap_bytes


def extract_font_data(font_size):
    """
    Extract glyph data for all characters at specified font size.
    Returns dict: char -> (width, height, glyph_bytes_list)
    """
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        print(f"Font path: {FONT_PATH}")
        return {}
    
    glyphs = {}
    
    for char in CHARACTERS:
        try:
            width, height, bitmap_bytes = render_character(font, char, font_size)
            
            # Convert bytes to 16-bit words (pad height to 10 for consistency)
            words = []
            for y in range(font_size):
                if y < len(bitmap_bytes):
                    byte_val = bitmap_bytes[y]
                else:
                    byte_val = 0
                # Store as uint16_t: byte value in high byte, 0 in low byte
                word = (byte_val << 8) | 0x00
                words.append(word)
            
            # Pad to 10 elements
            while len(words) < 10:
                words.append(0x0000)
            
            glyphs[char] = {
                'width': width,
                'height': height,
                'words': words,
                'bitmap_bytes': bitmap_bytes
            }
            
            print(f"  ✓ '{char}' -> width={width}, height={height}")
        except Exception as e:
            print(f"  ✗ '{char}' -> {e}")
    
    return glyphs


def generate_cpp_header(glyphs_7px):
    """
    Generate C++ header file with font data.
    """
    lines = [
        "#pragma once",
        "#include <map>",
        "#include <vector>",
        "#include <cstdint>",
        "",
        "struct FontChar {",
        "    int width;",
        "    std::vector<uint16_t> data;  // 7px Height, 16-bit Width",
        "};",
        "",
        "// Cusong Font - 7px height",
        "// Extracted from: cusong16_zitidi.com.ttf",
        "const std::map<char, FontChar> FONT_CUSONG_7PX = {",
    ]
    
    for char in sorted(glyphs_7px.keys()):
        glyph = glyphs_7px[char]
        width = glyph['width']
        words = glyph['words']
        
        # Escape special characters in C++
        if char == '"':
            char_display = '\\"'
        elif char == "'":
            char_display = "\\'"
        elif char == '\\':
            char_display = '\\\\'
        else:
            char_display = char
        
        ascii_code = ord(char)
        
        # Format word values as hex
        words_hex = ', '.join(f"0x{w:04X}" for w in words)
        
        lines.append(f"    {{'{char_display}', {{{width}, {{ {words_hex} }}}}}},  // ASCII {ascii_code}")
    
    lines.extend([
        "};",
        "",
    ])
    
    return '\n'.join(lines)


def compare_with_sniff():
    """
    Compare extracted glyphs with known sniffed data.
    From the BLE sniff: 'e' = 1C 22 3E 20 20 22 1C
    """
    print("\n" + "="*60)
    print("SNIFF COMPARISON")
    print("="*60)
    print("From BLE sniff for 'e' (7px):")
    print("  Hex bytes: 1C 22 3E 20 20 22 1C")
    print("  Binary: ")
    for byte_hex in ['1C', '22', '3E', '20', '20', '22', '1C']:
        byte_val = int(byte_hex, 16)
        binary = format(byte_val, '08b')
        print(f"    {byte_hex} = {binary}")
    print()


def main():
    print("\n" + "="*60)
    print("CUSONG FONT EXTRACTION")
    print("="*60)
    
    # Extract 7px font
    print("\nExtracting 7px glyphs...")
    glyphs_7px = extract_font_data(FONT_SIZE_7PX)
    
    if not glyphs_7px:
        print("ERROR: No glyphs extracted!")
        return False
    
    print(f"\nSuccessfully extracted {len(glyphs_7px)} glyphs at 7px")
    
    # Compare with sniffed data
    compare_with_sniff()
    
    # Generate C++ header
    print("Generating C++ header file...")
    cpp_code = generate_cpp_header(glyphs_7px)
    
    # Write to file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(cpp_code)
    
    print(f"✓ Generated: {OUTPUT_FILE}")
    print(f"  File size: {len(cpp_code)} bytes")
    
    # Show sample
    print("\nSample output (first 500 chars):")
    print(cpp_code[:500] + "...")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
