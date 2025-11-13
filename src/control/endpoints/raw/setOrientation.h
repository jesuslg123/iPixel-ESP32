#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setOrientation("/control/raw/setOrientation", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long orientation = getParamLong(request, "orientation");
    device->queuePush(iPixelCommands::setOrientation(orientation));
    request->send(200, "text/plain", "OK");
});