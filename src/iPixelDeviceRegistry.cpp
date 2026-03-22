#include "iPixelDeviceRegistry.h"

std::vector<iPixelDevice*> knownDevices;

static bool sameAddress(const NimBLEAddress& a, const NimBLEAddress& b) {
    return a.toString() == b.toString();
}

iPixelDevice* getOrCreateDevice(const NimBLEAddress& addr) {
    for (auto* dev : knownDevices) {
        if (dev != nullptr && sameAddress(dev->address, addr)) {
            return dev;
        }
    }

    auto* newDev = new iPixelDevice(addr);
    knownDevices.push_back(newDev);
    return newDev;
}

iPixelDevice* getOrCreateDevice(const String& macAddress) {
    return getOrCreateDevice(NimBLEAddress(macAddress.c_str(), 0));
}

void loop_deviceregistry() {
    static unsigned long lastAttempt = 0;
    const unsigned long now = millis();

    if (now - lastAttempt > 1000) {
        lastAttempt = now;
        for (auto* dev : knownDevices) {
            if (dev != nullptr && !dev->connected) {
                dev->connectAsync();
            }
        }
    }

    for (auto* dev : knownDevices) {
        if (dev != nullptr && dev->connected) {
            dev->queueTick();
        }
    }
}

void clearDeviceRegistry() {
    for (auto* dev : knownDevices) {
        if (dev == nullptr) {
            continue;
        }

        if (dev->client != nullptr && dev->connected) {
            dev->client->disconnect();
        }

        delete dev;
    }

    knownDevices.clear();
}
