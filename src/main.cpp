#include "Tasking.h"
#include "wifi/index.h"
#include "bluetooth/index.h"
#include "webserver/index.h"
#include "control/index.h"

void setup() {
  delay(2000);
  Serial.begin(115200);
  Serial.println("[Setup] Hello World! Let's hope we can pixel together!");
  Serial.println("[Setup] We are jumping into our task runner! *JUMPS*");
  LittleFS.begin();
  Task::runAllOf("setup");
}

void loop() {
  Task::runAllOf("loop");
  delay(1);
}

//  iPixelDevice test(BLEAddress("3d:50:0c:1f:6d:ec"));
//2F:9F:9C:9C:51:AC	