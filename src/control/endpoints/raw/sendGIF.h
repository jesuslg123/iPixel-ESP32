#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_sendGIF("/control/raw/sendGIF", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    std::vector<uint8_t> data = getParamHex(request, "data");
    device->queuePush(iPixelCommands::sendGIF(data));
    request->send(200, "text/plain", "OK");
});