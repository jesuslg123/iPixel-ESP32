#include <Arduino.h>
#include "iPixelBleClient.h"

static const char* DEVICE_MAC = "19:2D:FE:55:52:AA";

iPixelBLE::Client matrix(DEVICE_MAC);

bool commandSent = false;
unsigned long lastStatusLog = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("[BLE Example] Starting BLE-only iPixel client example");
  Serial.println("[BLE Example] Update DEVICE_MAC in src/examples/ble_only_main.cpp before use");

  iPixelBLE::Client::init("iPixel-BLE-Example");
  matrix.setAutoReconnect(true);
  matrix.connect();
}

void loop() {
  matrix.loop();

  const unsigned long now = millis();
  if (now - lastStatusLog > 3000) {
    lastStatusLog = now;
    Serial.printf("[BLE Example] connected=%s queued=%u\n", matrix.isConnected() ? "true" : "false", (unsigned int)matrix.queuedCommands());
  }

  if (matrix.isConnected() && !commandSent) {
    matrix.setBrightness(60);
    matrix.clear();
    matrix.sendText("Hello", 0, 1, 50, 255, 255, 255, 0, 16, 16);
    commandSent = true;
    Serial.println("[BLE Example] Initial commands queued");
  }

  delay(1);
}
