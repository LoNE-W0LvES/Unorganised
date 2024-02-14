#include "WiFiMulti.h"
#include "WiFiClientSecure.h"
#include "WiFiUDP.h"
#include "WakeOnLan.h"
#include "UniversalTelegramBot.h"
#include "ArduinoJson.h"
#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRac.h>
#include <IRutils.h>

const uint16_t kIrLed = 12;
IRac ac(kIrLed);

// Telegram Bot Token
String BOT_TOKEN[3] = {"6552948679:AAHVZ4t5827N_6Lu--5w-L8bz7DsKWgipJs", "6879307467:AAGx85K9EKjtZAjxEn_hKthDCOd8d89XqGw", "6807882535:AAGjnoPjgKbqOxC-7K9LBOaXNGcU9EKUpvw"};
#define ALLOWED_ID "1931000593"

// WiFi configuration
#define WIFI_SSID "wolves"
#define WIFI_PASS "wanda@201cse"

// MAC address of the target device
String MAC_ADDR = "24:1C:04:77:29:CC";
int count = 0;
WiFiMulti wifiMulti;
WiFiClientSecure secured_client;
WiFiUDP UDP;
WakeOnLan WOL(UDP);

const unsigned long BOT_MTBS = 1000; // mean time between scan messages
UniversalTelegramBot bot(BOT_TOKEN[2], secured_client);
unsigned long bot_lasttime; // last time messages' scan has been done

void sendWOL() {
  WOL.sendMagicPacket(MAC_ADDR); // send WOL on default port (9)
  delay(300);
}

void handleNewMessages(int numNewMessages) {
  Serial.print("handleNewMessages ");
  Serial.println(numNewMessages);

  for (int i = 0; i < numNewMessages; i++) {
    Serial.println(bot.messages[i].from_id);
    if (bot.messages[i].from_id != ALLOWED_ID) continue;
    
    String chat_id = bot.messages[i].chat_id;
    String text = bot.messages[i].text;

    String from_name = bot.messages[i].from_name;
    if (from_name == "") from_name = "Guest";

    if (text == "/WoLvES") {
      sendWOL();
      bot.sendMessage(chat_id, "Magic Packet sent to WoLvES!", "");
    } else if (text == "/AcON") {
      ac.next.power = true;
      ac.sendAc();
      bot.sendMessage(chat_id, "Turning AC on!", "");
    } else if (text == "/AcOFF") {
      ac.next.power = false;
      ac.sendAc();
      bot.sendMessage(chat_id, "Turning AC Off!", "");
    } else if (text.indexOf("/temp") != -1) {
      text.replace("/temp", "");
      int n = text.toInt();
      if (16 <= n <= 30){
        ac.next.degrees = n;
        ac.sendAc();
      }
      bot.sendMessage(chat_id, "Temp Set!", "");
    } else if (text == "/UserInfoWoLvES") {
      bot.sendMessage(chat_id, "IP: 103.136.236.19 User: 'nafimnr00@gmail.com' Password:'Wolvescse@201Lab'", "");
    } else if (text == "/ping") {
      bot.sendMessage(chat_id, "Pong.", "");
      
    } else if (text == "/start") {
      String welcome = "Welcome to **AID Lab**, " + from_name + ".\n";
      welcome += "/WoLvES :  Turn ON WoLvES PC\n";
      welcome += "/AcON :  Turn ON AC\n";
      welcome += "/AcOFF :  Turn OFF AC\n";
      welcome += "/temp{value} :  Set AC Temparature\n";
      welcome += "/UserInfoWoLvES : Login Info WoLvES PC\n";
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
    delay(150);
    now = time(nullptr);
    count += 1;
    if(count == 20) {
      Serial.println("Reset..");
      ESP.restart();
    }
  }
  Serial.println("Connected to internet.");
  ac.next.protocol = decode_type_t::DAIKIN;  // Set a protocol to use.
  ac.next.model = 1;  // Some A/Cs have different models. Try just the first.
  ac.next.mode = stdAc::opmode_t::kCool;  // Run in cool mode initially.
  ac.next.celsius = true;  // Use Celsius for temp units. False = Fahrenheit
  ac.next.degrees = 25;  // 25 degrees.
  ac.next.fanspeed = stdAc::fanspeed_t::kMedium;  // Start the fan at medium.
  ac.next.swingv = stdAc::swingv_t::kOff;  // Don't swing the fan up or down.
  ac.next.swingh = stdAc::swingh_t::kOff;  // Don't swing the fan left or right.
  ac.next.light = false;  // Turn off any LED/Lights/Display that we can.
  ac.next.beep = false;  // Turn off any beep from the A/C if we can.
  ac.next.econo = false;  // Turn off any economy modes if we can.
  ac.next.filter = false;  // Turn off any Ion/Mold/Health filters if we can.
  ac.next.turbo = false;  // Don't use any turbo/powerful/etc modes.
  ac.next.quiet = false;  // Don't use any quiet/silent/etc modes.
  ac.next.sleep = -1;  // Don't set any sleep time or modes.
  ac.next.clean = false;  // Turn off any Cleaning options if we can.
  ac.next.clock = -1;  // Don't set any current time if we can avoid it.
  ac.next.power = false;  // Initially start with the unit off.
  decode_type_t protocol = (decode_type_t)15;
  ac.next.protocol = protocol;
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
