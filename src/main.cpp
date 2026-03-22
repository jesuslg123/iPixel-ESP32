#include "Tasking.h"

void setup() {
  delay(2000);
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println("[Setup] iPixel BLE Library initialized");
  Task::runAllOf("setup");
}

void loop() {
  Task::runAllOf("loop");
  delay(1);
}	