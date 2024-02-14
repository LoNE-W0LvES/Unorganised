#include <SevSeg.h>

#define irpin A0

SevSeg sevseg;
int count = 0;

void setup() {
  Serial.begin(115200);
  byte numDigits = 4;
  byte digitPins[] = {9, 10, 11, 12, 13};
  byte segmentPins[] = {2, 3, 4, 5, 6, 7, 8};
  bool resistorsOnSegments = false;
  byte hardwareConfig = COMMON_CATHODE;
  bool updateWithDelays = false;
  bool leadingZeros = false;
  bool disableDecPoint = true;
  sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments,
  updateWithDelays, leadingZeros, disableDecPoint);
  sevseg.setBrightness(90);
  pinMode(irpin, INPUT);
}

void loop() {
  sevseg.refreshDisplay();
  sevseg.setNumber(count, 0);
  Serial.println(count);
  if (digitalRead(irpin) == false) {
    while (true) {
      sevseg.refreshDisplay();
      sevseg.setNumber(count, 0);
      if (digitalRead(irpin) == true){
        delay(100);
        break;
      }
    }
    count += 1;
    delay(100);
  }
}