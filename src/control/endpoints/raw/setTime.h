#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setTime("/control/raw/setTime", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long hour = getParamLong(request, "hour");
    long minute = getParamLong(request, "minute");
    long second = getParamLong(request, "second");
    device->queuePush(iPixelCommands::setTime(
        hour,
        minute,
        second
    ));
    request->send(200, "text/plain", "OK");
});