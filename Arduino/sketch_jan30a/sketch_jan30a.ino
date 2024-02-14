#include <WiFi.h>
#include <FirebaseESP32.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include "DHT.h"
#include "ESPAsyncWebServer.h"
#include <Preferences.h>

#define lightPin  32
#define doorPin 33
#define switchBoot 0
#define DHTPIN 21
#define DHTTYPE DHT22
#define doorBellPin 23

const char* WIFI_SSID = "";
const char* WIFI_PASSWORD = "";
TaskHandle_t Task1;
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"
Preferences preferences;
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
FirebaseData fbdo;
FirebaseData updateDb;
FirebaseAuth auth;
FirebaseConfig config;
DHT dht(DHTPIN, DHTTYPE);
// HardwareSerial SerialEspCam(1);
HardwareSerial SerialArduino(2);

void loop2( void * parameter ) {
  while (true) {
    Serial.println("x");
    if (staApSw == 0) {
      // SerialEspCam.println("zz");
      if ((staApSSIDSw == 1) && (staApPASSSw == 1)) {
        preferences.putInt("switch", 1);
        preferences.end();
        ESP.restart(); 
      }
    } else if (staApSw == 1) {
      if (digitalRead(switchBoot) == LOW) {
        while (true) {
          if (digitalRead(switchBoot) == HIGH) {
            break;
          }
        }
        preferences.putInt("switch", 0);
        preferences.end();
        delay(500);
        ESP.restart();
      }
      if ((WiFi.status() != WL_CONNECTED) && (millis() - previousMillis >=interval)) {
        WiFi.disconnect();
        WiFi.reconnect();
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
        previousMillis = millis();
      }
      // if (SerialEspCam.available()) {
      //   input_char = SerialEspCam.read();
      //   if ((input_char == 'zx') || (input_char == 'xz')){
      //     doorStateApp = 1;
      //   }
      // }
      if ((fanStateApp == 1) && (millis() - timeXT > 1000)){
        timeXT = millis();
        if (fanSpeed == 0){
          SerialArduino.println(300);
        }
        SerialArduino.println(fanSpeed);
      }
      if (oldLightStateApp != lightStateApp) {
        oldLightStateApp = lightStateApp;
        if (lightStateApp == 0){
          lightStateDevice = 0;
          digitalWrite(lightPin, LOW);
        } else if (lightStateApp == 1){
          lightStateDevice = 1;
          digitalWrite(lightPin, HIGH);
        }
      }
      if (oldFanStateApp != fanStateApp) {
        oldFanStateApp = fanStateApp;
        if (fanStateApp == 0){
          fanStateDevice = 0;
          SerialArduino.println(300);
        } else if (fanStateApp == 1){
          fanStateDevice = 1;
          SerialArduino.println(fanSpeed);
        }
      }
      if (oldDoorStateApp != doorStateApp) {
        oldDoorStateApp = doorStateApp;
        if (doorStateApp == 0){
          doorStateDevice = 0;
          digitalWrite(doorPin, HIGH);
        } else if (doorStateApp == 1){
          doorStateDevice = 1;
          digitalWrite(doorPin, LOW);
        }
      }
      if (doorStateDevice == 1) {
        if (millis() - timeX > 10000){
          timeX = millis();
          doorStateDevice = 0;
          doorStateApp = 0;
          digitalWrite(doorPin, HIGH);
          doorStateDeviceFb = 0;
        }  
      } else {
        timeX = millis();
      }
      if (millis() - timeDHT0 > 500){
        timeDHT0 = millis();
        h = dht.readHumidity();
        t = dht.readTemperature();
        f = dht.readTemperature(true);
        if (isnan(h) || isnan(t) || isnan(f)) {
          // Serial.println(F("Failed to read from DHT sensor!"));
          return;
        } else {
          if (t > 50){
            fireAlert = 1;
          } else if (t < 50) {
            fireAlert = 0;
          }
        }
      }
    }
  }
}

void setup()
{
  Serial.begin(115200);
  // SerialEspCam.begin(115200);
  SerialArduino.begin(115200);
  pinMode(doorPin, OUTPUT);
  digitalWrite(doorPin, HIGH);
  pinMode(doorBellPin, INPUT);
  pinMode(lightPin, OUTPUT);
  pinMode(switchBoot, INPUT);

  preferences.begin("wifiCred", false);
  staApSw = preferences.getInt("switch", 0);
  String ssidStr = preferences.getString("ssid", "");
  String passStr = preferences.getString("pass", "");
  WIFI_SSID = ssidStr.c_str();
  WIFI_PASSWORD = passStr.c_str();
  if ((WIFI_SSID == "") && (WIFI_PASSWORD == "")) {
    Serial.print("SSID & PASSWORD not found");
    staApSw  = 0;
  }
  if (staApSw == 1) {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (true) {
      while ((WiFi.status() != WL_CONNECTED) && (wifiRetry < 15)) {
        Serial.print(".");
        delay(300);
        wifiRetry++;
      }
      if (WiFi.status() == WL_CONNECTED) {
        if (connectTime == 1) {
          wifiRetry = 0;
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
  dht.begin();
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  Firebase.begin(DATABASE_URL, API_KEY);
  Firebase.setDoubleDigits(5);
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
    if (fanSpeed == 0){
      SerialArduino.println(300);
    } else {
      SerialArduino.println(fanSpeed);
    }
  });
  server.on("/fanOff", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "fan Off");
    fanStateApp = 0;
    oldFanStateApp = 0;
    fanStateDevice = 0;
    SerialArduino.println(300);
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
    if (fanStateApp == 0){
      fanStateDevice = 0;
      SerialArduino.println(300);
    } else if (fanStateApp == 1){
      SerialArduino.println(fanSpeed);
    }
    request->send(200, "text/plain", "fanSpeed-" + String(fanSpeed));
  });

  server.on("/ssid", HTTP_GET, [](AsyncWebServerRequest *request){
    staApSSIDSw = 1;
    String ssid;
    if (request->hasParam("value")) {
      ssid = request->getParam("value")->value();
    }
    preferences.putString("ssid", ssid);
    request->send(200, "text/plain", "ssid");
  });
  server.on("/pass", HTTP_GET, [](AsyncWebServerRequest *request){
    staApPASSSw = 1;
    String pass;
    if (request->hasParam("value")) {
      pass = request->getParam("value")->value();
    }
    preferences.putString("pass", pass);
    request->send(200, "text/plain", "pass");
  });
  xTaskCreatePinnedToCore(
    loop2,
    "loop2",
    10000,
    NULL,
    0,
    &Task1,
    0);
  
  server.begin();
}

void loop() {
  if (staApSw == 0) {
    if ((staApSSIDSw == 1) && (staApPASSSw == 1)) {
      preferences.putInt("switch", 1);
      preferences.end();
      ESP.restart(); 
    }
  } else if (staApSw == 1) {
      if (digitalRead(doorBellPin) == HIGH) {
        while (true) {
            if (digitalRead(doorBellPin) == LOW)
                break;
        }
        doorBell = 1;
        doorBellFb = 1;
        timeDB = millis();
      }
      if (doorBell == 1) {
        if (millis() - timeDB > 10000) {
          doorBell = 0; 
        }
      }
    if (Firebase.ready()) {
      if (millis() - timeDHT1 > 5000){
        timeDHT1 = millis();
        if (isnan(h) || isnan(t) || isnan(f)) {
          // Serial.println(F("Failed to read from DHT sensor!"));
          return;
        } else {
          Firebase.setFloat(fbdo, "/states/roomHum", h);
          Firebase.setFloat(fbdo, "/states/roomTemp", t);
          Firebase.setFloat(fbdo, "/states/roomTempFer", f);
          if (t > 50){
            fireAlert = 1;
            Firebase.setInt(fbdo, "/states/fireAlert", 1);
          } else if ((t < 50) && (fireAlert == 1)){
            fireAlert = 0;
            Firebase.setInt(fbdo, "/states/fireAlert", 0);
          }
        }
      }   

      if ((oldLightStateAppFb != lightStateApp) && (oldLightStateAppFb != 2)) {
        oldLightStateAppFb = lightStateApp;
        Firebase.setInt(fbdo, "/states/lightStateApp", lightStateApp);
        Firebase.setInt(fbdo, "/states/lightStateDevice", lightStateApp);
      }
      if ((oldFanStateAppFb != fanStateApp) && (oldFanStateAppFb != 2)) {
        oldFanStateAppFb = fanStateApp;
        Firebase.setInt(fbdo, "/states/fanStateApp", fanStateApp);
        Firebase.setInt(fbdo, "/states/fanStateDevice", fanStateApp);
      }
      if ((oldDoorStateAppFb != doorStateApp) && (oldDoorStateAppFb != 2)) {
        oldDoorStateAppFb = doorStateApp;
        Firebase.setInt(fbdo, "/states/doorStateApp", doorStateApp);
        Firebase.setInt(fbdo, "/states/doorStateDevice", doorStateApp);
      }
      if ((oldFanSpeedFb != fanSpeed) && (oldFanSpeedFb != 333)) {
        oldFanSpeedFb = fanSpeed;
        Firebase.setInt(fbdo, "/states/fanSpeed", fanSpeed);
      }

      if (doorBellFb == 1) {
        doorBellFb = 0;
        Firebase.setInt(fbdo, "/states/takePhoto", 1);
        Firebase.setInt(fbdo, "/states/doorBellDevice", 1);
      }
      if (doorStateDeviceFb == 0) {
        doorStateDeviceFb = 1;
        Firebase.setInt(fbdo, "/states/doorStateApp", 0);
        Firebase.setInt(fbdo, "/states/doorStateDevice", 0);
      }
      Firebase.getInt(fbdo, "/states/dataUpdate");
      dataUpdate = fbdo.to<int>();
      if ((dataUpdate == 1) || (firstDataUpdate == 1)) {
        firstDataUpdate = 0;
        dataUpdate = 0;
        Firebase.setInt(fbdo, "/states/dataUpdate", 0);
        Firebase.getInt(fbdo, "/states/doorStateApp");
        doorStateApp = fbdo.to<int>();
        Firebase.getInt(fbdo, "/states/lightStateApp");
        lightStateApp = fbdo.to<int>();
        Firebase.getInt(fbdo, "/states/fanStateApp");
        fanStateApp = fbdo.to<int>();
        Firebase.getInt(fbdo, "/states/fanSpeed");
        fanSpeed = fbdo.to<int>();
        Firebase.getInt(fbdo, "/states/fireAlert");
        fireAlert = fbdo.to<int>();
      }
    }
  }
}