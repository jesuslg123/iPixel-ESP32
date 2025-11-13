#pragma once
#include <Arduino.h>
#include "Tasking.h"
#include "registry.h"

Task BluetoothLoopConnect("BluetoothLoopConnect", 0, 1000, "loop", []() {
   for(auto &device : bluetoothPairings.list()) {
    device.loop_connect();
   }
});

Task BluetoothLoopQueue("BluetoothLoopQueue", 0, 10, "loop", []() {
   for(auto &device : bluetoothPairings.list()) {
    device.loop_queue();
   }
});