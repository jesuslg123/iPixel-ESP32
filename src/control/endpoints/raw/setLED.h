#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setLED("/control/raw/setLED", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    bool led = getParamBool(request, "led");
    device->queuePush(iPixelCommands::setLED(led));
    request->send(200, "text/plain", "OK");
});