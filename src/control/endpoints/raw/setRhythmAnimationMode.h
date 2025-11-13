#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setRhythmAnimationMode("/control/raw/setRhythmAnimationMode", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long style = getParamLong(request, "style");
    long frame = getParamLong(request, "frame");
    device->queuePush(iPixelCommands::setRhythmAnimationMode(
        style,
        frame
    ));
    request->send(200, "text/plain", "OK");
});