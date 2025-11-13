#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_deleteScreen("/control/raw/deleteScreen", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long screen = getParamLong(request, "screen");
    device->queuePush(iPixelCommands::deleteScreen(screen));
    request->send(200, "text/plain", "OK");
});