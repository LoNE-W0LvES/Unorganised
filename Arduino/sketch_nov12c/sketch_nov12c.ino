#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>
#include <HCSR04.h>

#define TYP_NEO NEO_GRB + NEO_KHZ800
#define DELAY_INTERVAL 250

HCSR04 hc[4] = {HCSR04(5, 6), HCSR04(3, 4), HCSR04(A4, A3), HCSR04(7, 8)};
Adafruit_NeoPixel NeoPixel = Adafruit_NeoPixel(4, A2, TYP_NEO);
byte readCard[4];
String tag_UID = "2874034";
int ultrasonic[4] = {0, 0, 0, 0};
int ultra[4] = {0, 0, 0, 0};
String tagID = "";
MFRC522 mfrc522(10, 9);
int sw = 0;

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  NeoPixel.begin();
  randomSeed(analogRead(0));
  for (int s=0; s < 4; s++) {
    NeoPixel.setPixelColor(s, NeoPixel.Color(0, 255, 0));
  }
  NeoPixel.show();
}

void loop() {
  int count = 0;
  for (int s=0; s < 4; s++) {
    if ((hc[s].dist() < 5.5) && (hc[s].dist() > 2)) {
      ultrasonic[s] = 1;
    } else {
      ultrasonic[s] = 0;
    }
  }
  for (int s=0; s < 4; s++) {
    if (ultrasonic[s] == 1) {
      count++;
    }
  }
  if (count == 1){
    for (int s=0; s < 4; s++) {
      if (ultrasonic[s] == 1) {
        NeoPixel.setPixelColor(s, NeoPixel.Color(0, 255, 0));
      } else {
        NeoPixel.setPixelColor(s, NeoPixel.Color(255, 0, 0));
      }
    }
    NeoPixel.show();
    delay(5000);
  }
  if (count == 0){
    for (int s=0; s < 4; s++) {
      NeoPixel.setPixelColor(s, NeoPixel.Color(0, 255, 0));
    }
    NeoPixel.show();
  }
  if ((count > 1) && (sw == 0)){
    sw = 1;
    int randNumber = random(4);
    for (int s=0; s < 4; s++) {
      NeoPixel.setPixelColor(s, NeoPixel.Color(255, 0, 0));
    }
    while (true){
      if (ultrasonic[randNumber] == 1) {
        NeoPixel.setPixelColor(randNumber, NeoPixel.Color(0, 255, 0));
        break;
      }
      randNumber = random(4);
    }
    NeoPixel.show();
    delay(5000);
  } else if (count < 2) {
    sw = 0;
  }

  while (readID()) {
    if (tagID == tag_UID) {
      for (int s=0; s < 4; s++) {
        if (s == 2) {
          NeoPixel.setPixelColor(s, NeoPixel.Color(0, 255, 0));
        } else {
          NeoPixel.setPixelColor(s, NeoPixel.Color(255, 0, 0));
        }
      }
      NeoPixel.show();
      delay(5000);
    }
  }
}


boolean readID(){
  if ( ! mfrc522.PICC_IsNewCardPresent()) { return false; }
  if ( ! mfrc522.PICC_ReadCardSerial()) { return false; }
  tagID = "";
  for ( uint8_t i = 0; i < 4; i++) { tagID.concat(String(mfrc522.uid.uidByte[i], HEX)); }
  tagID.toUpperCase();
  Serial.println(tagID);
  mfrc522.PICC_HaltA();
  return true;
}