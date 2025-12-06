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
    # Remove ALL whitespace (spaces, tabs, newlines, carriage returns) - beginning, middle, end
    cleaned = re.sub(r'\s+', '', raw_input)
    # Remove any remaining non-hex characters
    cleaned = re.sub(r'[^0-9A-Fa-f]', '', cleaned)
    # Convert to uppercase for consistency
    return cleaned.upper()


def hex_to_bytes(hex_string):
    """Convert hex string to byte array."""
    try:
        return bytes.fromhex(hex_string)
    except ValueError as e:
        print(f"Error: Invalid hex data - {e}")
        return None


def remove_header_from_hex(hex_string):
    """
    Remove Bluetooth header and payload settings from hex string.
    Header: 15 bytes = 30 hex characters
    Settings: 14 bytes = 28 hex characters
    Total to remove: 29 bytes = 58 hex characters
    
    Returns: Clean payload hex string
    """
    header_size = 15 * 2  # 15 bytes = 30 hex chars
    settings_size = 14 * 2  # 14 bytes = 28 hex chars
    total_remove = header_size + settings_size  # 58 hex chars
    
    if len(hex_string) <= total_remove:
        print(f"Error: Hex string too short ({len(hex_string)} chars). Need at least {total_remove + 1} chars.")
        return None
    
    # Remove first 58 hex characters
    payload_hex = hex_string[total_remove:]
    return payload_hex


def split_hex_into_chunks(hex_string, chunk_size_bytes=20):
    """
    Split hex string into chunks.
    Each chunk represents one character (20 bytes = 40 hex characters).
    
    Returns: List of hex string chunks
    """
    chunk_size_hex = chunk_size_bytes * 2  # 20 bytes = 40 hex chars
    chunks = []
    
    for i in range(0, len(hex_string), chunk_size_hex):
        chunk = hex_string[i:i + chunk_size_hex]
        
        # Only add complete chunks
        if len(chunk) == chunk_size_hex:
            chunks.append(chunk)
        elif len(chunk) > 0:
            print(f"Warning: Incomplete chunk at end ({len(chunk)} hex chars), skipping.")
    
    return chunks


def extract_glyph_from_hex_chunk(hex_chunk):
    """
    Extract 10-byte glyph from 20-byte hex chunk.
    Remove first 7 bytes (14 hex chars) and last 3 bytes (6 hex chars).
    Keep middle 10 bytes (20 hex chars).
    
    Structure: [14 hex header] + [20 hex glyph] + [6 hex trailer] = 40 hex chars
    Returns: 20-character hex string (10 bytes)
    """
    if len(hex_chunk) != 40:
        print(f"Warning: Expected 40 hex chars, got {len(hex_chunk)}.")
        return None
    
    # Skip first 14 hex chars (7 bytes), take next 20 hex chars (10 bytes)
    header_size = 7 * 2  # 7 bytes = 14 hex chars
    glyph_size = 10 * 2  # 10 bytes = 20 hex chars
    
    glyph_hex = hex_chunk[header_size:header_size + glyph_size]
    
    return glyph_hex


def hex_string_to_byte_list(hex_string):
    """
    Convert hex string to list of byte values.
    "6E33" -> [0x6E, 0x33]
    """
    byte_list = []
    for i in range(0, len(hex_string), 2):
        byte_hex = hex_string[i:i+2]
        byte_value = int(byte_hex, 16)
        byte_list.append(byte_value)
    return byte_list





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
    print()
    
    # Step 4: Remove header and settings from hex string
    payload_hex = remove_header_from_hex(cleaned_hex)
    if payload_hex is None:
        return False
    
    print(f"Payload length: {len(payload_hex)} hex chars ({len(payload_hex)//2} bytes)")
    print(f"Clean payload (hex): {payload_hex[:100]}..." if len(payload_hex) > 100 else f"Clean payload (hex): {payload_hex}")
    print()
    
    # Step 5: Split into character chunks (40 hex chars = 20 bytes each)
    character_chunks = split_hex_into_chunks(payload_hex, chunk_size_bytes=20)
    print(f"Found {len(character_chunks)} character chunks (40 hex chars = 20 bytes each)")
    print()
    
    # Debug: Show first chunk
    if character_chunks:
        print("DEBUG: First chunk (40 hex chars = 20 bytes):")
        print(f"  Hex: {character_chunks[0]}")
        print()
    
    # Step 6: Extract glyphs from chunks
    glyphs = []
    for i, hex_chunk in enumerate(character_chunks):
        glyph_hex = extract_glyph_from_hex_chunk(hex_chunk)
        if glyph_hex:
            # Convert hex string to byte list for final output
            glyph_bytes = hex_string_to_byte_list(glyph_hex)
            glyphs.append(glyph_bytes)
            
            # Debug: Show first glyph extraction
            if i == 0:
                header_hex = hex_chunk[:14]
                trailer_hex = hex_chunk[34:]
                print("DEBUG: First glyph extraction:")
                print(f"  Full chunk (40 chars): {hex_chunk}")
                print(f"  Header (14 chars):     {header_hex}")
                print(f"  Glyph (20 chars):      {glyph_hex}")
                print(f"  Trailer (6 chars):     {trailer_hex}")
                print(f"  Glyph as bytes:        {' '.join(f'{b:02X}' for b in glyph_bytes)}")
                print()
    
    print(f"Extracted {len(glyphs)} clean glyphs (10 bytes each)")
    print()
    
    # Step 7: Map to characters
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
