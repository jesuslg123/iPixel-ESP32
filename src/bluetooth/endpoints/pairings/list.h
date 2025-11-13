#pragma once
#include <ArduinoJson.h>
#include "webserver/endpoint.h"
#include "../../registry.h"

Endpoint ENDPOINT_bluetooth_pairings_list("/bluetooth/pairings/list", HTTP_GET, [](AsyncWebServerRequest* request) {
    JsonDocument doc;
    doc["ok"] = true;
    JsonArray data = doc["data"].to<JsonArray>();
    for(auto &w : bluetoothPairings.list()) {
        JsonObject obj = data.add<JsonObject>();
        w.toJSON(obj);
    }

    String json;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
});