#include <WiFi.h>
#include <FirebaseESP32.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include <Servo.h>
#include "DHT.h"

#define doorbell 25
#define lightPin  32
#define servoPin 33

#define DHTPIN 21
#define DHTTYPE DHT22

#define rSw1 12
#define rSw2 14

#define WIFI_SSID "Lab"
#define WIFI_PASSWORD "cselab@221"
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"

int doorBellDevice, doorStateApp,  fanSpeed, fanStateApp, lightStateApp, takePhoto, fireAlert;
int oldDoorStateApp = 2;
int oldFanStateApp = 2;
int oldLightStateApp = 2;
int oldFanSpeed = 111;
int dataUpdate = 1;
int firstDataUpdate = 1;
char input_char;
unsigned long timeX, timeY, timeXT, timeDHT;
int timeSwitch = 0;
float h, t, f, hif, hic;
FirebaseData fbdo;
FirebaseData updateDb;
FirebaseAuth auth;
FirebaseConfig config;
Servo myservo;
DHT dht(DHTPIN, DHTTYPE);
HardwareSerial SerialEspCam(1);
HardwareSerial SerialArduino(2);
void setup()
{
  Serial.begin(115200);
  SerialEspCam.begin(115200);
  SerialArduino.begin(115200);
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
  myservo.attach(servoPin);

  pinMode(lightPin, OUTPUT);
  pinMode(doorbell, INPUT);  
  timeXT = millis();
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
      Firebase.getInt(fbdo, "/states/takePhoto");
      takePhoto = fbdo.to<int>();
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
        hif = dht.computeHeatIndex(f, h);
        hic = dht.computeHeatIndex(t, h, false);
        Firebase.setFloat(fbdo, "/states/roomHum", h);
        Firebase.setFloat(fbdo, "/states/roomTemp", t);
        if (t > 50){
          fireAlert = 1;
          Firebase.setInt(fbdo, "/states/fireAlert", 1);
        }
        if (t < 50) && (fireAlert == 1){
          fireAlert = 0;
          Firebase.setInt(fbdo, "/states/fireAlert", 0);
        }
        Firebase.setFloat(fbdo, "/states/roomTempFer", f);
        Firebase.setFloat(fbdo, "/states/heatIndexFer", hif);
        Firebase.setFloat(fbdo, "/states/heatIndexCel", hic);  
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

    if (takePhoto == 1){
      takePhoto = 0;
      SerialEspCam.print("t");
    }
    if (digitalRead(doorbell) == HIGH) {
      while (true) {
          if (digitalRead(doorbell) == LOW)
              break;
      }
      Firebase.setInt(fbdo, "/states/doorBellDevice", 1);
      SerialEspCam.print("t");
      timeSwitch = 1;
      timeX = millis();
    } 
    timeY = millis();
    if (timeSwitch = 1) {
      if((timeY - timeX)> 30000){
        Firebase.setInt(fbdo, "/states/doorBellDevice", 0);
        timeSwitch = 0;
      }
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
      myservo.write(0);
    } else if (doorStateApp == 1){
      myservo.write(180);
    }
  }
  
}
