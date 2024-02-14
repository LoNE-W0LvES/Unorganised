#include "qrcode.h"
#include <HardwareSerial.h>

const byte rxPin = 16;  // Define your RX and TX pins for the printer
const byte txPin = 17;

HardwareSerial mySerial(1);  // Serial connection to your printer

QRCode qrcode;

void setup() {
  mySerial.begin(19200, SERIAL_8N1, rxPin, txPin);
  delay(1000);

  // Generate a random string
  String data = "generateRandomString10"; // Change 10 to the desired length

  // Print the random string as a QR code
  uint8_t qrcodeData[qrcode_getBufferSize(3)];
  qrcode_initText(&qrcode, qrcodeData, 3, 0, data.c_str());

  // Debug: Print the QR code data as text to the serial monitor
  Serial.begin(115200);
  for (int i = 0; i < sizeof(qrcodeData); i++) {
    Serial.print(qrcodeData[i], HEX);
    
    mySerial.print(qrcodeData[i]); // QR code data
    Serial.print(' ');
  }
  Serial.println();
  
  // Now, print the QR code data to the thermal printer
  mySerial.write(0x1D); // Initialize the printer
  mySerial.write('k');  // QR code model
  mySerial.write(3);    // QR code module size
  mySerial.write(0x1D); // Initialize the printer
  mySerial.write('M');  // QR code error correction level (M: 15% or less errors can be corrected)
  mySerial.write(0x1D); // Initialize the printer
  mySerial.write('Q');  // Print QR code
  mySerial.write(0x01); // Model 1
  mySerial.write(0x02); // Auto mode (selects best encoding mode)
  mySerial.write(qrcodeData, sizeof(qrcodeData)); // QR code data
}

void loop() {
  // Your looping code here
}
