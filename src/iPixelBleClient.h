#pragma once

#include <Arduino.h>
#include <NimBLEDevice.h>
#include <vector>
#include "iPixelDevice.h"

namespace iPixelBLE {

class Client {
public:
    explicit Client(const String& macAddress);
    explicit Client(const NimBLEAddress& address);

    static void init(const String& bleName = "ESP32");

    bool connect();
    void disconnect();
    void loop();

    void setAutoReconnect(bool enabled);

    bool isConnected() const;
    size_t queuedCommands() const;
    String mac() const;

    void queueRaw(const std::vector<uint8_t>& command);

    void setTime(int hour, int minute, int second);
    void setFunMode(bool value);
    void setOrientation(int orientation);
    void clear();
    void setBrightness(int brightness);
    void setSpeed(int speed);
    void setLED(bool on);
    void deleteScreen(int screen);
    void setPixel(int x, int y, uint8_t r, uint8_t g, uint8_t b);
    void setClockMode(int style, int dayOfWeek, int year, int month, int day, bool showDate, bool format24);
    void setRhythmLevelMode(int style, const int levels[11]);
    void setRhythmAnimationMode(int style, int frameNumber);
    void sendText(const String& text, int animation, int saveSlot, int speed, uint8_t colorR, uint8_t colorG, uint8_t colorB, int rainbowMode, int matrixHeight, int fontHeight = 16);
    void sendPNG(const std::vector<uint8_t>& pngData);
    void sendGIF(const std::vector<uint8_t>& gifData);

private:
    iPixelDevice device;
    bool autoReconnect = true;

    static bool initialized;
};

}
