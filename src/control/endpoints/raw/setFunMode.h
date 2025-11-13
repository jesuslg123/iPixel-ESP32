#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setFunMode("/control/raw/setFunMode", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    bool funMode = getParamBool(request, "funMode");
    device->queuePush(iPixelCommands::setFunMode(funMode));
    request->send(200, "text/plain", "OK");
});