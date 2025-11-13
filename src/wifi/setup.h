#pragma once
#include "Tasking.h"
#include "registry.h"

Task WiFiSetup("WiFiSetup", 0, 0, "setup", []() {
    Serial.println("[WiFi] Initialising...");
    wifiPairings.load();
    Serial.println("[WiFi] Initialized!");
});