#!/usr/bin/env python3
"""
Sort font entries in Font_CUSONG_7PX_COMPACT.h by ASCII order
"""
import re
import os

def get_ascii_value(entry):
    """Extract the ASCII value of the character from a font entry line"""
    # Try to match standard format: {'X', 6, { ... }}
    match = re.search(r"\{'(.)', ", entry)
    if match:
        char = match.group(1)
        # Handle escape sequences
        if char == '\\':
            return ord('\\')
        elif char == "'":
            return ord("'")
        elif char == '"':
            return ord('"')
        return ord(char)
    
    # Handle special UTF-8 characters
    match = re.search(r"\{'(.*?)', ", entry)
    if match:
        char_str = match.group(1)
        if len(char_str) == 1:
            return ord(char_str)
        # Handle multi-byte characters
        if len(char_str) > 0:
            return ord(char_str[0])
    
    return 999  # fallback for unparseable entries

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_file = os.path.join(script_dir, '..', 'include', 'Font_CUSONG_7PX_COMPACT.h')
    
    # Read the file
    with open(font_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find where the array starts and ends
    array_start = -1
    array_end = -1
    for i, line in enumerate(lines):
        if 'static const CompactFontChar CUSONG_7PX_DATA[] PROGMEM = {' in line:
            array_start = i
        elif array_start != -1 and '};' in line:
            array_end = i
            break
    
    if array_start == -1 or array_end == -1:
        print("Error: Could not find array boundaries!")
        return
    
    # Extract all font entries
    entries = []
    for i in range(array_start + 1, array_end):
        line = lines[i]
        if line.strip().startswith('{'):
            entries.append(line)
    
    print(f"Found {len(entries)} font entries")
    
    # Sort entries by ASCII value
    sorted_entries = sorted(entries, key=get_ascii_value)
    
    # Show first and last few entries for verification
    print("\nFirst 5 entries:")
    for entry in sorted_entries[:5]:
        ascii_val = get_ascii_value(entry)
        match = re.search(r"\{'(.*?)', ", entry)
        char = match.group(1) if match else '?'
        print(f"  ASCII {ascii_val:3d}: '{char}'")
    
    print("\nLast 5 entries:")
    for entry in sorted_entries[-5:]:
        ascii_val = get_ascii_value(entry)
        match = re.search(r"\{'(.*?)', ", entry)
        char = match.group(1) if match else '?'
        print(f"  ASCII {ascii_val:3d}: '{char}'")
    
    # Rebuild the file
    new_lines = lines[:array_start+1]
    new_lines.extend(sorted_entries)
    new_lines.append(lines[array_end])
    new_lines.extend(lines[array_end+1:])
    
    # Write back
    with open(font_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✓ File sorted by ASCII order")
    print(f"✓ Written to: {font_file}")

if __name__ == "__main__":
    main()
