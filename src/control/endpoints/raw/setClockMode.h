#pragma once
#include "webserver/endpoint.h"
#include "../../helpers.h"
#include "iPixelCommands.h"

Endpoint ENDPOINT_control_raw_setClockMode("/control/raw/setClockMode", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing* device = getBluetoothDevice(request, "device");
    long style = getParamLong(request, "style");
    long dayOfWeek = getParamLong(request, "dayOfWeek");
    long year = getParamLong(request, "year");
    long month = getParamLong(request, "month");
    long day = getParamLong(request, "day");
    bool showDate = getParamBool(request, "showDate");
    bool format24 = getParamBool(request, "format24");
    device->queuePush(iPixelCommands::setClockMode(
        style,
        dayOfWeek,
        year,
        month,
        day,
        showDate,
        format24
    ));
    request->send(200, "text/plain", "OK");
});