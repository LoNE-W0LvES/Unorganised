
#include <SPI.h>
#include <MFRC522.h>
#include <Preferences.h>
Preferences preferences;

constexpr uint8_t RST_PIN = D2;
constexpr uint8_t SS_PIN = D8;

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;

String tag;
String newTag[100];
int setMode = 0;
int count = 0;
int tagFound = 0;
int doorOpen = 0;
unsigned long timeX;
int doorOpened = 0;

void setup() {
  pinMode(D1, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D3, INPUT);
  digitalWrite(D1, HIGH);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.begin(9600);
  preferences.begin("tags", false);
  count = preferences.getInt("count", 0);
  for (byte i = 0; i <= count; i++) {
    newTag[i] = preferences.getString("tag" + i, "");
  }
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {
  if (rfid.PICC_IsNewCardPresent()){
    if (rfid.PICC_ReadCardSerial()) {
      for (byte i = 0; i < 4; i++) {
        tag += rfid.uid.uidByte[i];
      }
      rfid.PICC_HaltA();
      rfid.PCD_StopCrypto1();
      if (tag == "181023027") {
        if (setMode == 0) {
          setMode = 1;
          digitalWrite(LED_BUILTIN, LOW);
        }else {
          setMode = 0;
          digitalWrite(LED_BUILTIN, HIGH);
        }
      } else {
        if (setMode == 1) {
          for (byte i = 0; i <= count; i++) {
            if (tag == newTag[i]) {
              tagFound = 1;
              doorOpen = 1;
              timeX = millis();
              Serial.println("tag found");
              break;
            }
          }
          if ((tagFound == 0) && (tag != "181023027")) {
            Serial.println("tag not found");
            preferences.putString("tag" + count, tag);
            newTag[count] = tag;
            count++;
            preferences.putInt("count", count);
            digitalWrite(LED_BUILTIN, HIGH);
            delay(200);
            digitalWrite(LED_BUILTIN, LOW);
          }
          
        }
        tagFound = 0;
      }
      for (byte i = 0; i <= count; i++) {
        if (tag == newTag[i]) {
          doorOpen = 1;
          timeX = millis();
        }
      }
      tag = "";
    }
  }
  if ((digitalRead(D3) == LOW) && (setMode == 1)) {
    preferences.clear();
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    ESP.restart();
  }
  if ((doorOpen == 1) && (doorOpened == 0)) {
    digitalWrite(D1, LOW);
    Serial.println("Door opened");
    doorOpened = 1;
    doorOpen = 0;
  }
  if ((millis() - timeX) >= 10000){
    if (doorOpened == 1) {    
      doorOpened = 0;
      digitalWrite(D1, HIGH);
      Serial.println("Door closed");
    }
  }
}