#!/usr/bin/env python3
"""
Script to remove all spaces from input text.
"""
import sys

def main():
    print("Enter your text (press Ctrl+D when done):")
    
    # Read all input from stdin
    text = sys.stdin.read()
    
    # Process: Remove all spaces and newlines
    cleaned_text = text.replace(' ', '').replace('\n', '').replace('\r', '')
    
    # Print the cleaned text
    print("\nCleaned text:")
    print(cleaned_text)
    
    # Remove first 30 characters
    trimmed_text = cleaned_text[30:]
    
    # Print the trimmed text
    print("\nTrimmed text (first 30 chars removed):")
    print(trimmed_text)
    
    # Remove first 28 characters from trimmed text
    final_text = trimmed_text[28:]
    
    # Print the final text
    print("\nFinal text (first 28 chars removed from trimmed):")
    print(final_text)
    
    # Split final text into chunks of 40 characters
    chunk_size = 40
    chunks = [final_text[i:i + chunk_size] for i in range(0, len(final_text), chunk_size)]
    
    # Print the chunks
    print("\nChunks (40 characters each):")
    print(chunks)
    
    # Keep chunks intact (no trimming) so downstream steps see the full data
    cleaned_chunks = list(chunks)

    # Print the preserved chunks
    print("\nChunks preserved (no trimming):")
    print(cleaned_chunks)

    # Ask for a second string to link with chunks
    print("\nEnter the second string (one line) to map over chunks:")
    with open('/dev/tty', 'r') as tty:
        second_string = tty.readline().strip()

    # Create relation between each letter of second_string and each chunk in order
    relation = list(zip(second_string, cleaned_chunks))

    # Print the relation
    print("\nRelation (letter -> chunk):")
    print(relation)

    # Build formatted entries: map each letter to its chunk as font-style rows
    formatted_entries = []
    for letter, chunk in relation:
        if not chunk:
            continue

        # Ensure even-length hex string by padding a leading 0 if needed
        hex_body = chunk if len(chunk) % 2 == 0 else "0" + chunk

        # Convert every byte to a 16-bit word (byte << 8) with 0x prefix
        bytes_list = [hex_body[i:i + 2] for i in range(0, len(hex_body), 2)]
        words = [f"0x{b.upper()}00" for b in bytes_list]

        # Assemble the output line (width hardcoded to 6 like the example)
        line = f"{{'{letter}', 6, {{ {', '.join(words)} }} }},"
        formatted_entries.append(line)

    # Print formatted entries
    print("\nFormatted chunk entries:")
    for entry in formatted_entries:
        print(entry)


if __name__ == "__main__":
    main()
