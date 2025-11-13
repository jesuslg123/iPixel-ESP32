#pragma once
#include <ArduinoJson.h>
#include "webserver/endpoint.h"
#include "webserver/helpers.h"
#include "../../registry.h"

Endpoint ENDPOINT_bluetooth_pairings_add("/bluetooth/pairings/add", HTTP_GET, [](AsyncWebServerRequest* request) {
    BluetoothPairing pairing;
    pairing.id = String(random(0, 999999999));
    pairing.name = getParamString(request, "name");
    pairing.mac = getParamString(request, "mac");
    pairing.enabled = getParamBool(request, "enabled");

    bluetoothPairings.add(pairing);
    bluetoothPairings.save();

    JsonDocument doc;
    doc["ok"] = true;
    JsonObject data = doc["data"].to<JsonObject>();
    pairing.toJSON(data);

    String json;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
});