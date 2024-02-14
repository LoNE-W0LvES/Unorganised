

void setup() {
NeoPixel.begin();

}

void loop() {
  for (int pixel=0; pixel < 4; pixel++) {
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(255, 0, 0));
    NeoPixel.show();
    delay(500);
  }
  for (int pixel=0; pixel < 4; pixel++) {
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(0, 0, 0));
    NeoPixel.show();
    delay(500);
  }
}
