#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
Adafruit_SH1106G display = Adafruit_SH1106G(128, 64, &Wire, -1);


void setup()   {
  Serial.begin(115200);
  delay(250);
  display.begin(0x3c, true);
  dht.begin();
  display.setRotation(2);
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
}


void loop () {
  delay(2000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  if (isnan(h) || isnan(t) || isnan(f)) {
    return;
  }
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(" ");
  display.print("Humidity: ");
  display.print(h);
  display.println("%");
  display.println(" ");
  display.print("Temp: ");
  display.print(t);
  display.print("C (");
  display.print(f);
  display.println("F)");
  display.display();
}
