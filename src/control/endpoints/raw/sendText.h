#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_sendText("/control/raw/sendText", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    String text = getParamString(request, "text");
    long animation = getParamLong(request, "animation");
    long save_slot = getParamLong(request, "save_slot");
    long speed = getParamLong(request, "speed");
    long colorR = getParamLong(request, "colorR");
    long colorG = getParamLong(request, "colorG");
    long colorB = getParamLong(request, "colorB");
    long rainbow_mode = getParamLong(request, "rainbow_mode");
    long matrix_height = getParamLong(request, "matrix_height");
    device->queuePush(iPixelCommands::sendText(
        text,
        animation,
        save_slot,
        speed,
        colorR,
        colorG,
        colorB,
        rainbow_mode,
        matrix_height
    ));
    request->send(200, "text/plain", "OK");
});