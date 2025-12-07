#!/usr/bin/env python3
"""
Convert character literals to Unicode code points in Font_CUSONG_7PX_COMPACT.h
"""
import re
import os

def char_to_codepoint(char_str):
    """Convert a character string to its Unicode code point"""
    # Handle escape sequences
    if char_str == '\\\\':
        return ord('\\')
    elif char_str == "\\'":
        return ord("'")
    elif char_str == '\\"':
        return ord('"')
    elif len(char_str) == 1:
        return ord(char_str)
    else:
        # Multi-byte UTF-8 character
        return ord(char_str[0]) if char_str else 32

def convert_entry(line):
    """Convert a font entry line from character literal to code point"""
    # Match the character in the entry: {'X', 6, { ... }} or {X, 6, { ... }}
    # First try to match entries that already have numeric codepoints
    if re.match(r"\s*\{\d+,", line):
        return line  # Already converted
    
    # Match character literal format
    match = re.match(r"(\s*)\{['\"](.+?)['\"], (\d+), (\{.+\})\},?", line, re.DOTALL)
    if match:
        indent = match.group(1)
        char_str = match.group(2)
        width = match.group(3)
        data = match.group(4)
        
        # Get the code point
        codepoint = char_to_codepoint(char_str)
        
        # Reconstruct the line with code point
        return f"{indent}{{{codepoint}, {width}, {data}}},\n"
    
    return line

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
    
    print(f"Converting entries from line {array_start+1} to {array_end-1}")
    
    # Convert each entry
    converted_count = 0
    new_lines = lines[:array_start+1]
    
    for i in range(array_start + 1, array_end):
        line = lines[i]
        if line.strip().startswith('{'):
            new_line = convert_entry(line)
            new_lines.append(new_line)
            converted_count += 1
        else:
            new_lines.append(line)
    
    new_lines.append(lines[array_end])
    new_lines.extend(lines[array_end+1:])
    
    # Write back
    with open(font_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✓ Converted {converted_count} entries to code points")
    print(f"✓ Written to: {font_file}")

if __name__ == "__main__":
    main()
