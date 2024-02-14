#include <WiFi.h>
#include "ESPAsyncWebServer.h"
#include <HTTPClient.h>
const char* WIFI_SSID = "wolves";
const char* WIFI_PASSWORD = "csewolveslab@201";
int wifiRetry = 0;
AsyncWebServer server(80);
const char* espCamReset = "http://192.168.3.30/doorUnlock";
String returnxX;
String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "--"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (true) {
    while ((WiFi.status() != WL_CONNECTED) && (wifiRetry < 15)) {
      Serial.print(".");
      delay(300);
      wifiRetry++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        break;
    } else {
      wifiRetry = 0;
      WiFi.disconnect();
      WiFi.reconnect();
    }
  }
  // put your setup code here, to run once:
  server.on("/pp", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "door Unlock");
  });
  server.begin();
}

void loop() {
  returnxX = httpGETRequest(espCamReset);
  Serial.println(returnxX);
  delay(2000);

}
