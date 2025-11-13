#pragma once
#include <ArduinoJson.h>
#include "webserver/endpoint.h"
#include "webserver/helpers.h"
#include "../../registry.h"

Endpoint ENDPOINT_bluetooth_pairings_update("/bluetooth/pairings/update", HTTP_GET, [](AsyncWebServerRequest* request) {
    String id = getParamString(request, "id");
    BluetoothPairing* pairing = bluetoothPairings.find(id);
    if(!pairing) {
        JsonDocument doc;
        doc["ok"] = false;
        doc["error"] = "Pairing not found";

        String json;
        serializeJson(doc, json);
        request->send(200, "application/json", json);
        return;
    }

    pairing->name = getParamString(request, "name");
    pairing->mac = getParamString(request, "mac");
    pairing->enabled = getParamBool(request, "enabled");
    pairing->reset();

    bluetoothPairings.save();

    JsonDocument doc;
    doc["ok"] = true;
    JsonObject data = doc["data"].to<JsonObject>();
    pairing->toJSON(data);

    String json;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
});