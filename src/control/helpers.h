#pragma once
#include "bluetooth/registry.h"
#include "webserver/Helpers.h"
#include "../Helpers.h"

BluetoothPairing* getBluetoothDevice(AsyncWebServerRequest* request, const char* name) {
    String device = getParamString(request, name);
    BluetoothPairing* dev = bluetoothPairings.find(device);
    if (!dev) throw std::invalid_argument("Device not found (please pair first)");
    if (!dev->_connected) throw std::invalid_argument("Device is (still) connecting");
    return dev;
}

std::vector<uint8_t> getParamHex(AsyncWebServerRequest* request, const char* name) {
    return Helpers::hexStringToVector(getParamString(request, name));
};