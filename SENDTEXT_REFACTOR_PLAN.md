# SendText Refactor Plan: Multi-Resolution Support

## Executive Summary

The `sendText` feature currently works only for 96×16 displays because:
- The font is hardcoded to **16 pixels height**
- Header calculations assume 16px font height
- No support for variable-height fonts or screen dimensions
- Character encoding assumes 16 rows per character (32 bytes after bit transformations)

**Target Goal:** Enable `sendText` for 32×64 displays (20px screen height, 10px text height) and future resolutions while maintaining backward compatibility with existing 16px font.

---

## Current Implementation Analysis

### Font System

**File:** [include/Font.h](include/Font.h)

**Current State:**
- Single font variant: `FONT_VCR_OSD_MONO_16PX`
- Font structure:
  ```cpp
  struct FontChar {
      int width;                    // ~9 pixels per character
      std::vector<uint16_t> data;   // HARDCODED to 16 elements (16 rows)
  };
  ```
- All characters: 9px width × 16px height
- **Problem:** No way to scale or adapt font for different screen heights

### SendText Encoding Pipeline

**Files:**
- [src/iPixelCommands.cpp](src/iPixelCommands.cpp) — Main `sendText()` function (lines 171-300+)
- [src/iPixelCommands.h](src/iPixelCommands.h) — Function declarations
- [src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h) — HTTP endpoint
- [src/bluetooth/endpoints/pairings/sendText.h](src/bluetooth/endpoints/pairings/sendText.h) — BLE endpoint (if exists)

**Current Function Signature:**
```cpp
std::vector<uint8_t> sendText(
    const String& text,
    int animation,
    int save_slot,
    int speed,
    uint8_t r,
    uint8_t g,
    uint8_t b,
    int rainbow_mode,
    int matrix_height  // Screen height in pixels
)
```

**Encoding Process (Simplified):**
1. Look up each character in `FONT_VCR_OSD_MONO_16PX`
2. Convert font data: 16 uint16_t values → 32 bytes (2 bytes per row)
3. Apply transformations: `SwapFrames()` → `ReverseBytes()` → `ReverseBits()`
4. Build character payload:
   - `0x80` (color marker)
   - R, G, B (3 bytes)
   - Width = 9 (1 byte)
   - **matrix_height** (1 byte) — User-provided screen height
   - Character bitmap (32 bytes = 16 rows × 2 bytes)

**Total:** 38 bytes per character

### Header Calculation

**File:** [src/iPixelCommands.cpp](src/iPixelCommands.cpp) (lines ~255-270)

```cpp
const uint16_t HEADER_1_MG = 0x1D;
const uint16_t HEADER_3_MG = 0x0E;

// CRITICAL: Uses matrix_height, not actual font height
uint16_t header_gap = 0x06 + matrix_height * 0x02;

uint16_t header_1_val = HEADER_1_MG + text.length() * header_gap;
uint16_t header_3_val = HEADER_3_MG + text.length() * header_gap;

// Header: [val1_LB] [val1_HB] 0x00 0x01 0x00 [val3_LB] [val3_HB] 0x00 0x00
```

**Problem:** Header gap scales with `matrix_height` (screen height), not actual font height. Protocol expects this to reflect the font dimensions, not the display canvas size.

---

## Root Cause: Why It Fails for 20px Screens

### The Mismatch

| Aspect | 16px Display | 20px Display |
|--------|-------------|--------------|
| **Font Height** | 16px (fixed) | 10px (official app) |
| **Screen Height** | 16px | 20px |
| **matrix_height param** | 16 | 20 |
| **Header Gap Calc** | `0x06 + 16*0x02 = 0x26` | `0x06 + 20*0x02 = 0x32` |
| **Expected Header Gap** | Should be 16-based | **Should be 10-based = 0x1A** |

### Consequences

1. **Wrong header values** are sent to device (scaled for 20px instead of 10px)
2. **Device expects different payload structure** than what's being sent
3. **Character bitmap mismatch:** Font is always 16 rows, but header says different
4. Device either:
   - Rejects the message (wrong frame size)
   - Displays corrupted text (reads extra bytes as data)
   - Shows oversized/distorted characters

---

## Proposed Solution: Font-Aware Architecture

### Phase 1: Create Font Variants

**Goal:** Define fonts for target resolutions

**Create:** `FONT_VCR_OSD_MONO_10PX` variant
- Character width: ~6-7 pixels (scaled down from 9px)
- Character height: **10 pixels** (10 uint16_t rows instead of 16)
- All alphanumeric + common punctuation
- **Location:** [include/Font.h](include/Font.h) — Add alongside existing 16px font

**Future Variants (for expandability):**
- `FONT_VCR_OSD_MONO_8PX` — For very compact displays
- `FONT_VCR_OSD_MONO_24PX` — For larger displays
- Custom fonts registered in a `FontRegistry`

### Phase 2: Refactor sendText Function

**Current Signature Issue:**
```cpp
std::vector<uint8_t> sendText(..., int matrix_height)
```

The function receives only screen height, not font selection.

**Proposed New Signature:**
```cpp
std::vector<uint8_t> sendText(
    const String& text,
    int animation,
    int save_slot,
    int speed,
    uint8_t r,
    uint8_t g,
    uint8_t b,
    int rainbow_mode,
    int matrix_height,      // Screen height (e.g., 16, 20, 32)
    int font_height = 16    // NEW: Font variant (8, 10, 16, 24...)
)
```

**Alternative: Auto-detect approach**
```cpp
// Use a FontRegistry to auto-select best font for screen height
// Pro: Simpler API
// Con: Less explicit, requires hardcoded rules
```

**Recommendation:** Explicit parameter approach for clarity and future flexibility

### Phase 3: Update Encoding Logic

**File:** [src/iPixelCommands.cpp](src/iPixelCommands.cpp)

**Changes Required:**

1. **Font Selection**
   - Map `font_height` parameter to correct font variant
   - Validate combination of `matrix_height` and `font_height`
   - Return error if invalid (e.g., 10px font on 8px screen)

2. **Dynamic Row Iteration**
   ```cpp
   // OLD (hardcoded):
   for (int row = 0; row < 16; row++) { ... }
   
   // NEW (dynamic):
   int actual_font_height = getSelectedFontHeight(font_height);
   for (int row = 0; row < actual_font_height; row++) { ... }
   ```

3. **Header Gap Calculation**
   ```cpp
   // OLD (wrong for multi-font):
   uint16_t header_gap = 0x06 + matrix_height * 0x02;
   
   // NEW (correct):
   uint16_t header_gap = 0x06 + actual_font_height * 0x02;
   ```

4. **Character Encoding**
   - Loop over actual font rows (8, 10, 16, etc.) instead of hardcoded 16
   - Adjust character payload size accordingly:
     - 10px font: 20 bytes per character (10 rows × 2 bytes)
     - 16px font: 32 bytes per character (16 rows × 2 bytes)

### Phase 4: Update HTTP & BLE Endpoints

**Files:**
- [src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h)
- [src/bluetooth/endpoints/pairings/sendText.h](src/bluetooth/endpoints/pairings/sendText.h) (if exists)

**Changes:**
- Add `font_height` query parameter to HTTP endpoint
- Add validation with error responses
- Pass parameter to `sendText()` function
- Document new parameter in endpoint description

**Example HTTP Request:**
```
/control/raw/sendText?text=Hello&animation=0&font_height=10&matrix_height=20
```

### Phase 5: Backward Compatibility

**Strategy:** Default parameter approach

```cpp
// Old code still works:
sendText(text, anim, slot, speed, r, g, b, mode, 16);  // Uses default font_height=16

// New code can specify:
sendText(text, anim, slot, speed, r, g, b, mode, 20, 10);  // Explicit 10px font
```

**HTTP Endpoint:**
```
// Backward compatible (defaults to 16px):
/control/raw/sendText?text=Hello&matrix_height=16

// With font specification:
/control/raw/sendText?text=Hello&matrix_height=20&font_height=10
```

---

## Implementation Checklist

### 1. Font Creation
- [ ] Design or extract 10px font variant from official app
- [ ] Add `FONT_VCR_OSD_MONO_10PX` to [include/Font.h](include/Font.h)
- [ ] Verify character coverage (A-Z, a-z, 0-9, punctuation, emojis)
- [ ] Test font character alignment and spacing

### 2. Core Function Refactoring
- [ ] Add `font_height` parameter to [src/iPixelCommands.cpp](src/iPixelCommands.cpp) `sendText()` declaration
- [ ] Create font selection logic (map height to font variant)
- [ ] Update character encoding loop to use dynamic font height
- [ ] Fix header gap calculation to use font height, not matrix height
- [ ] Update character bitmap encoding (variable bytes based on font)

### 3. Endpoint Updates
- [ ] Update [src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h) to accept `font_height` parameter
- [ ] Add parameter validation
- [ ] Update HTTP query parameter parsing
- [ ] Check for BLE endpoint updates needed

### 4. Testing & Validation
- [ ] Test with 96×16 display + 16px font (backward compatibility)
- [ ] Test with 32×64 display + 10px font (new target)
- [ ] Test header calculations for both scenarios
- [ ] Verify payload byte counts match protocol expectations
- [ ] Test edge cases: 1-char, max-length text, special characters

### 5. Documentation
- [ ] Update [README.md](README.md) with font support information
- [ ] Update [README_API.md](README_API.md) with new endpoint parameters
- [ ] Add examples for both 16px and 10px fonts

---

## Technical Details: Header Calculation Deep Dive

### Protocol Header Structure (from iPixel_PROTOCOL.md)

```
[Header: 9 bytes] [CRC32: 4 bytes] [SaveSlot: 2 bytes] [Payload: variable]

Header format:
[val1_LB] [val1_HB] 0x00 0x01 0x00 [val3_LB] [val3_HB] 0x00 0x00

Where:
  val1 = 0x1D + (text_length * header_gap)
  val3 = 0x0E + (text_length * header_gap)
  header_gap = 0x06 + (actual_font_height * 0x02)
```

### Examples

**Scenario 1: 96×16 Display + 16px Font**
```
text_length = 5
actual_font_height = 16
header_gap = 0x06 + (16 * 0x02) = 0x06 + 0x20 = 0x26
val1 = 0x1D + (5 * 0x26) = 0x1D + 0xAE = 0xCB
val3 = 0x0E + (5 * 0x26) = 0x0E + 0xAE = 0xBC
```

**Scenario 2: 32×64 Display + 10px Font (CORRECT)**
```
text_length = 5
actual_font_height = 10
header_gap = 0x06 + (10 * 0x02) = 0x06 + 0x14 = 0x1A
val1 = 0x1D + (5 * 0x1A) = 0x1D + 0x7E = 0x9B
val3 = 0x0E + (5 * 0x1A) = 0x0E + 0x7E = 0x8C
```

**Current (WRONG) Implementation for 32×64:**
```
text_length = 5
matrix_height = 20  // Screen height, not font height
header_gap = 0x06 + (20 * 0x02) = 0x06 + 0x28 = 0x2E  // WRONG!
val1 = 0x1D + (5 * 0x2E) = 0x1D + 0xE6 = 0x103 (overflow!)
val3 = 0x0E + (5 * 0x2E) = 0x0E + 0xE6 = 0xF4
```

This mismatch causes the device to reject or misinterpret the message.

---

## Font Architecture Options

### Option A: Simple Lookup (Recommended for Phase 1)

```cpp
const FontChar* selectFont(int font_height) {
    switch(font_height) {
        case 10: return &FONT_VCR_OSD_MONO_10PX;
        case 16: return &FONT_VCR_OSD_MONO_16PX;
        default: return nullptr;  // Error
    }
}
```

**Pros:**
- Simple, straightforward
- Easy to understand and maintain
- Good for current use case

**Cons:**
- Not scalable for many fonts
- Switch statement becomes unwieldy

### Option B: FontRegistry (Recommended for Future)

```cpp
class FontRegistry {
    std::map<int, const FontChar*> fonts;
    
    void registerFont(int height, const FontChar* font);
    const FontChar* getFont(int height);
};
```

**Pros:**
- Scalable for future fonts
- Decoupled from hardcoded fonts
- Allows runtime font registration

**Cons:**
- More complex implementation
- Overkill for current scope

**Recommendation:** Use Option A for Phase 1, refactor to Option B if more fonts are added.

---

## Validation Rules

### Screen Height vs Font Height Compatibility

| Screen Height | Supported Fonts | Rationale |
|---|---|---|
| 8px | 8px (future) | Font must fit within screen |
| 10px | 8px, 10px | 10px font fits exactly, 8px with padding |
| 16px | 8px, 10px, 16px | Original target resolution |
| 20px | 10px, 16px, 20px (future) | Official app uses 10px for this |
| 24px | 8px, 10px, 16px, 24px (future) | Multiple options |
| 32px+ | All available | Plenty of space |

### Validation Logic (Pseudocode)

```cpp
bool isValidCombination(int matrix_height, int font_height) {
    // Font must be smaller than or equal to screen height
    if (font_height > matrix_height) return false;
    
    // Both must be valid values
    if (!isSupportedFontHeight(font_height)) return false;
    
    // Optional: Check for "official" combinations
    // if (!isOfficialCombination(matrix_height, font_height)) 
    //     log warning but allow
    
    return true;
}
```

---

## Risk Assessment

### Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Breaking existing clients | High | Use default parameter (backward compatible) |
| Wrong font selection | Medium | Clear validation errors in response |
| Incorrect header calculation | Critical | Unit tests for header calculation |
| Font data corruption | High | Verify font data matches protocol spec |
| Off-by-one in row iteration | High | Explicit loop bounds testing |

### Testing Strategy

1. **Unit Tests:**
   - Header calculation for 16px and 10px fonts
   - Font selection/validation
   - Character encoding byte count

2. **Integration Tests:**
   - Full message encoding with both fonts
   - CRC32 validation
   - Device communication tests

3. **Regression Tests:**
   - Existing 96×16 + 16px font flow unchanged
   - HTTP endpoint backward compatibility

---

## Future Enhancements

### Beyond Phase 1

1. **Variable Character Width**
   - Current: All characters 9px wide (16px font)
   - Future: Support proportional fonts
   - Enables more text per line

2. **Font Scaling**
   - Automatically scale 16px font to other sizes
   - Trade-off: Quality vs. simplicity
   - Use if custom font variants unavailable

3. **Multi-Color Text**
   - Current: Single color per message
   - Future: Per-character color support
   - Requires larger payload

4. **Font Registry Persistence**
   - Load custom fonts from SPIFFS
   - User-created fonts support
   - Advanced customization

5. **Text Alignment**
   - Center, left, right alignment
   - Requires header/payload adjustments

---

## Files to Modify

### Core Implementation
1. [include/Font.h](include/Font.h) — Add 10px font variant
2. [src/iPixelCommands.h](src/iPixelCommands.h) — Update function signature
3. [src/iPixelCommands.cpp](src/iPixelCommands.cpp) — Refactor encoding logic

### Endpoints
4. [src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h) — Add font_height parameter
5. [src/bluetooth/endpoints/pairings/sendText.h](src/bluetooth/endpoints/pairings/sendText.h) — If exists, update

### Documentation
6. [README.md](README.md) — Update with font information
7. [README_API.md](README_API.md) — Document new parameters
8. [iPixel_PROTOCOL.md](iPixel_PROTOCOL.md) — Update with multi-font section

---

## Implementation Timeline

### Phase 1 (Current Sprint): 32×64 Support
- [ ] Design/extract 10px font (2-3 hours)
- [ ] Refactor sendText function (3-4 hours)
- [ ] Update endpoints (1-2 hours)
- [ ] Testing & validation (2-3 hours)
- **Total: ~8-12 hours**

### Phase 2 (Future): Scalability
- [ ] Add 8px and 24px fonts (if needed)
- [ ] Implement FontRegistry
- [ ] Refactor for flexibility
- **Total: ~4-6 hours**

---

## Success Criteria

✅ sendText works on 32×64 displays with 10px font
✅ sendText still works on 96×16 displays with 16px font (backward compatible)
✅ Header calculations are correct for both scenarios
✅ API is intuitive and well-documented
✅ All tests pass (unit + integration)
✅ No breaking changes to existing clients

