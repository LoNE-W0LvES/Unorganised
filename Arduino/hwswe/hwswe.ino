#include "qrcode.h"
#include <Adafruit_Thermal.h>

#include "HardwareSerial.h"
#define BAUD_RATE 19200


#define TX_PIN 17 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 16 // Arduino receive   GREEN WIRE   labeled TX on printer

HardwareSerial mySerial(2); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor

QRCode qrcode;

void setup() {
    Serial.begin(115200);
    mySerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);

    // Create the QR code
    uint8_t qrcodeData[qrcode_getBufferSize(3)];
    qrcode_initText(&qrcode, qrcodeData, 3, 0, "HELLO WORLD");

    // Print the QR code to the thermal printer
    printer.justify('C');
    printer.setSize('L'); // You may need to adjust the size depending on your printer model

    for (uint8_t y = 0; y < qrcode.size; y++) {
        for (uint8_t x = 0; x < qrcode.size; x++) {
            if (qrcode_getModule(&qrcode, x, y)) {
                printer.write('\xFF');  // Use '\xFF' for WHITE (255)
            } else {
                printer.write('\x00');  // Use '\x00' for BLACK (0)
            }
        }
        printer.write('\n');
    }

    // Feed the paper (you may need to adjust these commands based on your printer model)
    printer.feed(4);
    // Note: There might not be a direct 'cut' method in some libraries, refer to your printer's documentation
}

void loop() {
    // Add your looping code here
}
