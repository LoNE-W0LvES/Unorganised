#include <WiFi.h>
#include <FirebaseESP32.h>

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#define WIFI_SSID "Lab"
#define WIFI_PASSWORD "cselab@221"
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"
FirebaseData fbdo;
FirebaseData doorStateDb;
FirebaseData fanStateDb;
FirebaseData lightStateDb;
FirebaseData fanSpeedDb;
FirebaseAuth auth;
FirebaseConfig config;

int doorBellDevice, doorStateApp,  fanSpeed, fanStateApp, lightStateApp, takePhoto;
int firstDataUpdate = 1;
char input_char;

unsigned long timeX, timeY;
int timeSwitch = 0;

void setup()
{
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
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
  if (!Firebase.beginStream(lightStateDb, "/states/lightStateApp")){
    Serial.printf("sream begin error, %s\n\n", lightStateDb.errorReason().c_str());
  }
  if (!Firebase.beginStream(fanStateDb, "/states/fanStateApp")){
    Serial.printf("sream begin error, %s\n\n", fanStateDb.errorReason().c_str());
  }
  if (!Firebase.beginStream(doorStateDb, "/states/doorStateApp")){
    Serial.printf("sream begin error, %s\n\n", doorStateDb.errorReason().c_str());
  }
  if (!Firebase.beginStream(fanSpeedDb, "/states/fanSpeed")){
    Serial.printf("sream begin error, %s\n\n", fanSpeedDb.errorReason().c_str());
  }
}

void loop()
{
  if(Serial.available()>0){
    input_char = Serial.read();
  }
  if (Firebase.ready()) {
    if (!Firebase.readStream(lightStateDb))
      Serial.printf("sream read error, %s\n\n", lightStateDb.errorReason().c_str());
    if (lightStateDb.streamAvailable()) {
//      Firebase.getInt(lightStateDb, "/states/lightStateApp");
      lightStateApp = lightStateDb.intData();
      if (lightStateApp == 0){
//        digitalWrite(lightPin, LOW);
        Serial.print("a");
        Firebase.setInt(fbdo, "/states/lightStateDevice", 0);
      } else if (lightStateApp == 1){
//        digitalWrite(lightPin, HIGH);
        Serial.print("b");
        Firebase.setInt(fbdo, "/states/lightStateDevice", 1);
      }
    }
    
    if (!Firebase.readStream(fanStateDb))
      Serial.printf("sream read error, %s\n\n", fanStateDb.errorReason().c_str());
    if (fanStateDb.streamAvailable()) {

      fanStateApp = fanStateDb.intData();
      if (fanStateApp == 0){
        Serial.print("c");
        Firebase.setInt(fbdo, "/states/fanStateDevice", 0);
      }
      if (fanStateApp == 1){
        Serial.print("d");
        Firebase.setInt(fbdo, "/states/fanStateDevice", 1);
      }
    }
    if (!Firebase.readStream(doorStateDb))
      Serial.printf("sream read error, %s\n\n", doorStateDb.errorReason().c_str());
    if (doorStateDb.streamAvailable()) {
      doorStateApp = doorStateDb.intData();
      if (doorStateApp == 0){
        Serial.print("e");
        Firebase.setInt(fbdo, "/states/doorStateDevice", 0);
      }
      if (doorStateApp == 1){
        Serial.print("f");
        Firebase.setInt(fbdo, "/states/doorStateDevice", 1);
      }
    }
    if (!Firebase.readStream(fanSpeedDb))
      Serial.printf("sream read error, %s\n\n", fanSpeedDb.errorReason().c_str());
    if (fanSpeedDb.streamAvailable()) {
      fanSpeed = fanSpeedDb.intData();
      if (fanStateApp == 1) {
//        dim.write(0, fanSpeed);
         Serial.print(fanSpeed);
      }
    }
  }
}