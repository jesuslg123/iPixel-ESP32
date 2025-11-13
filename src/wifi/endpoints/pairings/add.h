#pragma once
#include <WiFi.h>
#include <ArduinoJson.h>
#include "webserver/endpoint.h"
#include "webserver/helpers.h"
#include "../../registry.h"

Endpoint ENDPOINT_wifi_pairings_add("/wifi/pairings/add", HTTP_GET, [](AsyncWebServerRequest* request) {
    WiFiPairing pairing;
    pairing.id = String(random(0, 999999999));
    pairing.ssid = getParamString(request, "ssid");
    pairing.password = getParamString(request, "password");
    pairing.enabled = getParamBool(request, "enabled");
    pairing.priority = getParamLong(request, "priority");

    wifiPairings.add(pairing);
    wifiPairings.save();

    JsonDocument doc;
    doc["ok"] = true;
    JsonObject data = doc["data"].to<JsonObject>();
    pairing.toJSON(data);

    String json;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
});