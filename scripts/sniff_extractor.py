#!/usr/bin/env python3
"""
Bluetooth Sniff Data Extractor for Cusong 7px Font
Extracts clean payload data and maps character glyphs from Bluetooth protocol captures.

Usage:
    python3 sniff_extractor.py
    
    Then provide:
    1. Raw hex sniff data (paste when prompted)
    2. Text string that was displayed (e.g., "1234567890")
    
The script will:
    - Clean the hex data
    - Extract the payload section
    - Identify character boundaries (FFFF FF markers)
    - Extract 10-byte glyphs for each character
    - Display visual previews
    - Generate Python code for build_cusong_from_sniff.py
"""

import sys
import re


def clean_hex_data(raw_input):
    """Remove whitespace, formatting, and non-hex characters."""
    # Remove common separators and whitespace
    cleaned = re.sub(r'[\s\t\n\r]', '', raw_input)
    # Remove any non-hex characters
    cleaned = re.sub(r'[^0-9A-Fa-f]', '', cleaned)
    return cleaned.upper()


def hex_to_bytes(hex_string):
    """Convert hex string to byte array."""
    try:
        return bytes.fromhex(hex_string)
    except ValueError as e:
        print(f"Error: Invalid hex data - {e}")
        return None


def find_payload_section(byte_array):
    """
    Find the start of the payload section.
    Payload typically starts after Bluetooth header bytes.
    Look for the first FFFF FF marker.
    """
    for i in range(len(byte_array) - 2):
        if byte_array[i:i+3] == bytes.fromhex('FFFFFF'):
            # Payload likely starts 13 bytes before first marker
            # (to capture the first glyph)
            payload_start = max(0, i - 13)
            return payload_start
    
    print("Warning: No FFFF FF markers found. Using entire data as payload.")
    return 0


def find_character_markers(byte_array):
    """Find all FFFF FF marker positions (character separators)."""
    markers = []
    for i in range(len(byte_array) - 2):
        if byte_array[i:i+3] == bytes.fromhex('FFFFFF'):
            markers.append(i)
    return markers


def extract_glyphs_from_markers(byte_array, markers):
    """
    Extract 10-byte glyphs using FFFF FF markers as references.
    
    Protocol structure: glyph (10 bytes) + padding (3 bytes) + FFFF FF marker
    So glyph is at: marker_pos - 13 to marker_pos - 3
    """
    glyphs = []
    
    for marker_pos in markers:
        glyph_start = marker_pos - 13
        
        # Validate we have enough data
        if glyph_start < 0 or glyph_start + 10 > len(byte_array):
            continue
        
        glyph_bytes = list(byte_array[glyph_start:glyph_start + 10])
        glyphs.append(glyph_bytes)
    
    return glyphs


def visualize_glyph(glyph_bytes, width=8):
    """Generate ASCII art visualization of a 10-row glyph."""
    lines = []
    for byte_val in glyph_bytes:
        bits = format(byte_val, '08b')
        visual = ''.join('█' if bit == '1' else '·' for bit in bits)
        lines.append(f"{visual} ({byte_val:02X})")
    return lines


def generate_python_code(char_map, width=6):
    """Generate Python code for VERIFIED_GLYPHS dictionary."""
    lines = [
        "# Extracted from Bluetooth sniff (corrected alignment)",
        "",
    ]
    
    for char, glyph_bytes in sorted(char_map.items()):
        hex_list = ', '.join(f'0x{b:02X}' for b in glyph_bytes)
        lines.append(f"    '{char}': ({width}, [{hex_list}]),")
    
    return '\n'.join(lines)


def main():
    print("\n" + "=" * 80)
    print("BLUETOOTH SNIFF DATA EXTRACTOR - Cusong 7px Font")
    print("=" * 80)
    print()
    
    # Step 1: Get raw sniff data
    print("Step 1: Paste the raw Bluetooth sniff data")
    print("-" * 80)
    print("(Paste the hex data, then press Enter twice when done)")
    print()
    
    raw_data = []
    try:
        while True:
            line = input()
            if not line:
                if raw_data:
                    break
            else:
                raw_data.append(line)
    except EOFError:
        pass
    
    if not raw_data:
        print("Error: No data provided")
        return False
    
    raw_hex = '\n'.join(raw_data)
    print()
    
    # Step 2: Get the text string
    print("Step 2: What text was displayed on the device?")
    print("-" * 80)
    text_string = input("Enter the text (e.g., '1234567890'): ").strip()
    
    if not text_string:
        print("Error: No text provided")
        return False
    
    print()
    
    # Step 3: Clean and parse data
    print("=" * 80)
    print("PROCESSING DATA")
    print("=" * 80)
    print()
    
    cleaned_hex = clean_hex_data(raw_hex)
    print(f"Cleaned hex length: {len(cleaned_hex)} characters ({len(cleaned_hex)//2} bytes)")
    
    byte_array = hex_to_bytes(cleaned_hex)
    if byte_array is None:
        return False
    
    # Step 4: Find markers
    markers = find_character_markers(byte_array)
    print(f"Found {len(markers)} FFFF FF markers at offsets: {markers}")
    print()
    
    # Step 5: Extract glyphs
    glyphs = extract_glyphs_from_markers(byte_array, markers)
    print(f"Extracted {len(glyphs)} glyphs")
    print()
    
    # Step 6: Map to characters
    print("=" * 80)
    print("CHARACTER MAPPING")
    print("=" * 80)
    print()
    
    char_map = {}
    
    for idx, char in enumerate(text_string):
        if idx < len(glyphs):
            char_map[char] = glyphs[idx]
            print(f"Character '{char}' (index {idx}):")
            print(f"  Hex: {' '.join(f'{b:02X}' for b in glyphs[idx])}")
            print(f"  Visual preview:")
            for line in visualize_glyph(glyphs[idx]):
                print(f"    {line}")
            print()
    
    # Check for duplicates
    unique_chars = len(set(text_string))
    extracted_chars = len(char_map)
    
    if unique_chars < extracted_chars:
        print(f"Note: Found {extracted_chars} glyphs for {unique_chars} unique characters")
        print("(Some characters may have multiple variants)")
        print()
    
    # Step 7: Generate code
    print("=" * 80)
    print("PYTHON CODE FOR build_cusong_from_sniff.py")
    print("=" * 80)
    print()
    
    python_code = generate_python_code(char_map)
    print(python_code)
    print()
    
    # Step 8: Save to file
    print("=" * 80)
    print("SAVE RESULTS")
    print("=" * 80)
    print()
    
    save = input("Save extracted glyphs to file? (y/n): ").strip().lower()
    
    if save == 'y':
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"sniff_extract_{timestamp}.py"
        
        with open(filename, 'w') as f:
            f.write("# Extracted Cusong 7px glyphs from Bluetooth sniff\n")
            f.write(f"# Text: '{text_string}'\n")
            f.write(f"# Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Add these to VERIFIED_GLYPHS in build_cusong_from_sniff.py\n\n")
            f.write(python_code)
        
        print(f"✓ Saved to: {filename}")
        print()
    
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("1. Review the extracted glyphs above")
    print("2. Copy the Python code and add it to VERIFIED_GLYPHS in:")
    print("   scripts/build_cusong_from_sniff.py")
    print("3. Run: python3 scripts/build_cusong_from_sniff.py")
    print("4. Compile and test: platformio run --environment esp32s3dev")
    print()
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
