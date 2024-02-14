#include <WiFi.h>
#include "ESPAsyncWebServer.h"

#define lightPin  32
#define doorPin 33
#define switchBoot 0
#define DHTPIN 21
#define DHTTYPE DHT22
#define doorBellPin 23

const char* WIFI_SSID = "wolves";
const char* WIFI_PASSWORD = "csewolveslab@201";
TaskHandle_t Task1;
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"
AsyncWebServer server(80);
IPAddress IP = {192, 168, 1, 30};
IPAddress NMask = {255, 255, 255, 0};
IPAddress noIP = {0, 0, 0, 0};
IPAddress storedIp;
IPAddress localIP;
IPAddress gatewayIP;
IPAddress subnetMask;
IPAddress dnsIP0;
IPAddress dnsIP1;
int connectTime = 0;
int doorStateApp, fanSpeed, fanStateApp, lightStateApp, fireAlert, doorBell, doorBellFb;
int staApSSIDSw = 0;
int staApPASSSw = 0;
int doorStateDevice = 2;
int fanStateDevice = 2;
int lightStateDevice = 2;
int oldDoorStateApp = 2;
int oldFanStateApp = 2;
int oldLightStateApp = 2;
int oldFanSpeedFb = 333;
int oldDoorStateAppFb = 2;
int oldFanStateAppFb = 2;
int oldLightStateAppFb = 2;
int oldFanSpeed = 333;
int dataUpdate = 1;
int firstDataUpdate = 1;
int firstDataUpdatexx = 1;
char input_char;
int staApSw = 0;
unsigned long timeX, timeY, timeXT, timeDHT1, timeDB, timeDHT0;
int doorStateDeviceFb = 1;
String espCamlIP;
int wifiRetry = 0;
const char* PARAM_INPUT = "value";
unsigned long previousMillis = 0;
unsigned long interval = 30000;
int timeSwitch = 0;
float h, t, f;

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

void setup()
{
  Serial.begin(115200);
  // SerialEspCam.begin(115200);
  // SerialArduino.begin(115200);
  pinMode(doorPin, OUTPUT);
  digitalWrite(doorPin, HIGH);
  pinMode(doorBellPin, INPUT);
  pinMode(lightPin, OUTPUT);
  pinMode(switchBoot, INPUT);

  // preferences.begin("wifiCred", false);
  // staApSw = preferences.getInt("switch", 0);
  // String ssidStr = preferences.getString("ssid", "");
  // String passStr = preferences.getString("pass", "");
  // WIFI_SSID = ssidStr.c_str();
  // WIFI_PASSWORD = passStr.c_str();
  // if ((WIFI_SSID == "") && (WIFI_PASSWORD == "")) {
  //   Serial.print("SSID & PASSWORD not found");
  //   staApSw  = 0;
  // }
  staApSw = 1;
  if (staApSw == 1) {
    WiFi.disconnect(true);
    delay(1000);
    WiFi.onEvent(WiFiStationConnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_CONNECTED);
    WiFi.onEvent(WiFiGotIP, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_GOT_IP);
    WiFi.onEvent(WiFiStationDisconnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_DISCONNECTED);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (true) {
      while ((WiFi.status() != WL_CONNECTED) && (wifiRetry < 15)) {
        Serial.print(".");
        delay(300);
        wifiRetry++;
      }
      if (WiFi.status() == WL_CONNECTED) {
        if (connectTime == 1) {
          break;
        } else if (connectTime == 0) {
          storedIp = WiFi.localIP();
          localIP = {storedIp[0], storedIp[1], storedIp[2], 40};
          // espCamlIP = String(storedIp[0]) + "." + String(storedIp[1]) + "." + String(storedIp[2]) + ".40";
          storedIp = WiFi.gatewayIP();
          gatewayIP = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
          storedIp = WiFi.subnetMask();
          subnetMask = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
          storedIp = WiFi.dnsIP(0);
          dnsIP0 = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
          storedIp = WiFi.dnsIP(1);
          dnsIP1 = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
          wifiRetry = 0;
          connectTime += 1;
          WiFi.disconnect();
          delay(500);
          if ((localIP != noIP) && (gatewayIP != noIP) && (subnetMask != noIP) && (dnsIP0 != noIP)) {
            Serial.println("setting ip");
            if (WiFi.config(localIP, gatewayIP, subnetMask, dnsIP0, dnsIP1) == false) {
              Serial.println("Configuration failed.");
            }
          }
          WiFi.reconnect();
        }
      } else {
        wifiRetry = 0;
        WiFi.disconnect();
        WiFi.reconnect();
      }
    }
  } else if (staApSw == 0) {
    WiFi.mode(WIFI_AP);
    WiFi.softAP("EspDevice", "password1234");
    delay(1000);
    WiFi.softAPConfig(IP, IP, NMask);
    delay(1000);
  }
  timeXT = millis();
  timeX = millis();
  timeDHT0 = millis();
  timeDHT1 = millis();
  
  server.on("/cheakDevice", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "esp32device-" + String(lightStateDevice) + "-" + String(fanStateDevice) + "-" + String(doorStateDevice) + "-" + String(fanSpeed) + "-" + String(t) + "-" + String(f) + "-" + String(h) + "-" + String(fireAlert) + "-" + String(doorBell));
  });
  server.on("/lightOn", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "light On");
    lightStateApp = 1;
    oldLightStateApp = 1;
    lightStateDevice = 1;
    digitalWrite(lightPin, HIGH);
  });
  server.on("/lightOff", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "light Off");
    lightStateApp = 0;
    oldLightStateApp = 0;
    lightStateDevice = 0;
    digitalWrite(lightPin, LOW);
  });
  server.on("/fanOn", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "fan On");
    fanStateApp = 1;
    oldFanStateApp = 1;
    fanStateDevice = 1;
    // if (fanSpeed == 0){
    //   SerialArduino.println(300);
    // } else {
    //   SerialArduino.println(fanSpeed);
    // }
  });
  server.on("/fanOff", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "fan Off");
    fanStateApp = 0;
    oldFanStateApp = 0;
    fanStateDevice = 0;
    // SerialArduino.println(300);
  });
  server.on("/doorLock", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "door Lock");
    doorStateApp = 0;
    oldDoorStateApp = 0;
    doorStateDevice = 0;
    doorStateDeviceFb = 0;
    digitalWrite(doorPin, HIGH);
  });
  server.on("/doorUnlock", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "door Unlock");
    doorStateApp = 1;
    oldDoorStateApp = 1;
    doorStateDevice = 1;
    doorStateDeviceFb = 1;
    digitalWrite(doorPin, LOW);
  });
  server.on("/fanSpeed", HTTP_GET, [] (AsyncWebServerRequest *request) {
    String inputMessage;
    if (request->hasParam(PARAM_INPUT)) {
      inputMessage = request->getParam(PARAM_INPUT)->value();
      fanSpeed = inputMessage.toInt();
    }
    // if (fanStateApp == 0){
    //   fanStateDevice = 0;
    //   SerialArduino.println(300);
    // } else if (fanStateApp == 1){
    //   SerialArduino.println(fanSpeed);
    // }
    request->send(200, "text/plain", "fanSpeed-" + String(fanSpeed));
  });

  server.on("/ssid", HTTP_GET, [](AsyncWebServerRequest *request){
    staApSSIDSw = 1;
    String ssid;
    if (request->hasParam("value")) {
      ssid = request->getParam("value")->value();
    }
    request->send(200, "text/plain", "ssid");
  });
  server.on("/pass", HTTP_GET, [](AsyncWebServerRequest *request){
    staApPASSSw = 1;
    String pass;
    if (request->hasParam("value")) {
      pass = request->getParam("value")->value();
    }
    request->send(200, "text/plain", "pass");
  });
  server.begin();
}

void loop() {
  
}
