#include <Arduino.h>

String input_string;
#define swPin 5
#define lightPin 4
#define relayPin 6

void setup() {
  Serial.begin(115200);
  pinMode(lightPin, OUTPUT);
  pinMode(relayPin, OUTPUT);
  pinMode(swPin, INPUT);
  digitalWrite(relayPin, HIGH);
}

void loop() {
  while(Serial.available()>0){
    input_string = Serial.readString();
    input_string.trim();
    if (input_string.indexOf("lightStateApp: 1") != -1) {
      digitalWrite(lightPin, HIGH);
    }
    if (input_string.indexOf("lightStateApp: 0") != -1) {
      digitalWrite(lightPin, LOW);
    }
    if (input_string.indexOf("doorStateApp: 1") != -1) {
      digitalWrite(relayPin, LOW);
    }
    if (input_string.indexOf("doorStateApp: 0") != -1) {
      digitalWrite(relayPin, HIGH);
    }
  }

  if(digitalRead(swPin) == HIGH){
    Serial.print("doorBell");
    Serial.println();
  }
}
