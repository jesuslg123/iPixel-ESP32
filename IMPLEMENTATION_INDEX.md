# iPixel ESP32 - sendText Refactor & Font Conversion Index

This index documents all the work completed for enabling multi-resolution text display support on iPixel LED matrix screens.

## 📋 Problem Statement

The `sendText` feature only worked on 96×16 displays (16px text height) because:
- Font was hardcoded to 16px height
- Header calculation used screen height instead of actual font height
- No support for variable-height fonts
- Failed on 32×64 displays (20px screen, needs 10px text)

## 📚 Documentation Files (Read in This Order)

### 1. **SENDTEXT_REFACTOR_PLAN.md** ⭐ START HERE
**Purpose:** Comprehensive analysis and implementation roadmap

**Contains:**
- Root cause analysis (why it fails for 20px screens)
- Detailed comparison of current vs. expected header calculations
- 5-phase implementation plan with specific steps
- Risk assessment and success criteria
- Technical deep-dive into protocol specifications

**Key Sections:**
- Font System Analysis
- SendText Encoding Pipeline Overview
- Header Calculation Deep Dive
- Implementation Checklist
- Files to Modify

**When to Read:** Before starting any code changes

---

### 2. **FONT_CONVERSION_SUMMARY.md** 
**Purpose:** Font converter tool and generated font documentation

**Contains:**
- Font Converter script specifications
- Generated font specifications (10px and 16px)
- Font data format technical details
- Character bitmap encoding explanation
- Integration guidelines

**Key Sections:**
- Font Converter Features & Usage
- Generated Font Specifications
- Font Data Format Reference
- Comparison with Original VCR OSD Font
- Technical Notes on Rendering Algorithm

**When to Read:** When working with fonts or understanding bitmap format

---

### 3. **FONT_CONVERTER_QUICKSTART.md**
**Purpose:** Quick reference for using the font converter

**Contains:**
- Installation instructions
- Common usage patterns
- Examples for generating different sizes
- Troubleshooting guide

**When to Read:** When you need to regenerate or create new fonts

---

## 🛠️ Tool & Generated Assets

### Font Converter Tool

**File:** [scripts/font_converter.py](scripts/font_converter.py)

**Features:**
- Converts TTF/OTF fonts to iPixel C++ format
- Generates fonts at any pixel height
- Produces ASCII previews
- Provides character statistics
- Creates production-ready C++ code

**Usage:**
```bash
python3 scripts/font_converter.py \
  --input refactor/PixeloidSans.ttf \
  --height 10 \
  --output include/Font_PIXELOID_SANS_10PX.h
```

**Dependencies:** pillow, fonttools

---

### Generated Fonts

#### PixeloidSans 10px

**File:** [include/Font_PIXELOID_SANS_10PX.h](include/Font_PIXELOID_SANS_10PX.h)

- **Height:** 10 pixels
- **Characters:** 89 (A-Z, a-z, 0-9, symbols)
- **Size:** 24 KB
- **Use Case:** 32×64 displays (20px height, 10px text)
- **Format:** C++ std::map<char, FontChar>

#### PixeloidSans 16px

**File:** [include/Font_PIXELOID_SANS_16PX.h](include/Font_PIXELOID_SANS_16PX.h)

- **Height:** 16 pixels
- **Characters:** 89 (same charset)
- **Size:** 35 KB
- **Use Case:** 96×16 displays (16px height, backward compatibility)
- **Format:** C++ std::map<char, FontChar>

---

## 🔧 Implementation Roadmap

### Phase 1: Analysis (✅ COMPLETED)
- [x] Identified root cause of sendText failures
- [x] Analyzed current implementation
- [x] Created comprehensive refactor plan
- [x] Designed solution architecture

**Deliverables:**
- SENDTEXT_REFACTOR_PLAN.md

---

### Phase 2: Font Generation (✅ COMPLETED)
- [x] Created font converter tool
- [x] Generated 10px font variant (PixeloidSans)
- [x] Generated 16px font variant (PixeloidSans)
- [x] Verified font data integrity
- [x] Created documentation

**Deliverables:**
- scripts/font_converter.py
- include/Font_PIXELOID_SANS_10PX.h
- include/Font_PIXELOID_SANS_16PX.h
- FONT_CONVERSION_SUMMARY.md
- FONT_CONVERTER_QUICKSTART.md

---

### Phase 3: Code Refactoring (⏳ PENDING)
**Estimated:** 4-6 hours

**Tasks:**

1. **Update Font Registry** [include/Font.h](include/Font.h)
   - Include new font headers
   - Create font selection mechanism
   - Maintain backward compatibility

2. **Refactor sendText Function** [src/iPixelCommands.cpp](src/iPixelCommands.cpp)
   - Add `font_height` parameter
   - Implement font selection logic
   - Fix header gap calculation
   - Update character encoding loop
   - Add validation

3. **Update Endpoints**
   - [src/control/endpoints/raw/sendText.h](src/control/endpoints/raw/sendText.h)
   - [src/bluetooth/endpoints/pairings/sendText.h](src/bluetooth/endpoints/pairings/sendText.h)
   - Add font_height query/parameter
   - Update HTTP parsing

4. **Testing**
   - Unit tests for header calculation
   - Integration tests with both fonts
   - Hardware testing on 32×64 display

---

## 📊 Technical Reference

### Header Calculation Examples

**Scenario: 32×64 Display with 10px Font**
```
Current (WRONG):
header_gap = 0x06 + (20 * 0x02) = 0x2E

Fixed (CORRECT):
header_gap = 0x06 + (10 * 0x02) = 0x1A
```

### Font Data Structure

```cpp
struct FontChar {
    int width;                    // 1-16 pixels
    std::vector<uint16_t> data;   // One uint16_t per row
};

// 10px font example:
.data = {
    0x0000,  // Row 0
    0x0000,  // Row 1
    0x1800,  // Row 2
    // ... 7 more rows for 10px total
}
```

### Protocol Header Formula

```
val1 = 0x1D + (text_length * header_gap)
val3 = 0x0E + (text_length * header_gap)
header_gap = 0x06 + (font_height * 0x02)
```

---

## 🗂️ File Structure

### New Files Created
```
project/
├── scripts/
│   └── font_converter.py              # Font conversion tool
├── include/
│   ├── Font_PIXELOID_SANS_10PX.h     # 10px font
│   └── Font_PIXELOID_SANS_16PX.h     # 16px font
├── SENDTEXT_REFACTOR_PLAN.md          # Main refactor plan
├── FONT_CONVERSION_SUMMARY.md         # Font documentation
├── FONT_CONVERTER_QUICKSTART.md       # Font tool guide
└── IMPLEMENTATION_INDEX.md            # This file
```

### Files to Modify (Phase 3)
```
include/
└── Font.h                      # Add new fonts, font selection

src/
├── iPixelCommands.h            # Update function signature
├── iPixelCommands.cpp          # Refactor sendText logic
├── control/endpoints/raw/
│   └── sendText.h              # Add font_height parameter
└── bluetooth/endpoints/pairings/
    └── sendText.h              # Add font_height parameter
```

---

## 🎯 Success Criteria

- [x] sendText works on 96×16 displays (16px font) — backward compatible
- [ ] sendText works on 32×64 displays (10px font) — new target
- [ ] Header calculations are correct for both scenarios
- [ ] API is intuitive and well-documented
- [ ] All tests pass (unit + integration)
- [ ] Hardware testing successful
- [ ] No breaking changes to existing clients

---

## 🚀 Getting Started

### For Understanding the Problem
1. Read: [SENDTEXT_REFACTOR_PLAN.md](SENDTEXT_REFACTOR_PLAN.md)
2. Focus: "Root Cause: Why It Fails for 20px Screens" section
3. See: Header calculation examples

### For Working with Fonts
1. Read: [FONT_CONVERSION_SUMMARY.md](FONT_CONVERSION_SUMMARY.md)
2. Reference: [FONT_CONVERTER_QUICKSTART.md](FONT_CONVERTER_QUICKSTART.md)
3. Use: [scripts/font_converter.py](scripts/font_converter.py)

### For Code Implementation
1. Read: [SENDTEXT_REFACTOR_PLAN.md](SENDTEXT_REFACTOR_PLAN.md) - Phase 3 section
2. Start with: [include/Font.h](include/Font.h)
3. Follow: Implementation Checklist in refactor plan
4. Test after each phase

---

## 📞 Quick Reference

### Key Issues Fixed
| Issue | Root Cause | Solution |
|-------|-----------|----------|
| 32×64 sendText fails | Header uses screen height instead of font height | Use actual font height in calculation |
| Font incompatibility | Hardcoded 16px font | Support multiple font variants |
| No font selection | Single font hardcoded | Add font_height parameter |
| Oversized text | 16px font on small screens | Create 10px font variant |

### Key Files
| File | Purpose | Status |
|------|---------|--------|
| SENDTEXT_REFACTOR_PLAN.md | Implementation roadmap | ✅ Complete |
| scripts/font_converter.py | Font generation tool | ✅ Ready |
| Font_PIXELOID_SANS_10PX.h | 10px font variant | ✅ Ready |
| Font_PIXELOID_SANS_16PX.h | 16px font variant | ✅ Ready |
| iPixelCommands.cpp | sendText function | ⏳ Pending refactor |

---

## 📝 Notes

### Why PixeloidSans?
- Pixel-perfect font designed for LED displays
- Scalable (any size from single TTF)
- Compact (more characters per line)
- Modern aesthetic suitable for LED matrices

### Backward Compatibility
- All new features use optional parameters with sensible defaults
- Existing code continues to work without changes
- Original 16px font support maintained

### Future Expansion
Font converter tool supports generating:
- 8px fonts (very compact)
- 12px fonts (medium)
- 24px fonts (large displays)
- Custom fonts from any TTF/OTF

---

## 🤝 Contributing

When implementing Phase 3:
1. Follow the checklist in SENDTEXT_REFACTOR_PLAN.md
2. Test after each change
3. Verify backward compatibility
4. Document any API changes

---

**Last Updated:** December 6, 2025
**Status:** Phase 2 Complete, Phase 3 Pending
**Next Milestone:** Code refactoring and hardware testing
