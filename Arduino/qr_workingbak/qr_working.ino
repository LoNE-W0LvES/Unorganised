
#include "Adafruit_Thermal.h"

#include "HardwareSerial.h"

const byte rxPin = 16;
const byte txPin = 17;

HardwareSerial mySerial(1);
Adafruit_Thermal printer(&mySerial);

void setup() {
  Serial.begin(115200);
  mySerial.begin(19200, SERIAL_8N1, rxPin, txPin);
  printer.begin();
  
  qr_print("Md Nafiur Rahman 170151 no room guest");
  printer.print("\n");
  printer.print("name\n");
  printer.print("roll\n");
  printer.print("room\n");
  printer.print("date\n");
  // printer.feed(3);
  printer.write(0x1D);
  printer.write(0x56);
  printer.write(1);

}

void loop() {
}
