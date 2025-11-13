#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setBrightness("/control/raw/setBrightness", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long brightness = getParamLong(request, "brightness");
    device->queuePush(iPixelCommands::setBrightness(brightness));
    request->send(200, "text/plain", "OK");
});