byte sensor[6] = {A0, A1, A2, A3, A4, A5};
byte led[7] = {2, 3, 4, 5, 6, 7, 8};

byte s[] = {0, 0, 0, 0, 0, 0};
byte arr[] = {0, 0, 0, 0, 0, 0, 0};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 6; i++){
    pinMode(sensor[i], INPUT);
  }
  for (int i = 0; i < 7; i++){
    pinMode(led[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 6; i++){
    s[i] = analogRead(sensor[i]);
  }

  if (s[5] > 0) {
    s[4] = 10;
    arr[5] = 1;
    arr[6] = 1;
  } else {
    arr[5] = 0;
    arr[6] = 0;
  }

  if (s[4] > 5) {
    s[3] = 10;
    arr[4] = 1;
  } else {
    arr[4] = 0;
  }

  if (s[3] > 5) {
    s[2] = 10;
    arr[3] = 1;
  } else {
    arr[3] = 0;
  }

  if (s[2] > 5) {
    s[1] = 35;
    arr[2] = 1;
  } else {
    arr[2] = 0;
  }

  if (s[1] > 30) {
    s[0] = 10;
    arr[1] = 1;
  } else {
    arr[1] = 0;
  }

  if (s[0] > 5) {
    arr[0] = 1;
  } else {
    arr[0] = 0;
  }

  for (int i = 0; i < 7; i++){
    if (arr[i] == 1){
      digitalWrite(led[i], HIGH);
    } else {
      digitalWrite(led[i], LOW);
    }
  }
  delay(100);
}
