#pragma once
#include <Arduino.h>
#include "parser/GenericRegistry.h"
#include <NimBLEDevice.h>

const NimBLEUUID serviceUUID("000000fa-0000-1000-8000-00805f9b34fb");
const NimBLEUUID charUUID("0000fa02-0000-1000-8000-00805f9b34fb");

class BluetoothPairing : public NimBLEClientCallbacks {
    public:
        String id;
        String name;
        String mac;
        bool enabled;
        
        bool _connecting = false;
        bool _connected = false;
        NimBLEClient* _client = nullptr;
        NimBLERemoteService *_service = nullptr;
        NimBLERemoteCharacteristic *_characteristic = nullptr;
        std::vector<std::vector<uint8_t>> _queue;

        void fromJSON(JsonObject doc) {
            id = doc["id"].as<String>();
            name = doc["name"].as<String>();
            mac = doc["mac"].as<String>();
            enabled = doc["enabled"];
        }

        void toJSON(JsonObject &doc) {
            doc["id"] = id;
            doc["name"] = name;
            doc["mac"] = mac;
            doc["enabled"] = enabled;
            doc["_connecting"] = _connecting;
            doc["_connected"] = _connected;   
            doc["_queuedCommands"] = _queue.size();   
        }

        void loop_connect() {
            if(!_client) {
                _client = NimBLEDevice::createClient();
                _client->setClientCallbacks(this, false);
                Serial.println("[Bluetooth] [" + id + "] " + "Created client!");
            }

            if (!_connecting && !_connected) {
                Serial.println("[Bluetooth] [" + id + "] Trying to connect...");
                if (_client->connect(NimBLEAddress(mac.c_str(), 0))) {
                    _connecting = true;
                } else {
                    _connecting = false;
                    Serial.println("[Bluetooth] [" + id + "] Connect failed immediately, retrying...");
                }
                return;
            }

            if(!_connected) return;

            if(!_service) {
                _service = _client->getService(serviceUUID);
                if(!_service) {
                    Serial.println("[Bluetooth] [" + id + "] " + "Failed to get service!");
                    return;
                }
            }

            if(!_characteristic) {
                _characteristic = _service->getCharacteristic(charUUID);
                if(!_characteristic) {
                    Serial.println("[Bluetooth] [" + id + "] " + "Failed to get characteristic!");
                    return;
                }
            }
        }

        void loop_queue() {
            if(!_connected) return;
            if (_queue.empty()) return;

            //Get command from queue
            std::vector<uint8_t> &command = _queue.front();

            //Take bytes from command
            size_t chunkSize = min(500, (int)command.size());

            //Write bytes from command
            _characteristic->writeValue(command.data(), chunkSize, false);

            //Debug
            Serial.print("[Bluetooth] [" + id + "] ");
            Serial.print("Sent chunk of ");
            Serial.print(chunkSize);
            Serial.print(" bytes (remaining: ");
            Serial.print(command.size());
            Serial.print(") (queue size: ");
            Serial.print(_queue.size());
            Serial.println(")");

            //Print bytes as HEX
            Serial.print("Data: ");
            for (size_t i = 0; i < chunkSize; i++) {
                if (command[i] < 0x10) Serial.print('0'); // leading zero for single-digit hex
                Serial.print(command[i], HEX);
                Serial.print(' ');
            }
            Serial.println();

            //Remove bytes from command
            command.erase(command.begin(), command.begin() + chunkSize);

            //Remove command if empty
            if (command.empty()) _queue.erase(_queue.begin());

            //Do not overload BLE
            delay(100);
        }

        void onConnect(NimBLEClient *pClient) {
            _connected = true;
            _connecting = false;
            Serial.println("[Bluetooth] [" + id + "] " + "Connected!");
        }

        void onDisconnect(NimBLEClient *pClient) {
            _connected = false;
            _connecting = false;
            Serial.println("[Bluetooth] [" + id + "] " + "Disconnected!");
        }

        void queuePush(std::vector<uint8_t> command) {
            _queue.push_back(command);
            Serial.print("[Bluetooth] [" + id + "] ");
            Serial.print("Added command with ");
            Serial.print(command.size());
            Serial.print(" bytes to queue at ");
            Serial.println(_queue.size() - 1);
        }

        void reset() {
            _characteristic = nullptr;
            _service = nullptr;
            if(_client) NimBLEDevice::deleteClient(_client);
            _client = nullptr;
            _connected = false;
            _connecting = false;
            Serial.println("[Bluetooth] [" + id + "] " + "Reset!!!");
        }

};

GenericRegistry<BluetoothPairing> bluetoothPairings("/bluetoothPairings.json");