
#include "SPI.h"
#include <TFT_eSPI.h>
#include "EspUsbHostKeybord.h"

TFT_eSPI tft = TFT_eSPI();

class MyEspUsbHostKeybord : public EspUsbHostKeybord {
public:
  void onKey(usb_transfer_t *transfer) {
    uint8_t *const p = transfer->data_buffer;
    
    tft.setTextSize(1);
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    
    String Stt = String("onKey ") + String(p[0]) + " " + String(p[1]) + " " + String(p[2]) + " " + String(p[3]) + " " + String(p[4]) + " " + String(p[5]) + " " + String(p[6]) + " " + String(p[7]);
    tft.print(Stt);
  };
};

MyEspUsbHostKeybord usbHost;
void setup()
{
  Serial.begin(115200);
  tft.begin();
  tft.fillScreen(TFT_WHITE);
  usbHost.begin();
  Serial.println("\r\nInitialisation done.");
}


void loop()
{
    usbHost.task();
}
