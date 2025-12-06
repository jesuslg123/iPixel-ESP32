#include "iPixelCommands.h"

namespace iPixelCommands {

    bool checkRange(const char* name, int value, int minVal, int maxVal) {
        if (value < minVal || value > maxVal) {
            Serial.print("EXCEPTION: ");
            Serial.print(name);
            Serial.print(" out of range (");
            Serial.print(minVal);
            Serial.print("-");
            Serial.print(maxVal);
            Serial.print("), got ");
            Serial.println(value);
            throw std::invalid_argument(std::string(name) + " out of range (" + std::to_string(minVal) + "-" + std::to_string(maxVal) + ") got " + std::to_string(value));
            return false;
        }
        return true;
    }

    std::vector<uint8_t> setTime(int hour, int minute, int second) {
        checkRange("Hour", hour, 0, 23);
        checkRange("Minute", minute, 0, 59);
        checkRange("Second", second, 0, 59);

        std::vector<uint8_t> frame(8);
        frame[0] = 0x08;
        frame[1] = 0x00;
        frame[2] = 0x01;
        frame[3] = 0x80;
        frame[4] = (uint8_t)hour;
        frame[5] = (uint8_t)minute;
        frame[6] = (uint8_t)second;
        frame[7] = 0x00;

        return frame;
    }

    std::vector<uint8_t> setFunMode(bool value) {
        std::vector<uint8_t> frame(5);
        frame[0] = 0x05;
        frame[1] = 0x00;
        frame[2] = 0x04;
        frame[3] = 0x01;
        frame[4] = value ? 0x01 : 0x00;

        return frame;
    }
        
    std::vector<uint8_t> setOrientation(int orientation) {
        checkRange("Orientation", orientation, 0, 2);

        std::vector<uint8_t> frame(5);
        frame[0] = 0x05;
        frame[1] = 0x00;
        frame[2] = 0x06;
        frame[3] = 0x80;
        frame[4] = (uint8_t)orientation;

        return frame;
    }

    std::vector<uint8_t> clear() {
        std::vector<uint8_t> frame(4);
        frame[0] = 0x04;
        frame[1] = 0x00;
        frame[2] = 0x03;
        frame[3] = 0x80;

        return frame;
    }

    std::vector<uint8_t> setBrightness(int brightness) {
        checkRange("Brightness", brightness, 0, 100);

        std::vector<uint8_t> frame(5);
        frame[0] = 0x05;
        frame[1] = 0x00;
        frame[2] = 0x04;
        frame[3] = 0x80;
        frame[4] = (uint8_t)brightness;

        return frame;
    }

    std::vector<uint8_t> setSpeed(int speed) {
        checkRange("Speed", speed, 0, 100);

        std::vector<uint8_t> frame(4);
        frame[0] = 0x05;
        frame[1] = 0x00;
        frame[2] = 0x03;
        frame[3] = (uint8_t)speed;

        return frame;
    }

    std::vector<uint8_t> setLED(boolean on) {
        std::vector<uint8_t> frame(5);
        frame[0] = 0x05;
        frame[1] = 0x00;
        frame[2] = 0x07;
        frame[3] = 0x01;
        frame[4] = on ? 0x01 : 0x00;

        return frame;
    }

    std::vector<uint8_t> deleteScreen(int screen) {
        checkRange("Screen", screen, 0, 10);

        std::vector<uint8_t> frame(6);
        frame[0] = 0x07;
        frame[1] = 0x00;
        frame[2] = 0x02;
        frame[3] = 0x01;
        frame[4] = 0x00;
        frame[5] = (uint8_t)screen;

        return frame;
    }

    std::vector<uint8_t> setPixel(int x, int y, uint8_t r, uint8_t g, uint8_t b) {
        checkRange("X", x, 0, 255);
        checkRange("Y", y, 0, 255);
        checkRange("R", r, 0, 255);
        checkRange("G", g, 0, 255);
        checkRange("B", b, 0, 255);

        std::vector<uint8_t> frame(10);
        frame[0] = 0x0A;
        frame[1] = 0x00;
        frame[2] = 0x05;
        frame[3] = 0x01;
        frame[4] = 0x00;
        frame[5] = r;
        frame[6] = g;
        frame[7] = b;
        frame[8] = (uint8_t)x;
        frame[9] = (uint8_t)y;

        return frame;
    }

    std::vector<uint8_t> setClockMode(int style, int dayOfWeek, int year, int month, int day, bool showDate, bool format24) {
        checkRange("Style", style, 1, 8);
        checkRange("Day of Week", dayOfWeek, 1, 7);
        checkRange("Year", year, 0, 99);
        checkRange("Month", month, 1, 12);
        checkRange("Day", day, 1, 31);

        std::vector<uint8_t> frame(11);
        frame[0] = 0x0B;
        frame[1] = 0x00;
        frame[2] = 0x06;
        frame[3] = 0x01;
        frame[4] = (uint8_t)style;
        frame[5] = format24 ? 0x01 : 0x00;
        frame[6] = showDate ? 0x01 : 0x00;
        frame[7] = (uint8_t)year;
        frame[8] = (uint8_t)month;
        frame[9] = (uint8_t)day;
        frame[10] = (uint8_t)dayOfWeek;

        return frame;
    }

    std::vector<uint8_t> setRhythmLevelMode(int style, const int levels[11]) {
        checkRange("Style", style, 0, 4);
        for (int i = 0; i < 11; i++) checkRange("Level", levels[i], 0, 15);

        std::vector<uint8_t> frame(5 + 11);
        frame[0] = 0x10;
        frame[1] = 0x00; 
        frame[2] = 0x01;
        frame[3] = 0x02;
        frame[4] = (uint8_t)style;
        for (int i = 0; i < 11; i++)
            frame[5 + i] = (uint8_t)levels[i];

        return frame;
    }

    std::vector<uint8_t> setRhythmAnimationMode(int style, int frameNumber) {
        checkRange("Style", style, 0, 1);
        checkRange("Frame", frameNumber, 0, 7);

        std::vector<uint8_t> frame(6);
        frame[0] = 0x06;
        frame[1] = 0x00;
        frame[2] = 0x00;
        frame[3] = 0x02;
        frame[4] = (uint8_t)frameNumber;
        frame[5] = (uint8_t)style;

        return frame;
    }

    struct SelectedFont {
        const std::map<char, FontChar>* map;
        int height;
        bool isCompact = false;  // Flag for compact font
    };

    SelectedFont selectFont(int font_height) {
        switch (font_height) {
            case 7: {
                SelectedFont sf;
                sf.map = nullptr;
                sf.height = 7;
                sf.isCompact = true;
                return sf;
            }
            case 10: {
                SelectedFont sf;
                sf.map = &FONT_PIXELOID_SANS_10PX;
                sf.height = 10;
                sf.isCompact = false;
                return sf;
            }
            case 16: {
                SelectedFont sf;
                sf.map = &FONT_PIXELOID_SANS_16PX;
                sf.height = 16;
                sf.isCompact = false;
                return sf;
            }
            default:
                throw std::invalid_argument("Unsupported font height: " + std::to_string(font_height));
        }
    }

    std::vector<uint8_t> encodeTextCompact(const String& text, int font_height, uint8_t r, uint8_t g, uint8_t b) {
        (void)r; (void)g; (void)b; (void)font_height; (void)text; // Color is not encoded per-character for Cusong payload

        // FORCE HARDCODED "Hello" glyphs from official sniff for ALL text (testing only!)
        Serial.print("encodeTextCompact called with text: '");
        Serial.print(text);
        Serial.print("' (length: ");
        Serial.print(text.length());
        Serial.println(")");
        Serial.println("FORCING HARDCODED HELLO GLYPHS FOR TESTING!");
        
        std::vector<uint8_t> frame = {
            // H
            0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00,
            0x63, 0x63, 0x63, 0x63, 0x7F, 0x63, 0x63, 0x63, 0x63, 0x63,
            0x00, 0x00, 0x00, 0x00,  // trailing zeros (4 bytes)
            // e
            0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x7F, 0x03, 0x63, 0x3E,
            0x00, 0x00, 0x00, 0x00,  // trailing zeros (4 bytes)
            // l
            0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00,
            0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x38,
            0x00, 0x00, 0x00, 0x00,  // trailing zeros (4 bytes)
            // l
            0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00,
            0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x38,
            0x00, 0x00, 0x00, 0x00,  // trailing zeros (4 bytes)
            // o
            0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x3E, 0x63, 0x63, 0x63, 0x63, 0x63, 0x3E,
            0x00, 0x00, 0x00,  // trailing zeros (4 bytes)
        };
        return frame;
    }

    std::vector<uint8_t> encodeText(const String& text, const std::map<char, FontChar>& font, int font_height, uint8_t r, uint8_t g, uint8_t b) {
        std::vector<uint8_t> frame;
        uint8_t height_byte = (uint8_t)font_height;

        for (char character : text) {
            auto it = font.find(character);
            if (it == font.end()) continue;

            const FontChar& fontChar = it->second;
            int rows = std::min((int)fontChar.data.size(), font_height);
            std::vector<uint8_t> char_bytes;

            // Convert each 16-bit line to bytes
            for (int row = 0; row < rows; row++) {
                uint16_t line_data = fontChar.data[row];
                char_bytes.push_back((uint8_t)((line_data >> 8) & 0xFF));
                char_bytes.push_back((uint8_t)(line_data & 0xFF));
            }

            // Apply original transformations
            char_bytes = Helpers::invertFrames(char_bytes);
            char_bytes = Helpers::switchEndian(char_bytes);
            char_bytes = Helpers::logicReverseBitsOrder(char_bytes);

            uint8_t char_width_byte = (uint8_t)fontChar.width;

            if (!char_bytes.empty()) {
                // "80" = use per-character color
                frame.push_back(0x80);
                frame.push_back(r);
                frame.push_back(g);
                frame.push_back(b);
                frame.push_back(char_width_byte);
                frame.push_back(height_byte);
                frame.insert(frame.end(), char_bytes.begin(), char_bytes.end());
            }
        }

        return frame;
    }

    std::vector<uint8_t> sendText(const String& text, int animation, int save_slot, int speed, uint8_t r, uint8_t g, uint8_t b, int rainbow_mode, int matrix_height, int font_height) {
        checkRange("Text Length", text.length(), 1, 100);
        checkRange("Animation", animation, 0, 7);
        checkRange("Save Slot", save_slot, 1, 10);
        checkRange("Speed", speed, 0, 100);
        checkRange("colorR", r, 0, 255);
        checkRange("colorG", g, 0, 255);
        checkRange("colorB", b, 0, 255);
        checkRange("rainbow_mode", rainbow_mode, 0, 9);
        checkRange("matrix_height", matrix_height, 0, 255);
        checkRange("font_height", font_height, 0, 255);

        // Choose font and validate it fits the matrix
        SelectedFont selectedFont = selectFont(font_height);
        if (matrix_height < selectedFont.height) {
            throw std::invalid_argument("Font height exceeds matrix height");
        }

        // --- Validation ---
        if (text.length() == 0 || text.length() > 100) return {};
        if (animation == 3 || animation == 4) return {};

        // --- Header calculation ---
        const uint16_t HEADER_1_MG = 0x1D;
        const uint16_t HEADER_3_MG = 0x0E;
        uint16_t header_gap = 0x06 + selectedFont.height * 0x02;

        uint16_t header_1_val = HEADER_1_MG + text.length() * header_gap;
        uint16_t header_3_val = HEADER_3_MG + text.length() * header_gap;

        std::vector<uint8_t> header;

        auto appendHeader16 = [&header](uint16_t val) {
            std::vector<uint8_t> temp = { 
                (uint8_t)((val >> 8) & 0xFF),
                (uint8_t)(val & 0xFF)
            };
            auto switched = Helpers::switchEndian(temp);
            header.insert(header.end(), switched.begin(), switched.end());
        };

        appendHeader16(header_1_val); //Byte 1-2
        header.push_back(0x00); //Byte 3
        header.push_back(0x01); //Byte 4
        header.push_back(0x00); //Byte 5
        appendHeader16(header_3_val); //Byte 6-7
        header.push_back(0x00); //Byte 8
        header.push_back(0x00); //Byte 9

        // --- Save slot ---
        // HARDCODED: Match official sniff bytes after CRC: 00 17 followed by character count
        // std::vector<uint8_t> save_slot_bytes = { 0x00, 0x17, (uint8_t)(text.length()) };
        std::vector<uint8_t> save_slot_bytes = { 0x00, 0x17 };

        // --- Payload ---
        std::vector<uint8_t> payload;
        payload.push_back((uint8_t)(text.length()));
        payload.push_back(0x00); 
        payload.push_back(0x01); 
        payload.push_back(0x01); // fixed prefix

        payload.push_back((uint8_t)(animation));
        payload.push_back((uint8_t)(speed));
        payload.push_back((uint8_t)(rainbow_mode));

        // Append separator: FF FF FF 01 00 00 00 (matches official sniff)
        payload.push_back(0xFF);
        payload.push_back(0xFF); 
        payload.push_back(0xFF);
        payload.push_back(0x01); 
        payload.push_back(0x00); 
        payload.push_back(0x00);
        payload.push_back(0x00); 
        payload.push_back(0x00); //This should be part of the next character, not hardcoded here!

        // Append encoded characters
        std::vector<uint8_t> chars_bytes;
        if (selectedFont.isCompact) {
            chars_bytes = encodeTextCompact(text, selectedFont.height, r, g, b);
        } else {
            chars_bytes = encodeText(text, *selectedFont.map, selectedFont.height, r, g, b);
        }
        payload.insert(payload.end(), chars_bytes.begin(), chars_bytes.end());

        std::vector<uint8_t> crc_bytes = Helpers::calculateCRC32Bytes(payload); //Byte 10-13

        // --- Assemble final message ---
        std::vector<uint8_t> result;
        result.insert(result.end(), header.begin(), header.end());
        result.insert(result.end(), crc_bytes.begin(), crc_bytes.end());
        result.insert(result.end(), save_slot_bytes.begin(), save_slot_bytes.end());
        result.insert(result.end(), payload.begin(), payload.end());

        return result;
    }

    std::vector<uint8_t> sendPNG(const std::vector<uint8_t> &pngData) {
        std::vector<uint8_t> checksum = Helpers::calculateCRC32Bytes(pngData);
        std::vector<uint8_t> pngSize = Helpers::getFrameSize(pngData, 4);

        std::vector<uint8_t> result;
        result.insert(result.end(), { 0xFF, 0xFF }); //Placeholder for Frame Size
        result.insert(result.end(), { 0x02, 0x00, 0x00 }); //Prefix
        result.insert(result.end(), pngSize.begin(), pngSize.end()); //PNG Size
        result.insert(result.end(), checksum.begin(), checksum.end()); //Checksum
        result.insert(result.end(), { 0x00, 0x65 }); //Mid
        result.insert(result.end(), pngData.begin(), pngData.end()); //Data

        //Replace Placeholder for Frame Size
        std::vector<uint8_t> frameSize = Helpers::getFrameSize(result, 2);
        result[0] = frameSize[0];
        result[1] = frameSize[1];
        
        return result;
    }

    std::vector<uint8_t> sendGIF(const std::vector<uint8_t> &gifData) {
        std::vector<uint8_t> checksum = Helpers::calculateCRC32Bytes(gifData);
        std::vector<uint8_t> pngSize = Helpers::getFrameSize(gifData, 4);

        std::vector<uint8_t> result;
        result.insert(result.end(), { 0xFF, 0xFF }); //Placeholder for Frame Size
        result.insert(result.end(), { 0x03, 0x00, 0x00 }); //Prefix
        result.insert(result.end(), pngSize.begin(), pngSize.end()); //PNG Size
        result.insert(result.end(), checksum.begin(), checksum.end()); //Checksum
        result.insert(result.end(), { 0x02, 0x01 }); //Mid
        result.insert(result.end(), gifData.begin(), gifData.end()); //Data

        //Replace Placeholder for Frame Size
        std::vector<uint8_t> frameSize = Helpers::getFrameSize(result, 2);
        result[0] = frameSize[0];
        result[1] = frameSize[1];
        
        return result;
    }

}