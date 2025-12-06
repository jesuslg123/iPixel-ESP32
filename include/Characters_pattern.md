Here is a clean **README.md** you can drop directly into your project.
It documents the protocol, the bitmap format, encoding rules, and how to generate new characters.

---

# LED Font Encoding Format (20×8 Bitmap Glyphs)

This document describes the character format used by the 20×64 LED matrix driven over Bluetooth.
Each character is represented as a **20-row × 8-pixel** bitmap, encoded into an array of **20× `uint16_t`**, where only the **upper byte** of each row is used for pixel data.

Example character definition:

```c
{ 'A', 6, {
    0x0000, 0xFF00, 0xFF00, 0xFF00,
    0x0000, 0x0000, 0x0000,
    0x1C00, 0x3600, 0x6300, 0x6300,
    0x6300, 0x7F00, 0x6300, 0x6300,
    0x6300, 0x6300,
    0x0000, 0x0000, 0x0000
} },
```

---

# 1. Data Structure

Each glyph entry has the form:

```c
{ char character, uint8_t width, uint16_t rows[20] }
```

Where:

* **character** – ASCII char being represented (`'A'`, `'b'`, `'2'`, etc.)
* **width** – nominal character width (typically `6`)
* **rows[20]** – 20 vertical bitmap rows stored as 16-bit values

---

# 2. Row Encoding

Only the **upper 8 bits** of each row contain pixel data:

```
uint16_t row = pixel_bits << 8;
```

Thus:

| row value | pixel byte | bit pattern |
| --------: | ---------: | ----------- |
|  `0x3E00` |     `0x3E` | `00111110`  |
|  `0x6300` |     `0x63` | `01100011`  |
|  `0x7F00` |     `0x7F` | `01111111`  |
|  `0x0000` |     `0x00` | `00000000`  |

**Bit 7 = leftmost pixel**
**Bit 0 = rightmost pixel**

---

# 3. Fixed Header (Rows 0–3)

All characters begin with the following 4 rows:

| Row |    Value | Meaning        |
| --: | -------: | -------------- |
|   0 | `0x0000` | blank          |
|   1 | `0xFF00` | full-width bar |
|   2 | `0xFF00` | full-width bar |
|   3 | `0xFF00` | full-width bar |

This appears to be a **protocol requirement** or a **visual separator** at the top of the character cell.

---

# 4. Glyph Placement Rules

After row 3, glyph data begins.
Vertical placement depends on the type of character:

### Uppercase Letters (A–Z)

* Usually begin around **row 7**
* Height ~10 rows
  Example: `A`

```
Row 7: 0x1C00
Row 8: 0x3600
Row 9: 0x6300
…
```

### Lowercase Letters (a–z)

#### Without descender (a, c, e, h, n, o, u, etc.)

* Begin near **row 10**
* Height ~7 rows

#### With descender (g, j, p, q, y)

* Begin near **row 10**
* Extend down to row **17–18**

### Digits (0–9)

* Begin earlier, around **row 5**
* Typically tall (occupy most of vertical space)

Example (`2`):

```
Row 5: 0x3E00
Row 6: 0x7F00
Row 7: 0x6300
…
Row 19: 0x7F00
```

### Symbols

Symbol placement depends on shape and often mimics lowercase rules.

---

# 5. Building a Glyph Manually

To create a new character:

1. Design the glyph as an array of **8-bit row pixels**, e.g.:

```c
uint8_t glyph_C[] = {
    0b00111110,
    0b01100011,
    0b01100000,
    0b01100000,
    0b01100000,
    0b01100011,
    0b00111110
};
int glyph_height = 7;
```

2. Choose a vertical starting row

   * uppercase → 7
   * lowercase → 10
   * digits → 5
   * descenders → 10 (but extend downward)

3. Convert to the encoded 20-row format:

```c
uint16_t rows[20] = {0};

// header
rows[1] = rows[2] = rows[3] = 0xFF00;

// glyph rows
for(int i = 0; i < glyph_height; i++) {
    rows[start_row + i] = ((uint16_t)glyph_C[i]) << 8;
}
```

4. Wrap in the font entry:

```c
{ 'C', 6, { rows[0], rows[1], ..., rows[19] } },
```

---

# 6. Interpreting Rows Visually (for debugging)

To print/debug characters:

```c
void debug_print(uint16_t rows[20]) {
    for (int y = 0; y < 20; ++y) {
        uint8_t b = rows[y] >> 8;
        for (int x = 7; x >= 0; --x) {
            putchar((b & (1 << x)) ? '#' : '.');
        }
        putchar('\n');
    }
}
```

This displays the glyph in text form.

---

# 7. Summary of the Pattern

* **20 rows total per character**
* **8 pixels wide**, encoded in the top byte of each `uint16_t`
* **Rows 1–3 always 0xFF00** (top bar)
* **Rows below contain the glyph**, positioned depending on character class
* Descenders extend to rows 17–18
* Lowercase glyphs are shorter and placed lower
* Digits are tall and begin near row 5
* Unused rows are filled with `0x0000`

This format makes it easy to generate, modify, or import font glyphs programmatically.

---

If you want, I can also generate:

✅ A **Python script** that auto-converts standard bitmap fonts into this format
✅ A **full library** of all ASCII characters already encoded for your LED screen
Just tell me!
