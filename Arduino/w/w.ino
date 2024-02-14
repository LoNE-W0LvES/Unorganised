#include <Adafruit_Thermal.h>
#include "qrcode.h"

// Define the thermal printer settings
#define TX_PIN 1  // Connect the thermal printer's TX pin to this pin on the ESP32
#define BAUD_RATE 19200

Adafruit_Thermal printer(&Serial1);  // Use the appropriate Serial port for your ESP32

String paypalLink = "https://paypal.me/username"; // Insert your PayPal link here



void setup()
{
  Serial.begin(115200);
  Serial1.begin(BAUD_RATE);  // Initialize the serial communication with the thermal printer
  QRCode qrcode;
  printQRCode();
}

void loop()
{
  // Add your looping code here
}

void printQRCode()
{
  uint8_t qrcodeData[qrcode_getBufferSize(3)];
  qrcode_initText(&qrcode, qrcodeData, 3, 0, paypalLink.c_str());

  // Set the printing mode for the thermal printer
  printer.justify('C');
  printer.setSize('L'); // You may need to adjust the size depending on your printer model

  for (uint8_t y = 0; y < qrcode.size; y++)
  {
    for (uint8_t x = 0; x < qrcode.size; x++)
    {
      if (qrcode_getModule(&qrcode, x, y))
      {
        printer.write(Printer::LIGHT);
      }
      else
      {
        printer.write(Printer::DARK);
      }
    }
  }

  // Feed the paper and cut (you may need to adjust these commands based on your printer model)
  printer.feed(4);
  printer.cut();
}