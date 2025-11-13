#pragma once
#include <WiFi.h>
#include <ArduinoJson.h>
#include "webserver/endpoint.h"
#include "../../registry.h"

Endpoint ENDPOINT_wifi_pairings_list("/wifi/pairings/list", HTTP_GET, [](AsyncWebServerRequest* request) {
    JsonDocument doc;
    doc["ok"] = true;
    JsonArray data = doc["data"].to<JsonArray>();
    for(auto &w : wifiPairings.list()) {
        JsonObject obj = data.add<JsonObject>();
        w.toJSON(obj);
    }

    String json;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
});