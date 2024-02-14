#include <ArduinoJson.h>
#include <WiFi.h>
#include "Adafruit_Thermal.h"
#include "HardwareSerial.h"
#include <HTTPClient.h>
#include "webserver_index_html.h"
#include <WebServer.h>
#include <Preferences.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Preferences preferences;
const int jsonSize = 1024;

WebServer server(80);
const byte rxPin = 16;
const byte txPin = 17;
HTTPClient http0;
HTTPClient http1;
HardwareSerial mySerial(1);
Adafruit_Thermal printer(&mySerial);
int http_switch = 0;
long lastTimeButtonStateChanged = 0;
int buttonState;
int mode_wifi = 0;
int start_ap = 0;
int lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long time_wifi = 0;
unsigned long time_wifi1 = 0;
String wifi_ssid = ""; // Change the type to String
String wifi_password = ""; // Change the type to String

void setup() {
  Serial.begin(115200);
  loadWifiCredentials();
  mySerial.begin(19200, SERIAL_8N1, rxPin, txPin);
  printer.begin();
  // Define routes
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html", index_html);
  });
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setFont(NULL);
  server.on("/scan-wifi", HTTP_GET, handleScanWifi);
  server.on("/wifisave", HTTP_GET, handleWifiSave);
  // Start the server
  server.begin();
  Serial.println("HTTP server started");
  pinMode(0, INPUT);
}

void loop() {
  server.handleClient();
  delete_cred();
  if (mode_wifi == 1){
    print_from_web();
  }
}

