#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

int sensorA = A0;
int led1 = 12;
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);
	lcd.init();
	lcd.backlight();
	lcd.clear();
  pinMode(sensorA, INPUT);
  pinMode(led1, OUTPUT);
}

void loop() {
  float moisture_percentage;
  int sensor_analog;
  sensor_analog = analogRead(sensorA);
  moisture_percentage = ( 100 - ( (sensor_analog/1023.00) * 100 ) );
  lcd.setCursor(0,0);
  lcd.print("Moisture:");
  if (moisture_percentage < 99.99) {
    lcd.print(" ");
  }
  lcd.print(moisture_percentage);
  lcd.print("%");
  delay(1000);
}
