#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setPixel("/control/raw/setPixel", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long x = getParamLong(request, "x");
    long y = getParamLong(request, "y");
    long r = getParamLong(request, "r");
    long g = getParamLong(request, "g");
    long b = getParamLong(request, "b");
    device->queuePush(iPixelCommands::setPixel(
        x,
        y,
        r,
        g,
        b
    ));
    request->send(200, "text/plain", "OK");
});