#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#define PIN_1 7
#define PIN_2 5
#define PIN_3 6
#define PIN_4 4

#define NUM_PIXELS1 36
#define NUM_PIXELS2 28
#define NUM_PIXELS3 6
#define NUM_PIXELS4 84

#define DELAY_INTERVAL 250

Adafruit_NeoPixel NeoPixel1(NUM_PIXELS1, PIN_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel NeoPixel2(NUM_PIXELS2, PIN_2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel NeoPixel3(NUM_PIXELS3, PIN_3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel NeoPixel4(NUM_PIXELS4, PIN_4, NEO_GRB + NEO_KHZ800);

void setup() {
  NeoPixel1.begin();
  NeoPixel2.begin();
  NeoPixel3.begin();
  NeoPixel4.begin();
}

void loop() {
  // first
  NeoPixel1.clear();
  NeoPixel2.clear();
  NeoPixel3.clear();
  NeoPixel4.clear();
  for (int pixel = 0; pixel < NUM_PIXELS4; pixel++) { 
    if (pixel < NUM_PIXELS1) {
      NeoPixel1.setPixelColor(pixel, NeoPixel1.Color(0, 255, 0));
    }
    if (pixel < NUM_PIXELS2) {
      NeoPixel2.setPixelColor(pixel, NeoPixel2.Color(0, 255, 0));
    }
    if (pixel < NUM_PIXELS3) {
      NeoPixel3.setPixelColor(pixel, NeoPixel3.Color(0, 255, 0));
    }
    if (pixel < NUM_PIXELS4) {
      NeoPixel4.setPixelColor(pixel, NeoPixel4.Color(0, 255, 0));
    }
    NeoPixel1.show();
    NeoPixel2.show();
    NeoPixel3.show();
    NeoPixel4.show();

    delay(DELAY_INTERVAL);
  }
  NeoPixel1.clear();
  NeoPixel2.clear();
  NeoPixel3.clear();
  NeoPixel4.clear();
  // second
  NeoPixel1.show();
  NeoPixel2.show();
  NeoPixel3.show();
  NeoPixel4.show();
  delay(2000);
  for (int pixel = 0; pixel < NUM_PIXELS4; pixel++) {
    if (pixel < NUM_PIXELS1) {
      NeoPixel1.setPixelColor(pixel, NeoPixel1.Color(255, 0, 0));
    }
    
    if (pixel < NUM_PIXELS2) {
      NeoPixel2.setPixelColor(pixel, NeoPixel2.Color(255, 0, 0));
    }
    if (pixel < NUM_PIXELS3) {
      NeoPixel3.setPixelColor(pixel, NeoPixel3.Color(255, 0, 0));
    }
    if (pixel < NUM_PIXELS4) {
      NeoPixel4.setPixelColor(pixel, NeoPixel4.Color(255, 0, 0));
    }
  }
  NeoPixel1.show();
  NeoPixel2.show();
  NeoPixel3.show();
  NeoPixel4.show();
  delay(2000);
}
