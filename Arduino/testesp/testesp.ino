//===================================
//ESP8266 Web Server Peripheral Data
//===================================
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

#include "html_page.h"
//---------------------------------
const char* ssid = "wolves";
const char* password = "wanda@201cse";
//======================================================================
void setup()
{
  Serial.begin(115200);
  dht.begin();  
  WiFi.begin(ssid, password);
  Serial.print("\n\r \n\rWorking to connect");
  while (WiFi.status() != WL_CONNECTED) {delay(500); Serial.print(".");}
  Serial.println("");
  Serial.println("ESP32 Web Server");
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  server.on("/", html_page);
  server.begin();
  
  Serial.println("HTTP server started");
}
//======================================================================
void loop() {server.handleClient();}