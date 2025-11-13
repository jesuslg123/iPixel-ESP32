#pragma once
#include <Arduino.h>
#include "parser/GenericRegistry.h"

class WiFiPairing {
    public:
        String id;
        String ssid;
        String password;
        bool enabled;
        int priority;
        
        bool _connected = false;
        bool _failed = false;

        void fromJSON(JsonObject doc) {
            id = doc["id"].as<String>();
            ssid = doc["ssid"].as<String>();
            password = doc["password"].as<String>();
            enabled = doc["enabled"];
            priority = doc["priority"];
        }

        void toJSON(JsonObject &doc) {
            doc["id"] = id;
            doc["ssid"] = ssid;
            doc["password"] = password;
            doc["enabled"] = enabled;
            doc["priority"] = priority;
            doc["_connected"] = _connected;
            doc["_failed"] = _failed;
        }
};

GenericRegistry<WiFiPairing> wifiPairings("/wifiPairings.json");