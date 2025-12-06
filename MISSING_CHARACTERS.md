# Character Set for Cusong 7px Font

This document lists all characters needed for a complete Cusong 7px Compact font implementation.

## Currently Implemented Characters ✓

- **Space**: ` ` (space)
- **Numbers**: `0 1 2 3 4 5 6 7 8 9`
- **Uppercase**: `H`
- **Lowercase**: `e i l o p q r t u w y`

---

## Complete Character Set Needed

### Uppercase Letters (A-Z)
- ❌ A
- ❌ B
- ❌ C
- ❌ D
- ❌ E
- ❌ F
- ❌ G
- ✓ H (already implemented)
- ❌ I
- ❌ J
- ❌ K
- ❌ L
- ❌ M
- ❌ N
- ❌ O
- ❌ P
- ❌ Q
- ❌ R
- ❌ S
- ❌ T
- ❌ U
- ❌ V
- ❌ W
- ❌ X
- ❌ Y
- ❌ Z

### Lowercase Letters (a-z)
- ❌ a
- ❌ b
- ❌ c
- ❌ d
- ✓ e (already implemented)
- ❌ f
- ❌ g
- ❌ h
- ✓ i (already implemented)
- ❌ j
- ❌ k
- ✓ l (already implemented)
- ❌ m
- ❌ n
- ✓ o (already implemented)
- ✓ p (already implemented)
- ✓ q (already implemented)
- ✓ r (already implemented)
- ❌ s
- ✓ t (already implemented)
- ✓ u (already implemented)
- ❌ v
- ✓ w (already implemented)
- ❌ x
- ✓ y (already implemented)
- ❌ z

### Numbers (0-9)
- ✓ 0 (already implemented)
- ✓ 1 (already implemented)
- ✓ 2 (already implemented)
- ✓ 3 (already implemented)
- ✓ 4 (already implemented)
- ✓ 5 (already implemented)
- ✓ 6 (already implemented)
- ✓ 7 (already implemented)
- ✓ 8 (already implemented)
- ✓ 9 (already implemented)

### Common Symbols and Punctuation
- ❌ `!` (exclamation mark)
- ❌ `"` (quotation mark)
- ❌ `#` (hash/pound)
- ❌ `$` (dollar sign)
- ❌ `%` (percent)
- ❌ `&` (ampersand)
- ❌ `'` (apostrophe)
- ❌ `(` (left parenthesis)
- ❌ `)` (right parenthesis)
- ❌ `*` (asterisk)
- ❌ `+` (plus)
- ❌ `,` (comma)
- ❌ `-` (hyphen/minus)
- ❌ `.` (period/dot)
- ❌ `/` (forward slash)
- ❌ `:` (colon)
- ❌ `;` (semicolon)
- ❌ `<` (less than)
- ❌ `=` (equals)
- ❌ `>` (greater than)
- ❌ `?` (question mark)
- ❌ `@` (at sign)
- ❌ `[` (left bracket)
- ❌ `\` (backslash)
- ❌ `]` (right bracket)
- ❌ `^` (caret)
- ❌ `_` (underscore)
- ❌ `` ` `` (backtick)
- ❌ `{` (left brace)
- ❌ `|` (pipe/vertical bar)
- ❌ `}` (right brace)
- ❌ `~` (tilde)

---

## Summary Statistics

- **Total characters needed**: 95 (printable ASCII characters)
- **Currently implemented**: 23
- **Missing characters**: 72
  - Uppercase letters: 25
  - Lowercase letters: 15
  - Symbols/punctuation: 32

---

## Data Format

Each character should follow this format:

```cpp
{'X', 6, { 0x0000, 0xFF00, 0xFF00, 0xFF00, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0xXXXX, 0xXXXX, 0xXXXX, 0xXXXX, 0xXXXX, 0xXXXX, 0xXXXX, 0x0000, 0x0000, 0x0000 } },
```

Where:
- First parameter: ASCII character
- Second parameter: Character width (typically 5-6 pixels)
- Third parameter: 20 uint16_t values representing:
  - Bytes 0-6: Header `0x00, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00` (in uint16_t format)
  - Bytes 7-16: Glyph data (10 bytes for 7px height font)
  - Bytes 17-19: Trailer `0x00, 0x00, 0x00` (in uint16_t format)

---

## Priority Characters

For basic text functionality, prioritize generating these first:

1. **Uppercase letters A-Z** (25 missing - most commonly used in display text)
2. **Lowercase letters a-z** (15 missing - complete the alphabet)
3. **Basic punctuation**: `.`, `,`, `!`, `?`, `-`, `:`
4. **Common symbols**: `@`, `#`, `$`, `%`, `&`, `*`, `+`, `=`, `/`

---

## Total Progress

**23 / 95 characters implemented (24.2%)**

Characters to generate: 72

---

## Character Groups for Generation

Copy and paste these character groups into the official app to generate the font data packages:

### Group 1: Space + Numbers (Already Implemented - for re-generation)
```
 01234
```

### Group 2: Numbers + Uppercase H (Already Implemented - for re-generation)
```
56789H
```

### Group 3: Lowercase (Already Implemented - for re-generation)
```
eilopq
```

### Group 4: Lowercase + Symbols (Already Implemented - for re-generation)
```
rtuwy!
```

### Group 5: Symbols - Punctuation
```
"#$%&'
```

### Group 6: Symbols - Parentheses & Operators
```
()*+,-
```

### Group 7: Symbols - Period to Question
```
./:;<>
```

### Group 8: Symbols - Question to Uppercase E
```
?@ABCD
```

### Group 9: Uppercase E-J
```
EFGHIJ
```

### Group 10: Uppercase K-P
```
KLMNOP
```

### Group 11: Uppercase Q-V
```
QRSTUV
```

### Group 12: Uppercase W-Z & Brackets
```
WXYZ[\
```

### Group 13: Symbols & Lowercase a-d
```
]^_`ab
```

### Group 14: Lowercase c-h
```
cdefgh
```

### Group 15: Lowercase j-n
```
jkmnsv
```

### Group 16: Lowercase x-z & Symbols
```
xz{|}~
```

---

## Generation Instructions

1. Copy each group of characters (6 per group)
2. Paste into the official app's text field
3. Generate the font package/sniff data
4. Extract the character data from the Bluetooth sniff
5. Format it according to the data format specification above
6. Add to Font_CUSONG_7PX_COMPACT.h in ASCII order

**Note**: Groups 1-4 contain already implemented characters - regenerate these if you need consistent formatting or want to verify the existing data.

---

## Notes

- Characters must be added in **ASCII order** to maintain binary search compatibility
- Each character's glyph data is 20 uint16_t values (40 bytes total)
- The header (0x00, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00) is embedded in the first 7 bytes
- The trailer (0x00, 0x00, 0x00) is embedded in the last 3 bytes
