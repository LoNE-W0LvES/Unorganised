#include <WiFi.h>
#include <FirebaseESP32.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include "DHT.h"

#define lightPin  32
#define doorPin 33

#define DHTPIN 21
#define DHTTYPE DHT22
#define doorBellPin 23

#define WIFI_SSID "HA"
#define WIFI_PASSWORD "12345678"
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"

int doorStateApp, fanSpeed, fanStateApp, lightStateApp, fireAlert;
int doorStateDevice = 2;
int oldDoorStateApp = 2;
int oldFanStateApp = 2;
int oldLightStateApp = 2;
int oldFanSpeed = 111;
int dataUpdate = 1;
int firstDataUpdate = 1;
char input_char;
unsigned long timeX, timeY, timeXT, timeDHT;
int timeSwitch = 0;
float h, t, f;
FirebaseData fbdo;
FirebaseData updateDb;
FirebaseAuth auth;
FirebaseConfig config;
DHT dht(DHTPIN, DHTTYPE);
HardwareSerial SerialArduino(2);
void setup()
{
  Serial.begin(115200);
  SerialArduino.begin(115200);
  pinMode(doorPin, OUTPUT);
  digitalWrite(doorPin, HIGH);
  pinMode(doorBellPin, INPUT);
  pinMode(lightPin, OUTPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  /* Assign the api key (required) */
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  Firebase.begin(DATABASE_URL, API_KEY);
  //Comment or pass false value when WiFi reconnection will control by your code or third party library
 // Firebase.reconnectWiFi(true);
  Firebase.setDoubleDigits(5);
  if (!Firebase.beginStream(updateDb, "/states/dataUpdate")){
    Serial.printf("stream begin error");
  }
  timeXT = millis();
  timeX = millis();
  timeDHT = millis();
  dht.begin();
}

void loop()
{
  if (Firebase.ready()) {
    if (!Firebase.readStream(updateDb))
      Serial.printf("stream read error");
    if (updateDb.streamAvailable()) {
      dataUpdate = updateDb.intData();
    }
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
    if (millis() - timeDHT > 5000){
      timeDHT = millis();
      h = dht.readHumidity();
      t = dht.readTemperature();
      f = dht.readTemperature(true);
      if (isnan(h) || isnan(t) || isnan(f)) {
        Serial.println(F("Failed to read from DHT sensor!"));
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
    if (oldLightStateApp != lightStateApp) {
      if (lightStateApp == 0){
        Firebase.setInt(fbdo, "/states/lightStateDevice", 0);
      }
      if (lightStateApp == 1){
        Firebase.setInt(fbdo, "/states/lightStateDevice", 1);
      }
    }
    if (oldFanStateApp != fanStateApp) {
      if (fanStateApp == 0){
        Firebase.setInt(fbdo, "/states/fanStateDevice", 0);
      }
      if (fanStateApp == 1){
        Firebase.setInt(fbdo, "/states/fanStateDevice", 1);
      }
    }
    if (oldDoorStateApp != doorStateApp) {
      if (doorStateApp == 0){
        Firebase.setInt(fbdo, "/states/doorStateDevice", 0);
      }
      if (doorStateApp == 1){
        Firebase.setInt(fbdo, "/states/doorStateDevice", 1);
      }
    }

    if (digitalRead(doorBellPin) == HIGH) {
      while (true) {
          if (digitalRead(doorBellPin) == LOW)
              break;
      }
      Firebase.setInt(fbdo, "/states/takePhoto", 1);
      Firebase.setInt(fbdo, "/states/doorBellDevice", 1);
    }
    if (doorStateDevice == 1) {
      if (millis() - timeX > 10000){
        timeX = millis();
        doorStateDevice = 0;
        doorStateApp = 0;
        digitalWrite(doorPin, HIGH);
        Firebase.setInt(fbdo, "/states/doorStateApp", 0);
        Firebase.setInt(fbdo, "/states/doorStateDevice", 0);
      }  
    } else {
      timeX = millis();
    }
  }

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
      digitalWrite(lightPin, LOW);
    } else if (lightStateApp == 1){
      digitalWrite(lightPin, HIGH);
    }
  }
  if (oldFanStateApp != fanStateApp) {
    oldFanStateApp = fanStateApp;
    if (fanStateApp == 0){
      SerialArduino.println(300);
    } else if (fanStateApp == 1){
      SerialArduino.println(fanSpeed);
    }
  }
  if (oldDoorStateApp != doorStateApp) {
    oldDoorStateApp = doorStateApp;
    if (doorStateApp == 0){
      digitalWrite(doorPin, HIGH);
    } else if (doorStateApp == 1){
      doorStateDevice = 1;
      digitalWrite(doorPin, LOW);
    }
  }
  
}
