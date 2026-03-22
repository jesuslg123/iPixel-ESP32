#include "iPixelBleClient.h"
#include "iPixelCommands.h"

namespace iPixelBLE {

bool Client::initialized = false;

Client::Client(const String& macAddress)
    : device(NimBLEAddress(macAddress.c_str(), 0)) {}

Client::Client(const NimBLEAddress& address)
    : device(address) {}

void Client::init(const String& bleName) {
    if (initialized) return;
    NimBLEDevice::init(bleName.c_str());
    initialized = true;
}

bool Client::connect() {
    if (!initialized) {
        init();
    }
    device.connectAsync();
    return device.connected;
}

void Client::disconnect() {
    if (device.client) {
        device.client->disconnect();
    }
    device.connected = false;
}

void Client::loop() {
    if (autoReconnect && !device.connected) {
        connect();
        return;
    }

    if (device.connected) {
        device.queueTick();
    }
}

void Client::setAutoReconnect(bool enabled) {
    autoReconnect = enabled;
}

bool Client::isConnected() const {
    return device.connected;
}

size_t Client::queuedCommands() const {
    return device.queue.size();
}

String Client::mac() const {
    return device.address.toString().c_str();
}

void Client::queueRaw(const std::vector<uint8_t>& command) {
    device.queuePush(command);
}

void Client::setTime(int hour, int minute, int second) {
    device.queuePush(iPixelCommands::setTime(hour, minute, second));
}

void Client::setFunMode(bool value) {
    device.queuePush(iPixelCommands::setFunMode(value));
}

void Client::setOrientation(int orientation) {
    device.queuePush(iPixelCommands::setOrientation(orientation));
}

void Client::clear() {
    device.queuePush(iPixelCommands::clear());
}

void Client::setBrightness(int brightness) {
    device.queuePush(iPixelCommands::setBrightness(brightness));
}

void Client::setSpeed(int speed) {
    device.queuePush(iPixelCommands::setSpeed(speed));
}

void Client::setLED(bool on) {
    device.queuePush(iPixelCommands::setLED(on));
}

void Client::deleteScreen(int screen) {
    device.queuePush(iPixelCommands::deleteScreen(screen));
}

void Client::setPixel(int x, int y, uint8_t r, uint8_t g, uint8_t b) {
    device.queuePush(iPixelCommands::setPixel(x, y, r, g, b));
}

void Client::setClockMode(int style, int dayOfWeek, int year, int month, int day, bool showDate, bool format24) {
    device.queuePush(iPixelCommands::setClockMode(style, dayOfWeek, year, month, day, showDate, format24));
}

void Client::setRhythmLevelMode(int style, const int levels[11]) {
    device.queuePush(iPixelCommands::setRhythmLevelMode(style, levels));
}

void Client::setRhythmAnimationMode(int style, int frameNumber) {
    device.queuePush(iPixelCommands::setRhythmAnimationMode(style, frameNumber));
}

void Client::sendText(const String& text, int animation, int saveSlot, int speed, uint8_t colorR, uint8_t colorG, uint8_t colorB, int rainbowMode, int matrixHeight, int fontHeight) {
    device.queuePush(iPixelCommands::sendText(text, animation, saveSlot, speed, colorR, colorG, colorB, rainbowMode, matrixHeight, fontHeight));
}

void Client::sendPNG(const std::vector<uint8_t>& pngData) {
    device.queuePush(iPixelCommands::sendPNG(pngData));
}

void Client::sendGIF(const std::vector<uint8_t>& gifData) {
    device.queuePush(iPixelCommands::sendGIF(gifData));
}

}
