#include <Arduino.h>
#include <NimBLEDevice.h>
#include "iPixelDeviceRegistry.h"

static const char* DEVICE_MAC = "19:2D:FE:55:52:AA";
static iPixelDevice* matrix = nullptr;

bool commandSent = false;
unsigned long lastStatusLog = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("[BLE Example] Starting BLE-only iPixel registry example");
  Serial.println("[BLE Example] Update DEVICE_MAC in src/examples/ble_only_main.cpp before use");

  NimBLEDevice::init("iPixel-BLE-Example");
  matrix = getOrCreateDevice(String(DEVICE_MAC));
}

void loop() {
  loop_deviceregistry();

  const unsigned long now = millis();
  if (now - lastStatusLog > 3000) {
    lastStatusLog = now;
    const bool connected = (matrix != nullptr) ? matrix->connected : false;
    const unsigned int queued = (matrix != nullptr) ? (unsigned int)matrix->queue.size() : 0;
    Serial.printf("[BLE Example] connected=%s queued=%u\n", connected ? "true" : "false", queued);
  }

  if (matrix != nullptr && matrix->connected && !commandSent) {
    matrix->setBrightness(60);
    matrix->clear();
    matrix->sendText("Hello", 0, 1, 50, 255, 255, 255, 0, 16, 16);
    commandSent = true;
    Serial.println("[BLE Example] Initial commands queued");
  }

  delay(1);
}
