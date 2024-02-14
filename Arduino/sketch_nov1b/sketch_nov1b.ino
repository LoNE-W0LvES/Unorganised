#include <OneWire.h>
#include <DallasTemperature.h>
#include "DHT.h"
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

#define DHTPIN 2
#define DHTTYPE DHT22
#define ONE_WIRE_BUS 3

OneWire oneWire(ONE_WIRE_BUS);

DHT dht(DHTPIN, DHTTYPE);
DallasTemperature sensors(&oneWire);

void setup()
{
  Serial.begin(115200);
	lcd.init();
	lcd.backlight();
	lcd.clear();
  dht.begin();
  sensors.begin();
}

void loop(){ 
  delay(1000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  if (isnan(h)||isnan(t)||isnan(f)) {
    Serial.println("sensor error");
    return;
  }
  sensors.requestTemperatures(); 
  // lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  Humidity: ");
  lcd.print(h);
  lcd.print("%");
  lcd.setCursor(0,1);
  lcd.print("Temp: ");
  lcd.print(t);
  lcd.print("C(");
  lcd.print(f);
  lcd.print("F)");
  lcd.setCursor(4,2);
  lcd.print("Object Temp");
  lcd.setCursor(3,3);
  lcd.print(sensors.getTempCByIndex(0)); 
  lcd.print("C(");
  lcd.print(sensors.getTempFByIndex(0));
  lcd.print("F)");
}
