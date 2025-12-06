#!/usr/bin/env python3
"""
iPixel Font Converter
Converts TTF/OTF fonts to C++ FontChar struct format for iPixel LED displays.

Usage:
    python font_converter.py --input PixeloidSans.ttf --height 10 --output include/Font.h

Requirements:
    pip install pillow fonttools
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Tuple, List, Optional
import struct

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: PIL (Pillow) is required. Install with: pip install pillow")
    sys.exit(1)


class FontChar:
    """Represents a single character's bitmap data."""
    
    def __init__(self, char: str, width: int, height: int, bitmap: List[int]):
        self.char = char
        self.width = width
        self.height = height
        self.bitmap = bitmap  # List of uint16_t values (one per row)
    
    def __repr__(self) -> str:
        return f"FontChar('{self.char}', {self.width}x{self.height})"


class FontConverter:
    """Converts TTF fonts to iPixel C++ format."""
    
    # Standard character sets
    CHARSET_BASIC = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789"
        " .,!?;:'-\"()[]{}/@#$%&*+=_~"
    )
    
    CHARSET_EXTENDED = CHARSET_BASIC + "àáäâèéëêìíïîòóöôùúüûçñ°€£¥©®™"
    
    def __init__(self, font_path: str, height: int, charset: str = CHARSET_BASIC):
        """
        Initialize font converter.
        
        Args:
            font_path: Path to TTF/OTF font file
            height: Target font height in pixels
            charset: Characters to extract
        """
        self.font_path = Path(font_path)
        self.target_height = height
        self.charset = charset
        self.font = None
        self.characters: Dict[str, FontChar] = {}
        self.char_width = 0  # Will be calculated
        
        if not self.font_path.exists():
            raise FileNotFoundError(f"Font file not found: {font_path}")
        
        self._load_font()
    
    def _load_font(self):
        """Load the TTF font."""
        try:
            # Try to load font at target height
            self.font = ImageFont.truetype(str(self.font_path), self.target_height)
            print(f"✓ Loaded font: {self.font_path.name} at {self.target_height}px")
        except Exception as e:
            raise RuntimeError(f"Failed to load font: {e}")
    
    def _char_to_bitmap(self, char: str) -> Tuple[int, List[int]]:
        """
        Convert a single character to bitmap format.
        
        Args:
            char: Character to convert
        
        Returns:
            Tuple of (width, list of uint16_t bitmap rows)
        """
        # Create a temporary image to measure character
        temp_img = Image.new('L', (1, 1), 0)
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), char, font=self.font)
        char_width = bbox[2] - bbox[0]
        
        if char_width == 0:
            # Handle space or other invisible characters
            char_width = self.target_height // 2
        
        # Create image for the character
        img_height = self.target_height
        padding = 2
        img_width = max(char_width + padding * 2, 16)  # Minimum 16 bits
        
        img = Image.new('L', (img_width, img_height), 0)
        draw = ImageDraw.Draw(img)
        
        # Draw character
        draw.text((padding, 0), char, font=self.font, fill=255)
        
        # Convert to bitmap (list of uint16_t, one per row)
        bitmap = []
        pixels = img.load()
        
        for y in range(img_height):
            row_value = 0
            for x in range(min(16, img_width)):  # Maximum 16 bits per row
                if pixels[x, y] > 128:  # Threshold
                    row_value |= (1 << (15 - x))  # MSB first
            bitmap.append(row_value)
        
        # Trim width to actual content
        max_x = 0
        for y in range(img_height):
            for x in range(img_width - 1, -1, -1):
                if pixels[x, y] > 128:
                    max_x = max(max_x, x + 1)
                    break
        
        actual_width = min(max_x, 16)  # Cap at 16 pixels
        if actual_width == 0:
            actual_width = 1
        
        return actual_width, bitmap
    
    def convert(self, verbose: bool = False) -> Dict[str, FontChar]:
        """
        Convert all characters in charset to FontChar objects.
        
        Args:
            verbose: Print progress for each character
        
        Returns:
            Dictionary of char -> FontChar
        """
        self.characters = {}
        
        print(f"\n📝 Converting {len(self.charset)} characters at {self.target_height}px...")
        
        for i, char in enumerate(self.charset):
            try:
                width, bitmap = self._char_to_bitmap(char)
                font_char = FontChar(char, width, self.target_height, bitmap)
                self.characters[char] = font_char
                
                if verbose:
                    print(f"  [{i+1:3d}] '{char}' -> {width}px width")
            except Exception as e:
                print(f"  ⚠️  Skipped '{char}': {e}")
        
        print(f"✓ Converted {len(self.characters)} characters")
        return self.characters
    
    def preview(self, chars: Optional[str] = None, max_width: int = 80):
        """
        Display ASCII art preview of characters.
        
        Args:
            chars: Specific characters to preview (default: first 10)
            max_width: Terminal width for wrapping
        """
        if chars is None:
            chars = "HELLO"
        
        print(f"\n🎨 Preview ({self.target_height}px):")
        print("-" * max_width)
        
        for char in chars:
            if char not in self.characters:
                print(f"  '{char}': NOT FOUND")
                continue
            
            font_char = self.characters[char]
            print(f"\n  '{char}' (width={font_char.width}):")
            
            for row_value in font_char.bitmap:
                line = ""
                for bit in range(15, -1, -1):
                    if row_value & (1 << bit):
                        line += "██"
                    else:
                        line += "  "
                print(f"    {line}")
    
    def generate_cpp_code(self, font_name: str = "CUSTOM", 
                         namespace: str = "") -> str:
        """
        Generate C++ code for FontChar map.
        
        Args:
            font_name: Name for the font constant (e.g., "VCR_OSD_MONO_10PX")
            namespace: Optional C++ namespace
        
        Returns:
            C++ code as string
        """
        if not self.characters:
            raise ValueError("No characters converted. Call convert() first.")
        
        lines = []
        
        # Header comment
        lines.append("// AUTO-GENERATED: Font converter script")
        lines.append(f"// Font: {self.font_path.name}")
        lines.append(f"// Height: {self.target_height}px")
        lines.append(f"// Character count: {len(self.characters)}")
        lines.append("// DO NOT EDIT MANUALLY")
        lines.append("")
        
        if namespace:
            lines.append(f"namespace {namespace} {{")
            lines.append("")
        
        # Font constant definition
        const_name = f"FONT_{font_name}"
        lines.append(f"const std::map<char, FontChar> {const_name} = {{")
        
        # Generate each character
        char_list = sorted(self.characters.keys())
        for idx, char in enumerate(char_list):
            font_char = self.characters[char]
            
            # Escape special characters
            if char == "'":
                escaped_char = "\\'"
            elif char == "\\":
                escaped_char = "\\\\"
            elif char == "\n":
                escaped_char = "\\n"
            elif char == "\t":
                escaped_char = "\\t"
            else:
                escaped_char = char
            
            lines.append(f"    {{'{escaped_char}', FontChar{{")
            lines.append(f"        .width = {font_char.width},")
            
            # Generate bitmap data
            lines.append("        .data = {")
            
            for row_idx, row_value in enumerate(font_char.bitmap):
                hex_str = f"0x{row_value:04X}"
                if row_idx < len(font_char.bitmap) - 1:
                    lines.append(f"            {hex_str},")
                else:
                    lines.append(f"            {hex_str}")
            
            lines.append("        }")
            
            # Add comma to struct end (except for last character)
            if idx < len(char_list) - 1:
                lines.append("    }),")
            else:
                lines.append("    })")
        
        lines.append("};")
        
        if namespace:
            lines.append("")
            lines.append(f"}}  // namespace {namespace}")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def stats(self) -> Dict:
        """Get conversion statistics."""
        if not self.characters:
            return {}
        
        widths = [c.width for c in self.characters.values()]
        
        return {
            "total_characters": len(self.characters),
            "font_height": self.target_height,
            "min_width": min(widths),
            "max_width": max(widths),
            "avg_width": sum(widths) / len(widths),
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert TTF/OTF fonts to iPixel C++ FontChar format"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input font file (TTF/OTF)"
    )
    parser.add_argument(
        "--height",
        type=int,
        required=True,
        help="Target font height in pixels (e.g., 10, 16, 24)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output C++ header file (default: print to stdout)"
    )
    parser.add_argument(
        "--font-name", "-n",
        default="PIXELOID_SANS",
        help="Font constant name (default: PIXELOID_SANS)"
    )
    parser.add_argument(
        "--preview", "-p",
        default="HELLO iPixel",
        help="Preview text (default: 'HELLO iPixel')"
    )
    parser.add_argument(
        "--charset",
        choices=["basic", "extended"],
        default="basic",
        help="Character set to include (default: basic)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Select character set
    charset = FontConverter.CHARSET_EXTENDED if args.charset == "extended" else FontConverter.CHARSET_BASIC
    
    try:
        # Convert font
        converter = FontConverter(args.input, args.height, charset)
        converter.convert(verbose=args.verbose)
        
        # Show statistics
        stats = converter.stats()
        print(f"\n📊 Statistics:")
        print(f"  Font height: {stats['font_height']}px")
        print(f"  Character width: {stats['min_width']}-{stats['max_width']}px (avg: {stats['avg_width']:.1f})")
        print(f"  Total characters: {stats['total_characters']}")
        
        # Show preview
        converter.preview(args.preview)
        
        # Generate code
        cpp_code = converter.generate_cpp_code(
            font_name=args.font_name,
            namespace=""
        )
        
        # Output
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(cpp_code)
            print(f"\n✓ Generated: {output_path}")
        else:
            print("\n--- Generated C++ Code ---")
            print(cpp_code)
    
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
