#include <Adafruit_NeoPixel.h>
#ifdef AVR
#include <avr/power.h>
#endif

#define PIN_NEO_PIXEL 4
#define NUM_PIXELS 7

#define DELAY_INTERVAL 250

Adafruit_NeoPixel NeoPixel(NUM_PIXELS, PIN_NEO_PIXEL, NEO_GRB + NEO_KHZ800);

void setup() {
  NeoPixel.begin();
}

void loop() {
  // first
  NeoPixel.clear();
  for (int pixel = 0; pixel < NUM_PIXELS; pixel++) { 
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(0, 255, 0));
    NeoPixel.show();

    delay(DELAY_INTERVAL);
  }
  NeoPixel.clear();
  // second
  NeoPixel.show();
  delay(2000);
  for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(255, 0, 0));
  }
  NeoPixel.show();
  delay(2000);
  NeoPixel.clear();
  NeoPixel.show();
  delay(2000);
}