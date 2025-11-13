#pragma once
#include <Arduino.h>
#include <WiFi.h>
#include "registry.h"

struct WiFiTaskState {
    unsigned long startAttempt = 0;
    bool connecting = false;
    WiFiPairing* currentCred = nullptr;
    bool ap = false;
};
WiFiTaskState wifiState;