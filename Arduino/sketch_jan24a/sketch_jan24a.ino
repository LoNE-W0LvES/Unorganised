#include <Wire.h>
#include "RTClib.h"
#include <LiquidCrystal.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
LiquidCrystal lcd(3, 4, 5, 6, 7, 8);
RTC_DS1307 RTC;


#define motorPin 10
#define sanitizeLed 9
#define removeLed 2
#define down_button A2
#define up_button 11
#define SENSOR_PIN 12

unsigned long duration, time_x, time_y, time_sw1, time_sw2;
volatile int s, m, h, h_12, ap, d, mo, ye;
int pos_neg = 1;
int confirm = 7;
float distance;
float s_val = 0.017;
bool sw1 = false;
char daysOfTheWeek[7][12] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
byte customChar[] = {B01110, B01010, B01110, B00000, B00000, B00000, B00000, B00000};
char *hour_mode;

int distance_bak[10];
int new_hour, h_mode;
int am_temp = 34;
double o_temp= 98.5;


int avgx(int* arraya, int size) {
  int x = 0;
  for (int i = 0; i < size; i++) {
    if (arraya[i] == 0){
      x += 1;
    }
  }
  if (x > 5) {
    return 0;
  } else {
    return 1;
  }
}

int measureDistance() {
  for (int i = 0; i < 10; i++) {
    delay(10);
    int distx = digitalRead(SENSOR_PIN);
    if (distx == 1) {
      delay(10);
      distx = digitalRead(SENSOR_PIN);
    }
    distance_bak[i] = distx;
  }

  int state = avgx(distance_bak, 10);


  if (state == 0){
    return 5;
  } else {
    return 16;
  }
}

void showTemp() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(" Your Body Temp ");
    lcd.setCursor(4, 1);
    if (o_temp < 10) {
        lcd.print("  ");
        lcd.print(o_temp);
    } else if (o_temp > 10 && o_temp < 100) {
        lcd.print(" ");
        lcd.print(o_temp);
    } else
        lcd.print(o_temp);

    lcd.write((byte) 00);
    lcd.print("F");
    delay(1200);
}

void setup() {
    Wire.begin();
    RTC.begin();
  lcd.begin(16, 2);
    Serial.begin(9600);
    if (!mlx.begin()) {
      Serial.println("Error connecting to MLX sensor. Check wiring.");
      while (1);
    };
    if (!RTC.isrunning())
        RTC.adjust(DateTime(__DATE__, __TIME__));
    pinMode(motorPin, OUTPUT);
    pinMode(sanitizeLed, OUTPUT);
    pinMode(removeLed, OUTPUT);
    pinMode(up_button, INPUT);
    pinMode(down_button, INPUT);
    pinMode(SENSOR_PIN, INPUT);
    time_x = 0;
    lcd.createChar(00, customChar);
    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print("    Welcome     ");
    delay(1000);

}

void loop() {
    distance = measureDistance();
    am_temp = mlx.readAmbientTempC();
    o_temp= mlx.readObjectTempF();
    if (distance < 15) {
        if (time_x == 0) {
            time_x = millis();
            sw1 = true;
            lcd.clear();
            digitalWrite(sanitizeLed, LOW);
            digitalWrite(removeLed, LOW);
            lcd.setCursor(0, 0);
            lcd.print(" AUTOMATIC HaND");
            lcd.setCursor(0, 1);
            lcd.print("SANITIZERisReady");
            delay(1000);
            lcd.clear();
            digitalWrite(sanitizeLed, HIGH);
            digitalWrite(removeLed, LOW);
            digitalWrite(motorPin, HIGH);
            lcd.setCursor(0, 0);
            lcd.print("***SANITIZING***");
            lcd.setCursor(0, 1);
            lcd.print("******Busy********");
            delay(10);
        }
        while ((time_y - time_x) <= 10000 && distance < 10) {
            distance = measureDistance();
            time_y = millis();
        }
        time_y = millis();
        if ((time_y - time_x) >= 10000) {
            lcd.clear();
            digitalWrite(sanitizeLed, LOW);
            digitalWrite(removeLed, HIGH);
            delay(100);
            digitalWrite(motorPin, LOW);
            distance = measureDistance();
            while (distance < 10) {
                delay(100);
                lcd.setCursor(0, 0);
                lcd.print(" Please  Remove ");
                lcd.setCursor(0, 1);
                lcd.print("  Your Hand!!!  ");
                time_x = 0;
                sw1 = false;
                distance = measureDistance();
            }
            digitalWrite(removeLed, LOW);
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("    Thanks     ");
            delay(1000);
            showTemp();
            delay(3800);
            lcd.clear();
        }
    } else {
        if (sw1) {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("  Hand is not   ");
            lcd.setCursor(0, 1);
            lcd.print("   Position.    ");
            digitalWrite(sanitizeLed, LOW);
            digitalWrite(removeLed, LOW);
            digitalWrite(motorPin, LOW);
            delay(1200);
            showTemp();
            time_x = 0;
            sw1 = false;
            lcd.clear();
        }

        DateTime now = RTC.now();

        lcd.setCursor(0, 0);
        if (now.day() < 10)
            lcd.print('0');
        lcd.print(now.day(), DEC);
        lcd.print('/');
        if (now.month() < 10)
            lcd.print('0');
        lcd.print(now.month(), DEC);
        lcd.print('/');
        lcd.print(now.year(), DEC);
        lcd.print("  " + String(am_temp));
        lcd.setCursor(11, 0);
        if (am_temp < 10)
            lcd.print(" 0" + String(am_temp));
        else if (am_temp > 10 && am_temp < 100)
            lcd.print(" " + String(am_temp));

        lcd.write((byte) 00);
        lcd.print("C");

        if (now.hour() < 12) {
            new_hour = now.hour();
            hour_mode = " AM";
        } else {
            new_hour = now.hour() - 12;
            hour_mode = " PM";
        }
        lcd.setCursor(0, 1);
        lcd.print(daysOfTheWeek[now.dayOfTheWeek()]);
        lcd.print("  ");
        if (new_hour == 0)
            new_hour = 12;
        if (new_hour < 10)
            lcd.print('0');
        lcd.print(new_hour, DEC);
        lcd.print(':');
        if (now.minute() < 10)
            lcd.print('0');
        lcd.print(now.minute(), DEC);
        lcd.print(':');
        if (now.second() < 10)
            lcd.print('0');
        lcd.print(now.second(), DEC);
        lcd.print(hour_mode);
    }
}
//===========================Modified by WoLvES=============================
