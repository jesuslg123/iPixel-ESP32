#pragma once
#include <WiFi.h>
#include <ArduinoJson.h>
#include "webserver/endpoint.h"
#include "webserver/helpers.h"
#include "../../registry.h"

Endpoint ENDPOINT_wifi_pairings_remove("/wifi/pairings/remove", HTTP_GET, [](AsyncWebServerRequest* request) {
    String id = getParamString(request, "id");
    WiFiPairing* pairing = wifiPairings.find(id);
    if(!pairing) {
        JsonDocument doc;
        doc["ok"] = false;
        doc["error"] = "Pairing not found";

        String json;
        serializeJson(doc, json);
        request->send(200, "application/json", json);
        return;
    }

    wifiPairings.remove(*pairing);
    wifiPairings.save();

    JsonDocument doc;
    doc["ok"] = true;
    JsonObject data = doc["data"].to<JsonObject>();
    pairing->toJSON(data);

    String json;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
});