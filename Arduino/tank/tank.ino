
#include <Arduino.h>
#include <ArduinoSort.h>
#include <Wire.h> 
#include <LiquidCrystal.h>
#include <HCSR04.h>

#define switchUp 6
#define switchDown 5
#define switchConfirm 8
#define switchMenu 9
#define switchManual 7

#define sonarT 11
#define sonarE 10
#define buzzPin 4
#define motorPin 2

const int rs = 13, en = A1, d4 = A2, d5 = A3, d6 = A4, d7 = A5;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

UltraSonicDistanceSensor hcsr04(sonarT, sonarE);

int waterLev_y, waterLev_x, motor_state, curr_data, waterLev, tnkHeight;
unsigned int  time_y, time_x, time_xy;
float consumed_water, time_diff, amount, waterPerSec;
//int siphon          =0;

int valuesSonar[7] = {};

int measureDistance(){
    for(int & i : valuesSonar){
        i = hcsr04.measureDistanceCm();
        delay(40);
        Serial.println(i);
    }
    sortArray(valuesSonar, 7);
    return valuesSonar[3];
}

int waterLevel() {
    curr_data = (int)((((float)tnkHeight / 1.25) - (((float)measureDistance()) - ((float)tnkHeight / 6))) / ((float)tnkHeight / 125));
    if (curr_data < 0)
        curr_data = 0;
    if (curr_data > 100)
        curr_data = 100;
    return curr_data;
}

int setCLW(int posX, int posY, int value) {
    while (true) {
        if (digitalRead(switchUp) == HIGH) {
            value = value + 1;
            delay(250);
        }
        if(digitalRead(switchDown) == HIGH) {
            delay(200);
            value = value - 1;
        }
        if (value > 999)
            value = 1;
        if (value < 1)
            value = 999;

        lcd.setCursor(posX, posY);

        if (value<100){
            if (value<10)
                lcd.print(" 0"+String(value) + " ");
            else
                lcd.print(" "+String(value) + " ");
        } else {
            lcd.print(String(value) + " ");
        }

        if (digitalRead(switchConfirm) == HIGH) {
            while (true) {
                delay(100);
                if (digitalRead(switchConfirm) == LOW)
                    break;
            }
            break;
        }
    }
    return value;
}


void setCirCu(int tnk_x, int tnk_y) {
    lcd.setCursor(0,0);
    lcd.print("Tank Size=");
    amount = (float)0.000513402015425836 * (float)0.8 * tnk_x * tnk_y * tnkHeight;
    lcd.print(amount);
    lcd.print(" L");
    delay(1500);
}


void pumpStatus(char *str, int usedWater, int motorState) {
    if (motorState == 1) {
        lcd.clear();
        digitalWrite(motorPin, HIGH);
        motor_state = 1;
    } else if (motorState == 0) {
        lcd.clear();
        digitalWrite(motorPin, LOW);
        motor_state = 0;
    }
    lcd.setCursor(13,0);
    lcd.print(str);
    lcd.print("   ");
    lcd.setCursor(0,1);
    lcd.print("Used(L): " + String(usedWater) + "     ");

}


void setup() {
    pinMode(motorPin,OUTPUT);
    pinMode(buzzPin,OUTPUT);
    pinMode(switchMenu, INPUT);
    pinMode(switchConfirm, INPUT);
    pinMode(switchUp, INPUT);
    pinMode(switchDown, INPUT);
    pinMode(switchManual, INPUT);
    delay(200);
    lcd.begin(16, 2);
    lcd.clear();
    Serial.begin(9600);
    Serial.println("GG");
    tnkHeight = 0;
    if (tnkHeight == 0){
        lcd.print("WATER PUMP");
        lcd.setCursor(0, 1);
        lcd.print("Booting");
        delay(1000);
        lcd.clear();
        lcd.print("Keep Tank Empty");
        delay(1000);
        lcd.clear();
        tnkHeight = (int)(floor((double)measureDistance()));
        lcd.print("Height:");
        lcd.print(tnkHeight);
        delay(1000);
        lcd.clear();
        int asd = 0;
        while(true) {
          if (asd == 0){
            lcd.setCursor(2,0);
            lcd.print("Circle Tank");
          } else {
            lcd.setCursor(1,0);
            lcd.print("Rectangle Tank");
          }
          if (digitalRead(switchConfirm) == HIGH) {
            while (true) {
              delay(50);
              if (digitalRead(switchConfirm) == LOW)
                break;
            }
            break;
          }
          if (digitalRead(switchUp) == HIGH) {
            while (true) {
              delay(50);
              if (digitalRead(switchUp) == LOW)
                  break;
            }
            if (asd == 0){
              asd = 1;
              
            } else {
              asd = 0;
            }
            lcd.clear();
          }
        }
        lcd.clear();
        if (asd == 0){
          lcd.setCursor(4,0);
          lcd.print("Hight:");
          int size = setCLW(6, 1, 0);
          setCirCu(size, size);
        } else {
          lcd.setCursor(4,0);
          lcd.print("Hight:");
          int sizex = setCLW(6, 1, 0);
          lcd.clear();
          lcd.setCursor(4,0);
          lcd.print("Weight:");
          int sizey = setCLW(6, 1, 0);
          setCirCu(sizex, sizey);
        }
        waterPerSec = 0;
        consumed_water = 0;
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////
    } else {
        lcd.print("Current Failure!");
        delay(2000);
        waterPerSec = 0;
        consumed_water = 0;
        lcd.clear();
    }
}

void loop() {
    waterLev = waterLevel();
    lcd.setCursor(0,0);
    lcd.print("Water: ");
    if (waterLev<100){
        if (waterLev<10)
            lcd.print(String(waterLev) + "%  ");
        else
            lcd.print(String(waterLev) + "% ");
    } else {
        lcd.print(String(waterLev) + "%");
    }

    if (motor_state == 0){
        pumpStatus("OFF", (int)consumed_water, 2);
    } else if (motor_state == 1){
        pumpStatus("ON", (int)consumed_water, 2);
    }

    if (motor_state == 0) {
        if (waterLev < 15 || digitalRead(switchManual)) {
            time_y = millis();
            if (waterPerSec == 0) {
                Serial.println("First Time");

                pumpStatus("ON", 0, 1);
                waterLev_y = waterLev;
                Serial.println(time_y);
                Serial.println(waterLev_y);
            } else {
                pumpStatus("ON", (int)consumed_water, 1);
            }
        }
    } else if (motor_state == 1) {
        if (waterPerSec == 0) {
            if (waterLev >= 100 || digitalRead(switchManual)) {
                waterLev_x = waterLev;
                time_x = millis();
                waterPerSec = ((waterLev_x - waterLev_y) / (((float)(time_x - time_y)/1000) * (amount / 100)))/10;
                Serial.print("amount = ");
                Serial.println(amount);
                Serial.print("waterPerSec = ");
                Serial.println(waterPerSec);
                consumed_water = amount;
                Serial.println(time_x);
                Serial.println(waterLev_x);
                pumpStatus("OFF", (int)consumed_water, 0);
            }
        } else {
            time_x = millis();
            if (((time_x - time_y)/1000) >= 1){
                time_y = millis();
                consumed_water = consumed_water + waterPerSec;
                pumpStatus("ON", (int)consumed_water, 2);
                Serial.print("waterPerSec = ");
                Serial.println(waterPerSec);
            }
            if (waterLev >= 100 || digitalRead(switchManual)) {
                pumpStatus("OFF", (int)consumed_water, 0);
                Serial.print("consumed_water = ");
                Serial.println(consumed_water);
            }
        }
    }
}
