#include "Helpers.h"

namespace Helpers {

    std::vector<uint8_t> switchEndian(const std::vector<uint8_t>& bytes) {
        std::vector<uint8_t> result(bytes.rbegin(), bytes.rend());
        return result;
    }

    uint16_t reverseBits16(uint16_t n) {
        n = ((n & 0xFF00) >> 8) | ((n & 0x00FF) << 8);
        n = ((n & 0xF0F0) >> 4) | ((n & 0x0F0F) << 4);
        n = ((n & 0xCCCC) >> 2) | ((n & 0x3333) << 2);
        n = ((n & 0xAAAA) >> 1) | ((n & 0x5555) << 1);
        return n;
    }

    std::vector<uint8_t> logicReverseBitsOrder(const std::vector<uint8_t>& data) {
        if (data.size() % 2 != 0)
            throw std::invalid_argument("Input size must be a multiple of 2 bytes.");

        std::vector<uint8_t> result;
        result.reserve(data.size());

        for (size_t i = 0; i < data.size(); i += 2) {
            uint16_t value = ((uint16_t)(data[i]) << 8) | data[i + 1];
            uint16_t reversed_value = reverseBits16(value);
            result.push_back((uint8_t)((reversed_value >> 8) & 0xFF));
            result.push_back((uint8_t)(reversed_value & 0xFF));
        }

        return result;
    }

    std::vector<uint8_t> invertFrames(const std::vector<uint8_t>& data) {
        if (data.size() % 2 != 0)
            throw std::invalid_argument("invertFrames: Input size must be multiple of 2 bytes.");

        std::vector<uint8_t> result;
        result.reserve(data.size());

        // Process in 2-byte frames (like original 4-char hex)
        for (int i = (int)(data.size()) - 2; i >= 0; i -= 2) {
            result.push_back(data[i]);
            result.push_back(data[i + 1]);
        }
        return result;
    }

    std::vector<uint8_t> calculateCRC32Bytes(const std::vector<uint8_t>& data) {
        uint32_t crc = crc32Update(data.data(), data.size(), CRC32_INITIAL);
        crc = crc32Final(crc);
        std::vector<uint8_t> crc_bytes = {
            (uint8_t)((crc >> 24) & 0xFF),
            (uint8_t)((crc >> 16) & 0xFF),
            (uint8_t)((crc >> 8) & 0xFF),
            (uint8_t)(crc & 0xFF)
        };
        return switchEndian(crc_bytes);
    }

    
    std::vector<uint8_t> getFrameSize(const std::vector<uint8_t>& data, size_t byteCount) {
        uint64_t length = data.size();  
        std::vector<uint8_t> result(byteCount, 0);
        for (size_t i = 0; i < byteCount; ++i)
            result[byteCount - 1 - i] = static_cast<uint8_t>((length >> (i * 8)) & 0xFF);
        return switchEndian(result);
    }

    std::vector<uint8_t> hexStringToVector(const String &hexString) {
        std::vector<uint8_t> result;
        int len = hexString.length();
        for (int i = 0; i < len; ) {
            // Skip any spaces
            while (i < len && hexString[i] == ' ') i++;
            if (i >= len) break;

            // Parse two hex characters
            char c1 = hexString[i++];
            if (i >= len) break;
            char c2 = hexString[i++];

            uint8_t byte = 0;

            // Convert first hex digit
            if (c1 >= '0' && c1 <= '9') byte = (c1 - '0') << 4;
            else if (c1 >= 'A' && c1 <= 'F') byte = (c1 - 'A' + 10) << 4;
            else if (c1 >= 'a' && c1 <= 'f') byte = (c1 - 'a' + 10) << 4;

            // Convert second hex digit
            if (c2 >= '0' && c2 <= '9') byte |= (c2 - '0');
            else if (c2 >= 'A' && c2 <= 'F') byte |= (c2 - 'A' + 10);
            else if (c2 >= 'a' && c2 <= 'f') byte |= (c2 - 'a' + 10);

            result.push_back(byte);
        }
        return result;
    }

    std::vector<uint8_t> encodeRGBAPixelsToPng(std::vector<uint8_t> framebuffer, uint8_t width, uint8_t height) {
        // Allocate PNGENC on heap to avoid stack overflow (object has large internal buffers)
        PNGENC* png = new PNGENC();
        
        // Calculate required buffer size (2x raw data - balance between safety and memory)
        // For 64x20 RGBA: 5,120 bytes raw -> 10,240 bytes buffer (typical PNG: 2-4 KB)
        size_t rawSize = width * height * 4;
        size_t maxBufferSize = rawSize * 2;  // 2x provides enough headroom without excessive memory
        std::vector<uint8_t> pngData(maxBufferSize);
        
        Serial.printf("[PNG] Encoding %dx%d RGBA (%zu bytes raw, %zu buffer)\n", 
                     width, height, rawSize, maxBufferSize);
        
        // Initialize encoder to RAM buffer
        int rc = png->open(pngData.data(), pngData.size());
        if (rc != PNG_SUCCESS) {
            Serial.printf("[PNG] ERROR: Encoder init failed, code: %d\n", rc);
            delete png;
            return {};
        }
        
        // Start encoding: RGBA (32-bit), 8-bit per channel, compression level 6 (balanced)
        // Reduced from level 9 to avoid excessive compression overhead
        rc = png->encodeBegin(width, height, PNG_PIXEL_TRUECOLOR_ALPHA, 8, NULL, 6);
        if (rc != PNG_SUCCESS) {
            Serial.printf("[PNG] ERROR: Encode begin failed, code: %d\n", rc);
            delete png;
            return {};
        }
        
        // Encode line by line (PNGenc requirement)
        size_t bytesPerLine = width * 4; // RGBA = 4 bytes per pixel
        for (int y = 0; y < height; y++) {
            uint8_t* lineStart = framebuffer.data() + (y * bytesPerLine);
            rc = png->addLine(lineStart);
            if (rc != PNG_SUCCESS) {
                Serial.printf("[PNG] ERROR: Line %d failed, code: %d\n", y, rc);
                delete png;
                return {};
            }
        }
        
        // Finalize encoding and get actual PNG size
        int finalSize = png->close();
        delete png;  // Free heap allocation
        
        if (finalSize <= 0) {
            Serial.printf("[PNG] ERROR: Finalize failed, size: %d\n", finalSize);
            return {};
        }
        
        Serial.printf("[PNG] Success! Encoded %d bytes (%.1f%% of raw)\n", 
                     finalSize, (finalSize * 100.0) / rawSize);
        
        // Resize vector to actual PNG data size
        pngData.resize(finalSize);
        return pngData;
    }

}