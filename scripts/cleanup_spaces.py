#!/usr/bin/env python3
"""
Script to parse raw_font_sniff.md and extract font data.
"""
import os
import re

def parse_raw_font_file(filepath):
    """
    Parse the raw_font_sniff.md file to extract character groups and their hex data.
    
    Returns:
        List of tuples (character_string, hex_data_string)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into blocks separated by blank lines
    blocks = re.split(r'\n\n+', content.strip())
    
    groups = []
    i = 0
    while i < len(blocks):
        block = blocks[i].strip()
        
        # Check if this block looks like a character string (short, non-hex)
        # Character strings should not contain "9500" or lots of hex patterns
        if block and not block.startswith('9500') and len(block) < 50:
            # This is likely a character string
            char_string = block
            
            # The next block should be the hex data
            if i + 1 < len(blocks):
                hex_block = blocks[i + 1].strip()
                groups.append((char_string, hex_block))
                i += 2  # Skip both blocks
                continue
        
        i += 1
    
    return groups

def clean_hex_data(hex_data):
    """
    Remove all spaces and newlines from hex data.
    """
    return hex_data.replace(' ', '').replace('\n', '').replace('\r', '')

def process_hex_data(cleaned_hex):
    """
    Process the cleaned hex data:
    1. Remove first 30 characters
    2. Remove first 28 characters from result
    3. Split into chunks of 40 characters
    """
    # Remove first 30 characters
    trimmed = cleaned_hex[30:]
    
    # Remove first 28 characters from trimmed
    final = trimmed[28:]
    
    # Split into chunks of 40 characters
    chunk_size = 40
    chunks = [final[i:i + chunk_size] for i in range(0, len(final), chunk_size)]
    
    return chunks

def format_font_entries(char_string, chunks):
    """
    Format each character with its corresponding chunk as a font entry.
    """
    formatted_entries = []
    
    for char, chunk in zip(char_string, chunks):
        if not chunk:
            continue
        
        # Ensure even-length hex string by padding a leading 0 if needed
        hex_body = chunk if len(chunk) % 2 == 0 else "0" + chunk
        
        # Convert every byte to a 16-bit word (byte << 8) with 0x prefix
        bytes_list = [hex_body[i:i + 2] for i in range(0, len(hex_body), 2)]
        words = [f"0x{b.upper()}00" for b in bytes_list]
        
        # Assemble the output line (width hardcoded to 6 like the example)
        line = f"{{'{char}', 6, {{ {', '.join(words)} }} }},"
        formatted_entries.append(line)
    
    return formatted_entries

def main():
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_font_file = os.path.join(script_dir, 'raw_font_sniff.md')
    
    if not os.path.exists(raw_font_file):
        print(f"Error: {raw_font_file} not found!")
        return
    
    print(f"Reading from: {raw_font_file}\n")
    
    # Parse the file
    groups = parse_raw_font_file(raw_font_file)
    
    print(f"Found {len(groups)} character groups\n")
    
    all_formatted_entries = []
    
    for idx, (char_string, hex_data) in enumerate(groups, 1):
        print(f"Group {idx}: '{char_string}'")
        
        # Clean the hex data
        cleaned = clean_hex_data(hex_data)
        print(f"  Cleaned hex length: {len(cleaned)}")
        
        # Process the hex data
        chunks = process_hex_data(cleaned)
        print(f"  Number of chunks: {len(chunks)}")
        print(f"  Characters to map: {len(char_string)}")
        
        # Format the entries
        formatted = format_font_entries(char_string, chunks)
        all_formatted_entries.extend(formatted)
        
        print(f"  Generated {len(formatted)} font entries")
        print()
    
    # Print all formatted entries
    print("\n" + "="*80)
    print("ALL FORMATTED FONT ENTRIES:")
    print("="*80 + "\n")
    
    for entry in all_formatted_entries:
        print(entry)
    
    print(f"\nTotal entries generated: {len(all_formatted_entries)}")

if __name__ == "__main__":
    main()
