#include "WiFiMulti.h"
#include "WiFiClientSecure.h"
#include "WiFiUDP.h"
#include "WakeOnLan.h"
#include "UniversalTelegramBot.h"
#include "ArduinoJson.h"
#include <DHT22.h>
//define pin data
#define pinDATA 14

DHT22 dht22(pinDATA); 
// Telegram Bot Token
String BOT_TOKEN[4] = {"6036537818:AAHkbMngnPi0BH6V_D8wd1igGTtmib_ntHU", "6532476135:AAEdVK4zMU20ZWaDOFTGTsOjh6MuU2MvaAM", "6729722038:AAGO3toug4jpHBcGOBsVefA1gV8ikENPWJY", "6437480928:AAHeP0GjWBmY1rvVTeV1vR8cq5HCG654ZAo"};
#define ALLOWED_ID "1931000593"

// WiFi configuration
#define WIFI_SSID "Aid Lab"
#define WIFI_PASS "aidlab@213cse"

// MAC address of the target device
String MAC_ADDR[3] = {"50:EB:F6:B7:92:8D", "08:BF:B8:85:8D:9D", "2C:F0:5D:2A:58:F9"};
int count = 0;
WiFiMulti wifiMulti;
WiFiClientSecure secured_client;
WiFiUDP UDP;
WakeOnLan WOL(UDP);

const unsigned long BOT_MTBS = 1000; // mean time between scan messages
UniversalTelegramBot bot(BOT_TOKEN[3], secured_client);
unsigned long bot_lasttime; // last time messages' scan has been done

void sendWOL(int i) {
  WOL.sendMagicPacket(MAC_ADDR[i]); // send WOL on default port (9)
  delay(300);
}



void handleNewMessages(int numNewMessages) {
  Serial.print("handleNewMessages ");
  Serial.println(numNewMessages);

  for (int i = 0; i < numNewMessages; i++) {
    // if (bot.messages[i].from_id != ALLOWED_ID) continue;
    
    String chat_id = bot.messages[i].chat_id;
    String text = bot.messages[i].text;

    String from_name = bot.messages[i].from_name;
    if (from_name == "") from_name = "Guest";

    if (text == "/White") {
      sendWOL(0);
      bot.sendMessage(chat_id, "Magic Packet sent to White!", "");
    } else if (text == "/BlackNew") {
      sendWOL(1);
      bot.sendMessage(chat_id, "Magic Packet sent to Black New!", "");
    } else if (text == "/BlackOld") {
      sendWOL(2);
      bot.sendMessage(chat_id, "Magic Packet sent to Black Old!", "");
    } else if (text == "/UserInfoWhite") {
      bot.sendMessage(chat_id, "Wait", "");
      bot.sendMessage("1931000593", "Requested user: " + chat_id + " Name: " + from_name + "\nIP: 103.136.236.23:3122\nUser: USER\n Password: shakil", "");
    } else if (text == "/UserInfoBlackNew") {
      bot.sendMessage(chat_id, "Wait", "");
      bot.sendMessage("1931000593", "Requested user: " + chat_id + " Name: " + from_name + "\nIP: 103.136.236.23:3232\nUser: AID\n Password: AidLab@213CSENew", "");
    } else if (text == "/UserInfoBlackOld") {
      bot.sendMessage(chat_id, "Wait", "");
      bot.sendMessage("1931000593", "Requested user: " + chat_id + " Name: " + from_name + "\nIP: 103.136.236.23:3123\nUser: CSE-AiD\n Password: AidLab@213CSEOld", "");
    } else if (text == "/ping") {
      bot.sendMessage(chat_id, "Pong.", "");
    } else if (text == "/temp") {
      String t = String(dht22.getTemperature());
      String h = String(dht22.getHumidity());
      if (dht22.getLastError() != dht22.OK) {
        Serial.print("last error :");
        Serial.println(dht22.getLastError());
      }
      String Temp = "Humidity: " + h + "\nTemparature: " + t;
      bot.sendMessage("1931000593", Temp, "");
    } else if (text == "/start") {
      String welcome = "Welcome to **AID Lab**, " + from_name + ".\n";
      welcome += "Use is restricted to the bot owner.\n\n";
      welcome += "/White :  Turn ON White PC\n";
      welcome += "/BlackNew :  Turn ON NEW Black PC\n";
      welcome += "/BlackOld :  Turn ON Old Black PC\n";
      welcome += "/UserInfoWhite : Login Info White PC\n";
      welcome += "/UserInfoBlackNew : Login Info NEW Black PC\n";
      welcome += "/UserInfoBlackOld : Login Info Old Black PC\n";
      welcome += "/ping : Check the bot status\n";
      bot.sendMessage(chat_id, welcome, "Markdown");
    }
  }
}

void setup(){

  wifiMulti.addAP(WIFI_SSID, WIFI_PASS);
  secured_client.setCACert(TELEGRAM_CERTIFICATE_ROOT);
  
  Serial.begin(115200);
  Serial.print("Connecting to WiFI...");
  while ((wifiMulti.run() != WL_CONNECTED)) {
    delay(500);
    Serial.print(".");
    count += 1;
    if(count == 20) {
      Serial.println("Reset..");
      ESP.restart();
    }
  }
  Serial.println("Connected.");
  count = 0;
  WOL.calculateBroadcastAddress(WiFi.localIP(), WiFi.subnetMask()); 

  Serial.print("Retrieving time...");
  configTime(0, 0, "pool.ntp.org");
  time_t now = time(nullptr);
  while (now < 24 * 3600) {
    Serial.print(".");
    delay(500);
    now = time(nullptr);
    count += 1;
    if(count == 20) {
      Serial.println("Reset..");
      ESP.restart();
    }
  }
  Serial.println("Connected to internet.");
}

void loop() {
  if (millis() - bot_lasttime > BOT_MTBS) {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while (numNewMessages) {
      Serial.println("Response received");
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
    bot_lasttime = millis();
  }
  delay(10);
}
