#include <WiFi.h>
#include <FirebaseESP32.h>

#include <Arduino.h>
#include <GyverDimmer.h>
//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#define WIFI_SSID "Lab"
#define WIFI_PASSWORD "cselab@221"
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;


DimmerBresMulti<2> dim;
char input_char;
String fan_string;
#define swPin 5
#define lightPin 4
#define doorPin 6
int fan_state;

void isr() {
    dim.tick(); // trigger tick in null detector interrupt
}

void setup() {
  Serial.begin(115200);
  pinMode(lightPin, OUTPUT);
  pinMode(doorPin, OUTPUT);
  pinMode(swPin, INPUT);
  digitalWrite(doorPin, HIGH);
  attachInterrupt(0, isr, RISING);
  dim.attach(0, 3);   // channel 0, pin 3
}

void loop() {
  while(Serial.available()>0){
    input_char = Serial.read();
    switch (input_char) {
      case 'a':
        digitalWrite(lightPin, LOW);
        break;
      case 'b':
        digitalWrite(lightPin, HIGH);
        break;
      case 'c':
        fan_state = 0;
        dim.write(0, 0);
        break;
      case 'd':
        fan_state = 1;
        break;
      case 'e':
        digitalWrite(doorPin, HIGH);
        break;
      case 'f':
        digitalWrite(doorPin, LOW);
        break;  
      case 'g':
        if (fan_state == 1){
          dim.write(0, 0);
        }
        break;
      case 'h':
        if (fan_state == 1){
          dim.write(0, 25);
        }
        break;
      case 'i':
        if (fan_state == 1){
          dim.write(0, 50);
        }
        break;
      case 'j':
        if (fan_state == 1){
          dim.write(0, 75);
        }
        break;
      case 'k':
        if (fan_state == 1){
          dim.write(0, 100);
        }
        break;
      case 'l':
        if (fan_state == 1){
          dim.write(0, 125);
        }
        break;
      case 'm':
        if (fan_state == 1){
          dim.write(0, 150);
        }
        break;
      case 'n':
        if (fan_state == 1){
          dim.write(0, 175);
        }
        break;
      case 'o':
        if (fan_state == 1){
          dim.write(0, 200);
        }
        break;
      case 'p':
        if (fan_state == 1){
          dim.write(0, 225);
        }
        break;
      case 'q':
        if (fan_state == 1){
          dim.write(0, 255);
        }
        break;
    }
    input_char = 'z';
  }

  if (digitalRead(swPin) == HIGH) {
      while (true) {
          if (digitalRead(swPin) == LOW)
              break;
      }
      Serial.println('r');
  }
}
