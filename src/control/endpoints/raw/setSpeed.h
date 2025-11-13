#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setSpeed("/control/raw/setSpeed", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long speed = getParamLong(request, "speed");
    device->queuePush(iPixelCommands::setSpeed(speed));
    request->send(200, "text/plain", "OK");
});