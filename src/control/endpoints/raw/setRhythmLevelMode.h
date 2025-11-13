#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setRhythmLevelMode("/control/raw/setRhythmLevelMode", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long style = getParamLong(request, "style");
    int levels[11];
    for (int i = 0; i < 11; ++i)
        levels[i] = getParamLong(request, "l" + char(char('0') + i));
    device->queuePush(iPixelCommands::setRhythmLevelMode(
        style,
        levels
    ));
    request->send(200, "text/plain", "OK");
});