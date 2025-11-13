#pragma once
#include "Tasking.h"
#include <NimBLEDevice.h>
#include "registry.h"

Task BluetoothSetup("BluetoothSetup", 1, 0, "setup", []() {
    Serial.println("[Bluetooth] Initialising...");
    NimBLEDevice::init("ESP32");
    bluetoothPairings.load();
    Serial.println("[Bluetooth] Initialized!");
});