#pragma once
#include <LittleFS.h>
#include "Tasking.h"
#include "server.h"
#include "endpoint.h"

Task WebserverSetup("WebserverSetup", 1, 0, "setup", []() {
    Serial.println("[Webserver] Initialising...");
    tcpip_adapter_init(); //Do this because WiFi is not initialized here

    for (auto& ep : Endpoint::getRegistry()) {
        server.on(ep->path, ep->method, [handler = ep->handler](AsyncWebServerRequest* request) {
            try {
                handler(request);
            } catch (const std::invalid_argument& ex) {
                request->send(400, "text/plain", ex.what());
            } catch (const std::out_of_range& ex) {
                request->send(404, "text/plain", ex.what());
            } catch (const std::runtime_error& ex) {
                request->send(500, "text/plain", ex.what());
            } catch (const std::exception& ex) {
                request->send(500, "text/plain", ex.what());
            } catch (...) {
                request->send(500, "text/plain", "Unknown error");
            }
        });
        Serial.print("[Webserver] Registered endpoint: ");
        Serial.println(ep->path);
    }

    //server.serveStatic("/", LittleFS, "/www/").setDefaultFile("index.html");

    server.begin();
    Serial.println("[Webserver] Initialized!");
});

