#include <WiFi.h>
#include <Preferences.h>
#include "ESPAsyncWebServer.h"

const char* ssid = "wolves";
const char* password ="csewolveslab@201";
IPAddress noIP = {0, 0, 0, 0};
IPAddress storedIp;
IPAddress localIP;
IPAddress gatewayIP;
IPAddress subnetMask;
IPAddress dnsIP0;
IPAddress dnsIP1;
AsyncWebServer server(80);
// uint32_t ip_addr;
// uint32_t ip_addr1;
Preferences preferences;
void setup(){
  Serial.begin(115200);
  preferences.begin("ip", false);
  // storedIp = preferences.getUInt("localIP", (uint32_t) noIP);
  // localIP = {storedIp[0], storedIp[1], storedIp[2], 20};
  // storedIp = preferences.getUInt("gatewayIP", (uint32_t) noIP);
  // gatewayIP = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  // storedIp = preferences.getUInt("subnetMask", (uint32_t) noIP);
  // subnetMask = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  // storedIp = preferences.getUInt("dnsIP0", (uint32_t) noIP);
  // dnsIP0 = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  // storedIp = preferences.getUInt("dnsIP1", (uint32_t) noIP);
  // dnsIP1 = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  
  Serial.print("Saved ip: ");
 


//   WiFi.mode(WIFI_AP);
//   WiFi.softAP("EspDevice", "password1234");
//   delay(1000);
//   WiFi.softAPConfig(IP, IP, NMask);
//   server.on("/h", HTTP_GET, [](AsyncWebServerRequest *request){
//     request->send(200, "text/plain", "light On");
//   });
//   server.begin();

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("Connecting...\n\n");
  }
  // uint32_t ip_addr = (uint32_t) WiFi.localIP();
  // preferences.putUInt("localIP", (uint32_t) WiFi.localIP());
  // preferences.putUInt("gatewayIP", (uint32_t) WiFi.gatewayIP());
  // preferences.putUInt("subnetMask", (uint32_t) WiFi.subnetMask());
  // preferences.putUInt("dnsIP0", (uint32_t) WiFi.dnsIP(0));
  // preferences.putUInt("dnsIP1", (uint32_t) WiFi.dnsIP(1));
  delay(5000);
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
  Serial.print("Subnet Mask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway IP: ");
  Serial.println(WiFi.gatewayIP());
  Serial.print("DNS 1: ");
  Serial.println(WiFi.dnsIP(0));
  Serial.print("DNS 2: ");
  Serial.println(WiFi.dnsIP(1));
  storedIp = WiFi.localIP();
  localIP = {storedIp[0], storedIp[1], storedIp[2], 30};
  storedIp = WiFi.gatewayIP();
  gatewayIP = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  storedIp = WiFi.subnetMask();
  subnetMask = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  storedIp = WiFi.dnsIP(0);
  dnsIP0 = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  storedIp = WiFi.dnsIP(1);
  dnsIP1 = {storedIp[0], storedIp[1], storedIp[2], storedIp[3]};
  WiFi.disconnect();
  if ((localIP != noIP) && (gatewayIP != noIP) && (subnetMask != noIP) && (dnsIP0 != noIP)) {
    Serial.println("setting ip");
    if (WiFi.config(localIP, gatewayIP, subnetMask, dnsIP0, dnsIP1) == false) {
      Serial.println("Configuration failed.");
    }
  }
  WiFi.reconnect();
  preferences.end();
}

void loop(){}