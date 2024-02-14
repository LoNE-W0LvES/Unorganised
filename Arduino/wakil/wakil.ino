#define led_1 2
#define led_2 3
#define led_3 4
#define led_4 5
#define led_5 6
#define led_6 7

int led[7] = {2, 3, 4, 5, 6, 7, 8};

void setup() {
  for (int i = 0; i < 7; i++){
    pinMode(led[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 7; i++){
    digitalWrite(led[i], LOW);
    delay(200);
  }
  delay(1000);
  for (int i = 0; i < 7; i++){
    digitalWrite(led[i], HIGH);
    delay(200);
  }
  delay(1000);
}
