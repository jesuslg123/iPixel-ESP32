#pragma once

#include <vector>
#include <NimBLEDevice.h>
#include "iPixelDevice.h"

// Global registry of known devices for compatibility with legacy sketches.
extern std::vector<iPixelDevice*> knownDevices;

iPixelDevice* getOrCreateDevice(const NimBLEAddress& addr);
iPixelDevice* getOrCreateDevice(const String& macAddress);

// Runs reconnect attempts and queued command flush for all known devices.
void loop_deviceregistry();

// Optional cleanup helper to disconnect and free registered devices.
void clearDeviceRegistry();
