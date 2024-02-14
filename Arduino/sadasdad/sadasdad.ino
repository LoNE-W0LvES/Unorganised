#include <Arduino.h>
#include <HardwareSerial.h>
#include <Wire.h>
#include "qrcode.h"

const byte rxPin = 16;
const byte txPin = 17;

HardwareSerial mySerial(1);

QRCode qrcode;
String paypalLink = "https://paypal.me/username";

void setup() {
  Serial.begin(115200);
  mySerial.begin(19200, SERIAL_8N1, rxPin, txPin);
  delay(1000); // Wait for the printer to initialize

  mySerial.write(27); // ESC command
  mySerial.write('3'); // Set line spacing
  mySerial.write(10);   // -2 dots (adjust as needed for tighter overlap)

  uint8_t qrcodeData[qrcode_getBufferSize()];
  qrcode_initText(&qrcode, qrcodeData, 3, 0, paypalLink.c_str() );

  int scale = 2; // Change this for different sizes
  for (uint8_t y = 0; y < qrcode.size; y++)
  {
    for (uint8_t x = 0; x < qrcode.size; x++)
    {
      if (qrcode_getModule(&qrcode, x, y))
      {
          mySerial.write(219);
          mySerial.write(219);
      } else {
        mySerial.print("  ");
      }
    }
    mySerial.print("\n");
  }
  for (int i = 0; i < sizeof(qrcodeData); i++) {
    Serial.print(qrcodeData[i], HEX);
    Serial.print(" ");
  }


  mySerial.write(219);
  mySerial.print("\n");
  mySerial.print("Hello, Rongta!\n");
  mySerial.print("Hello, Rongta!\n");
  
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
