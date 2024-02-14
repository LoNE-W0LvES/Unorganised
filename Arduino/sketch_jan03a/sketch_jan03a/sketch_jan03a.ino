#include <GyverDimmer.h>
#include <GyverTimers.h>

#define D_PIN 5
int buf;
int outVal = 0;
Dimmer<D_PIN> dim;

void setup() {
  Serial.begin(115200);
  attachInterrupt(0, isr, RISING);
  Timer2.enableISR();
}

void isr() {
  if (dim.tickZero()) Timer2.setPeriod(dim.getPeriod());
  else Timer2.restart();
}

ISR(TIMER2_A) {
  dim.tickTimer();
  Timer2.stop();
}

void loop() {
  if (Serial.available())
  {
    buf = Serial.parseInt();
    if (buf != 0)
      outVal = buf;
    if (buf == 300){
      outVal = 0;
    }
    delay(200);
  }
  dim.write(outVal);
  delay(100);
}
