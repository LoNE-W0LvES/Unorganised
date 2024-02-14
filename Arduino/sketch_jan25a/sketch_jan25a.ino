#include "WiFi.h"
#include "ESPAsyncWebServer.h"

char ssid[] = "Network-1";          //  your network SSID (name) 

IPAddress IP = {10, 10, 1, 1}; // curly braces
IPAddress gateway = IPAddress (10, 10, 2, 8); // not curly braces
IPAddress NMask = IPAddress (255, 255, 255, 0); // not curly braces

AsyncWebServer server(80);
 
void setup ()
{
  Serial.begin(115200);
  Serial.println();
  Serial.print("System Start");

  WiFi.mode(WIFI_AP);  
  WiFi.softAP(ssid);
  delay(1000);

  WiFi.softAPConfig(IP, IP, NMask);

  delay(1000);
  
  IPAddress myIP = WiFi.softAPIP();
  Serial.println();
  Serial.print("AP IP address: ");
  Serial.println(myIP);  

  server.on("/hello", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "Hello World");
  });
 
  server.begin();
}

void loop ()
{ }