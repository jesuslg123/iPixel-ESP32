#pragma once
#include "Arduino.h"
#include <vector>

class Task {
    public:
        const char* id;
        uint8_t priority;
        const char* runsOn;
        void (*handler)();
        unsigned long intervalMs;
        unsigned long lastRun;

        Task(const char* id, uint8_t priority, unsigned long intervalMs, const char* runsOn, void (*handler)()): id(id), priority(priority), intervalMs(intervalMs), runsOn(runsOn), handler(handler) {
            auto& endpoints = getRegistry();
            for (auto& e : endpoints) {
                if (strcmp(e->id, id) == 0) {
                    Serial.println("[Tasking] Duplicate task added: " + String(e->id));
                    return;
                }
            }
            endpoints.push_back(this);
        }

        static std::vector<Task*>& getRegistry() {
            static std::vector<Task*> registry;
            return registry;
        }

        static void runAllOf(const char* target) {
            unsigned long now = millis();
            std::vector<Task*> toRun;

            // Collect tasks that match the target
            for (auto* task : getRegistry()) {
                if (strcmp(task->runsOn, target) == 0) {
                    toRun.push_back(task);
                }
            }

            // Sort by priority (lower  priority first)
            std::sort(toRun.begin(), toRun.end(), [](Task* a, Task* b) {
                return b->priority > a->priority;
            });

            // Run tasks if interval has passed
            for (auto* task : toRun) {
                if (task->handler) {
                    if (task->intervalMs == 0 || now - task->lastRun >= task->intervalMs) {
                        task->handler();
                        task->lastRun = now;
                    }
                }
            }
        }
};