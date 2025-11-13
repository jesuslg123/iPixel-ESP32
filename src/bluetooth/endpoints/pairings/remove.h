#pragma once
#include <ArduinoJson.h>
#include "webserver/endpoint.h"
#include "webserver/helpers.h"
#include "../../registry.h"

Endpoint ENDPOINT_bluetooth_pairings_remove("/bluetooth/pairings/remove", HTTP_GET, [](AsyncWebServerRequest* request) {
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

    bluetoothPairings.remove(*pairing);
    bluetoothPairings.save();

    JsonDocument doc;
    doc["ok"] = true;
    JsonObject data = doc["data"].to<JsonObject>();
    pairing->toJSON(data);

    String json;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
});