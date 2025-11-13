#pragma once
#include <Arduino.h>
#include <vector>
#include <ArduinoJson.h>
#include <LittleFS.h>

template <typename T>
class GenericRegistry {
private:
    const String rootFile;
    std::vector<T> entries;
    bool debug = true;

    void debugPrint(const String &msg) const {
        if (debug) {
            Serial.println("[GenericRegistry] [" + rootFile + "] " + msg);
        }
    }

public:
    GenericRegistry(const String &filePath, bool debugMode = true)
        : rootFile(filePath), debug(debugMode) {
        if (!LittleFS.exists(rootFile)) {
            File file = LittleFS.open(rootFile, "w");
            if (file) {
                file.print("[]");
                file.close();
                debugPrint("Created new registry file: " + rootFile);
            }
        }
    }

    bool load() {
        entries.clear();
        if (!LittleFS.exists(rootFile)) {
            debugPrint("Registry file does not exist, creating: " + rootFile);
            File file = LittleFS.open(rootFile, "w");
            if (file) {
                file.print("[]");
                file.close();
            }
            return true;
        }

        File file = LittleFS.open(rootFile, "r");
        if (!file) {
            debugPrint("Failed to open registry file for reading");
            return false;
        }

        JsonDocument doc;
        DeserializationError err = deserializeJson(doc, file);
        file.close();

        if (err) {
            debugPrint("Failed to deserialize registry file: " + String(err.c_str()));
            return false;
        }

        if (!doc.is<JsonArray>()) {
            debugPrint("Registry file is not a JSON array");
            return false;
        }

        for (JsonObject obj : doc.as<JsonArray>()) {
            T item;
            item.fromJSON(obj);
            entries.push_back(item);
            debugPrint("Loaded: " + item.id);
        }

        debugPrint("Total entries loaded: " + String(entries.size()));
        return true;
    }

    bool save() {
        File file = LittleFS.open(rootFile, "w");
        if (!file) {
            debugPrint("Failed to open registry file for writing");
            return false;
        }

        JsonDocument doc;
        JsonArray arr = doc.to<JsonArray>();

        for (auto &item : entries) {
            JsonObject obj = arr.add<JsonObject>();
            item.toJSON(obj);
            debugPrint("Saved: " + item.id);
        }

        serializeJson(doc, file);
        file.close();
        debugPrint("Total entries saved: " + String(entries.size()));
        return true;
    }

    void add(const T &item) {
        entries.push_back(item);
        debugPrint("Added entry: " + item.id);
    }

    void clear() {
        entries.clear();
        debugPrint("Cleared all entries");
    }

    std::vector<T> &list() {
        return entries;
    }

    T* find(const String &id) {
        for (auto &item : entries) {
            if (item.id == id) {
                debugPrint("Found entry: " + id);
                return &item;
            }
        }
        debugPrint("Entry not found: " + id);
        return nullptr;
    }

    bool remove(const String &id) {
        for (auto it = entries.begin(); it != entries.end(); ++it) {
            if (it->id == id) {
                entries.erase(it);
                debugPrint("Removed entry: " + id);
                return true;
            }
        }
        debugPrint("Remove failed, entry not found: " + id);
        return false;
    }

    bool remove(const T &item) {
        return remove(item.id);
    }
};