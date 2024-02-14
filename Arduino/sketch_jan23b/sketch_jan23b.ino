#include "WiFi.h"
#include "ESPAsyncWebServer.h"
 
#define WIFI_SSID "wolves"
#define WIFI_PASSWORD "csewolveslab@201"

AsyncWebServer server(80);
int wifiRetry = 0;
int relayPin = 23;

void WiFiStationConnected(WiFiEvent_t event, WiFiEventInfo_t info) {
  Serial.println("Connected to AP successfully!");
}

void WiFiGotIP(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void WiFiStationDisconnected(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("Disconnected from WiFi access point");
  Serial.print("WiFi lost connection. Reason: ");
  Serial.println(info.wifi_sta_disconnected.reason);
  Serial.println("Trying to Reconnect");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}
void setup(){

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);
  
  Serial.begin(115200);
 
  WiFi.disconnect(true);

  delay(1000);

  WiFi.onEvent(WiFiStationConnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_CONNECTED);
  WiFi.onEvent(WiFiGotIP, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_GOT_IP);
  WiFi.onEvent(WiFiStationDisconnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_DISCONNECTED);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (true) {
    while ((WiFi.status() != WL_CONNECTED) || (wifiRetry < 10)) {
      Serial.print(".");
      delay(300);
      wifiRetry++;
    }
    if (WiFi.status() == WL_CONNECTED){
      break;
    } else {
    wifiRetry = 0;
    WiFi.disconnect();
    WiFi.reconnect();
    }
  }
 
  Serial.println(WiFi.localIP());
 
  server.on("/hello", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "Hello World");
  });

  server.on("/relay/off", HTTP_GET   , [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "ok");
    digitalWrite(relayPin, HIGH);
  });
   server.on("/relay/on", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain","ok");
    digitalWrite(relayPin, LOW);
  });
  
  server.on("/relay/toggle", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain","ok");
  });
  
  server.on("/relay", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "XX");
  });
  
  server.begin();
}
 
void loop(){}