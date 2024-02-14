/* Copyright 2019 David Conran
*
* This example code demonstrates how to use the "Common" IRac class to control
* various air conditions. The IRac class does not support all the features
* for every protocol. Some have more detailed support that what the "Common"
* interface offers, and some only have a limited subset of the "Common" options.
*
* This example code will:
* o Try to turn on, then off every fully supported A/C protocol we know of.
* o It will try to put the A/C unit into Cooling mode at 25C, with a medium
*   fan speed, and no fan swinging.
* Note: Some protocols support multiple models, only the first model is tried.
*
*/
#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRac.h>
#include <IRutils.h>

const uint16_t kIrLed = 4;
IRac ac(kIrLed);

void setup() {
  Serial.begin(115200);
  delay(200);

  // Set up what we want to send.
  // See state_t, opmode_t, fanspeed_t, swingv_t, & swingh_t in IRsend.h for
  // all the various options.
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
}    

void loop() {
    decode_type_t protocol = (decode_type_t)15;
    if (ac.isProtocolSupported(protocol)) {
      ac.next.protocol = protocol;
      ac.next.power = true;
      ac.sendAc();
      delay(5000);
      ac.next.degrees = 20;
      ac.sendAc();
      delay(5000);
      ac.next.power = false;
      ac.sendAc();
      delay(1000);
    }
  Serial.println("Starting from the begining again ...");
}
