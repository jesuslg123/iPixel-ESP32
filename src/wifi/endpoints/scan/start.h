#pragma once
#include <WiFi.h>
#include <ArduinoJson.h>
#include "webserver/endpoint.h"

Endpoint ENDPOINT_wifi_scan_start("/wifi/scan/start", HTTP_GET, [](AsyncWebServerRequest* request) {
    WiFi.scanDelete();                
    WiFi.scanNetworks(true);

    JsonDocument doc;
    doc["status"] = "scanning";
                
    String response;
    serializeJson(doc, response);
    request->send(202, "application/json", response);
});