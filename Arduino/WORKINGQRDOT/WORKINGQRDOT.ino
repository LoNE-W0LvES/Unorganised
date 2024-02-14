#include <Arduino.h>
#include <HardwareSerial.h>
#include <Wire.h>
#include "qrcode.h"

QRCode qrcode;
String paypalLink = "https://paypal.me/username";

const byte rxPin = 18;
const byte txPin = 17;

HardwareSerial mySerial(1);

void setup() {
  Serial.begin(115200);
  mySerial.begin(19200, SERIAL_8N1, rxPin, txPin);
  delay(1000);

  // Print a simple text message
  mySerial.print("Hello, Rongta!\n");

  uint8_t qrcodeData[qrcode_getBufferSize(3)];
  qrcode_initText(&qrcode, qrcodeData, 3, 0, paypalLink.c_str() );
  for (uint8_t y = 0; y < qrcode.size; y++)
  {
    for (uint8_t x = 0; x < qrcode.size; x++)
    {
      if (qrcode_getModule(&qrcode, x, y))
      {
          mySerial.print("\u2588\u2588");
      } else {
        mySerial.print("  ");
      }
    }
    mySerial.println("");
  }
  for (int i = 0; i < sizeof(qrcodeData); i++) {
    Serial.print(qrcodeData[i], HEX);
    Serial.print(" ");
  }
  // Feed and cut the paper
  mySerial.write(27);  // ESC command
  mySerial.write('d'); // Paper feed
  mySerial.write(5);   // Feed 5 lines
  mySerial.write(29);  // GS command
  mySerial.write('V'); // Paper feed and cut
  mySerial.write(66);  // Feed length
  mySerial.write(1);   // Cut type (0: full cut, 1: partial cut)

  delay(1000); // Wait for the printing to complete before looping or exiting
}

void loop() {
}
