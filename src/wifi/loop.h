#pragma once
#include <Arduino.h>
#include "Tasking.h"
#include <WiFi.h>
#include "registry.h"
#include "state.h"

Task WiFiLoop("WiFiLoop", 0, 1000, "loop", []() {
    // Check for connected
    if (wifiState.connecting && wifiState.currentCred) {
        if (WiFi.status() == WL_CONNECTED) {
            Serial.println("[WiFi] Connected successfully to: " + WiFi.SSID());
            Serial.printf("[WiFi] IP address: %s\n", WiFi.localIP().toString().c_str());
            wifiState.currentCred->_failed = false;
            wifiState.currentCred->_connected = true;
            wifiState.connecting = false;
        }
    }

    //Set Disconnected
    if(!WiFi.isConnected() && wifiState.currentCred && wifiState.currentCred->_connected) {
        wifiState.currentCred->_connected = false;
        Serial.println("[WiFi] Disconnected from: " + wifiState.currentCred->ssid);
    }

    //Skip if connected
    if (WiFi.isConnected()) return;

    // Sort the credentials
    auto &list = wifiPairings.list();
    std::sort(list.begin(), list.end(), [](const WiFiPairing &a, const WiFiPairing &b) {
        return b.priority > a.priority;
    });

    // Search next credential to try
    WiFiPairing* nextCred = nullptr;
    for (auto &w : wifiPairings.list()) {
         if (w.enabled && !w._failed) {
            nextCred = &w;
            break;
        }
    }

    // Start AP if all credentials have failed
    if(!nextCred) {
        if(wifiState.ap) return;
        Serial.println("[WiFi] Oh no! All pairings failed! Entering AP mode...");
        WiFi.disconnect(true);
        WiFi.mode(WIFI_AP);
        
        const char* apSSID = "iPixel-ESP32";
        const char* apPassword = "123456789";
        WiFi.softAP(apSSID, apPassword);
        Serial.printf("[WiFi] AP started: %s\n", apSSID);
        Serial.printf("[WiFi] IP address: %s\n", WiFi.softAPIP().toString().c_str());

        wifiState.ap = true;
        return;
    }    

    // Start a new attempt if not connecting
    if (!wifiState.connecting) {
        wifiState.currentCred = nextCred;
        wifiState.connecting = true;
        wifiState.startAttempt = millis();
        nextCred->_failed = false;
        Serial.printf("[WiFi] Attempting connection to %s\n", nextCred->ssid.c_str());
        WiFi.disconnect(true);
        WiFi.mode(WIFI_STA);
        WiFi.begin(nextCred->ssid.c_str(), nextCred->password.c_str());
    }

    // Check for timeout (30 seconds)
    if (wifiState.connecting && wifiState.currentCred) {
        if (millis() - wifiState.startAttempt > 30000) {
            Serial.println("[WiFi] Connection timed out, will try next pairing...");
            WiFi.disconnect();
            wifiState.currentCred->_failed = true;
            wifiState.connecting = false;
        }
    }
});