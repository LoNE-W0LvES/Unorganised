#include "HardwareSerial.h"
#define controlPin 12

const byte rxPin = 17;
const byte txPin = 16;
HardwareSerial mySerial(1);


void setup() {
  Serial.begin(115200);
  mySerial.begin(9600, SERIAL_8N1, rxPin, txPin);
  pinMode(controlPin, OUTPUT);
  digitalWrite(controlPin, HIGH);

}

void loop() {
  while(mySerial.available()){
    char c = mySerial.read();
    Serial.println(c);
  }
}

