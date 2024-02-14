#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

#define switchUp    4
#define switchDown  5
#define switchStop  3
#define startCount  2
#define heter       6
unsigned long timeX, timeXY, timeZ, t_s, timeY;
int seconds = 0;
int minutes = 0;
int hours = 0;
int startDevice = 0;
int t_set = 0, Start = 0, asd = 0;
int seconds0 = 0;
int minutes0 = 0;
int hours0 = 0;
int pause = 0;
int oldStartDevice = 3;

byte customChar0[] = {B11110, B11110, B11110, B11110, B11110, B11110, B11110, B11110};
byte customChar1[] = {B01111, B01111, B01111, B01111, B01111, B01111, B01111, B01111};
byte customChar2[] = {B01001, B01001, B10010, B11111, B11111, B11111, B11111, B11110};
byte customChar3[] = {B01001, B01001, B10010, B11111, B11111, B11111, B11111, B01111};

int setTime(int maxValue) {
    int value = 0;
    while (true) {
        if (digitalRead(switchUp) == HIGH) {
            value = value + 1;
            delay(250);
        }
        if(digitalRead(switchDown) == HIGH) {
            delay(200);
            value = value - 1;
        }
        if (value > maxValue)
            value = 0;
        if (value < 0)
            value = maxValue;

        lcd.setCursor(6, 1);
        if (value<10)
            lcd.print(" 0" + String(value) + " ");
        else
            lcd.print(" " + String(value) + " ");

        if (digitalRead(startCount) == HIGH) {
            while (true) {
                delay(100);
                if (digitalRead(startCount) == LOW)
                    break;
            }
            break;
        }
    }
    return value;
}

void setup() {
  pinMode(switchUp, INPUT);
  pinMode(switchDown, INPUT);
  pinMode(switchStop, INPUT);
  pinMode(startCount, INPUT);
  pinMode(heter, OUTPUT);
  lcd.init();
  lcd.createChar(0, customChar0);
  lcd.createChar(1, customChar1);
  lcd.createChar(2, customChar2);
  lcd.createChar(3, customChar3);
  lcd.home();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("    WELCOME!    ");
  delay(1000);
  lcd.clear();
}

void printLcd(int value) {
  if (value < 10)
    lcd.print("0");
  lcd.print(value);
}

void loop() {
  // stop code
  if (digitalRead(switchStop) == HIGH) {
    while (true) {
        delay(100);
        if (digitalRead(switchStop) == LOW)
            break;
    }
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Stopped . . . ");
    digitalWrite(heter, LOW);
    startDevice = 0;
    oldStartDevice = startDevice;
    t_s = 0;
    delay(1000);
    lcd.clear();
  }
  // start code
  if (digitalRead(startCount) == HIGH) {
      while (true) {
          delay(100);
          if (digitalRead(startCount) == LOW)
              break;
      }
      if (t_s == 0) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("      Hour      ");
        hours = setTime(23);
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("    Minutes     ");
        minutes = setTime(60);
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("    Seconds     ");
        seconds = setTime(60);
        t_s = ((((hours * 60) + minutes) * 60) + seconds);
        startDevice = 1;
        timeX = millis();
        timeY = millis();
        lcd.clear();
      }
  }
  // pause code
  if (digitalRead(switchDown) == HIGH) {
    while (true) {
        delay(100);
        if (digitalRead(switchDown) == LOW)
            break;
    }
    if (t_s != 0) {
      if (pause == 0){
        pause = 1;
        timeXY = (millis() - timeX)/1000;
        t_s = t_s - timeXY;
        startDevice = 2;
        oldStartDevice = startDevice;
        digitalWrite(heter, LOW);
        lcd.setCursor(13, 0);
        lcd.write(0);
        lcd.write(1);
        lcd.setCursor(13, 1);
        lcd.print("   ");
        lcd.setCursor(0, 1);
        lcd.print("   ");
      } else {
        pause = 0;
        timeX = millis();
        startDevice = 1;
      }
    }
  }
  // restart
  if (digitalRead(switchUp) == HIGH) {
    while (true) {
        delay(100);
        if (digitalRead(switchUp) == LOW)
            break;
    }
    if ((hours !=0) || (minutes !=0) || (seconds !=0)) {
      t_s = ((((hours * 60) + minutes) * 60) + seconds);
      startDevice = 1;
      timeX = millis();
      timeY = millis();
      lcd.clear();
    }
  }

  if (startDevice == 1) {
    if (oldStartDevice != startDevice){
      oldStartDevice = startDevice;
      digitalWrite(heter, HIGH);
      lcd.setCursor(14, 1);
      lcd.write(3);
      lcd.write(2);
      lcd.setCursor(0, 1);
      lcd.write(3);
      lcd.write(2);
    }
    
    timeXY = (millis() - timeX)/1000;
    if (timeXY <= t_s){
      timeZ = t_s - timeXY;
      seconds0 = timeZ % 60;
      timeZ = (timeZ - seconds0)/60;
      minutes0 = (timeZ) % 60;
      hours0 = (timeZ - minutes0)/60;
      lcd.setCursor(4, 0);
      lcd.print("HH:MM:SS         ");
      lcd.setCursor(4, 1);
      printLcd(hours0);
      lcd.print(":");
      printLcd(minutes0);
      lcd.print(":");
      printLcd(seconds0);
    } else {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Done . . . ");
      digitalWrite(heter, LOW);
      startDevice = 0;
      t_s = 0;
      delay(1000);
      lcd.clear();
    }
  } else if (startDevice == 0) {
    oldStartDevice = startDevice;
    lcd.setCursor(0, 0);
    lcd.print("      UV-C      ");
    lcd.setCursor(0, 1);
    lcd.print("   STERILIZER   ");
  }
}