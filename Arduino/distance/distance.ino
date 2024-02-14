#include <HCSR04.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

Adafruit_SH1106G display = Adafruit_SH1106G(128, 64, &Wire, -1);
HCSR04 hc(A0, A1);

float distance = 0;
float distance_bak[10];

void setup() {

  Serial.begin(115200);
  delay(250);
  display.begin(0x3c, true);
  display.setRotation(2);
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
}



float getMin(float* array, int size) {
  int minimum = array[0];
  for (int i = 0; i < size; i++) {
    if (array[i] < minimum) minimum = array[i];
  }
  return minimum;
}

void loop () {
    display.setCursor(0, 0);
    display.print("Distance: ");
    for (int i = 0; i < 10; i++) {
      delay(50);
      distance = hc.dist();
      if (distance < 0) {
        delay(50);
        distance = hc.dist();
      }
      if (i != 0){
        if (distance > (distance_bak[i-1] + 20)){
            distance_bak[i] = distance_bak[i-1];
        } else {
          distance_bak[i] = distance;
        }
      } else {
          distance_bak[i] = distance;
        }
    }

    display.println(getMin(distance_bak, 10));
    display.display();
    delay(50);
    display.clearDisplay();
}