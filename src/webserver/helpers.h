#pragma once
#include <Arduino.h>
#include <ESPAsyncWebServer.h>
#include <stdexcept>

void requireParam(AsyncWebServerRequest* request, const char* name) {
    if(!request->hasParam(name)) throw std::invalid_argument("Missing '" + std::string(name) + "' parameter");
};

long getParamLong(AsyncWebServerRequest* request, const char* name) {
    requireParam(request, name);
    return request->getParam(name)->value().toInt();
};

bool getParamBool(AsyncWebServerRequest* request, const char* name) {
    return getParamLong(request, name) > 0;
};

String getParamString(AsyncWebServerRequest* request, const char* name) {
    requireParam(request, name);
    return request->getParam(name)->value();
};