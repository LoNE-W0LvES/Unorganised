
void wifi_init() {
  WiFi.mode(WIFI_STA);

  Serial.setDebugOutput(true);  
  delay(3000);
  Serial.println("\n Starting");

  pinMode(TRIGGER_PIN, INPUT);

  if(wm_nonblocking) wm.setConfigPortalBlocking(false);
  int customFieldLength = 40;
  const char* custom_radio_str = "<br/><label for='customfieldid'>Custom Field Label</label><input type='radio' name='customfieldid' value='1' checked> One<br><input type='radio' name='customfieldid' value='2'> Two<br><input type='radio' name='customfieldid' value='3'> Three";
  new (&custom_field) WiFiManagerParameter(custom_radio_str); // custom html input
  
  wm.addParameter(&custom_field);
  wm.setSaveParamsCallback(saveParamCallback);

  std::vector<const char *> menu = {"wifi","info","param","sep","restart","exit"};
  wm.setMenu(menu);

  wm.setClass("invert");

  wm.setConfigPortalTimeout(30);

  bool res;
  res = wm.autoConnect("AutoConnectAP","password");

  if(!res) {
    Serial.println("Failed to connect or hit timeout");
  } 
  else {
    Serial.println("connected...yeey :)");
  }
}

void checkButton(){
  if (millis() - lastTimeButtonStateChanged > 50) {
    byte buttonState = digitalRead(TRIGGER_PIN);
    if (buttonState != lastButtonState) {
      lastTimeButtonStateChanged = millis();
      lastButtonState = buttonState;
      if (buttonState == LOW) {
        if (millis() - time_x > 3000) {
          wm.resetSettings();
          ESP.restart();
        } else {
          wm.setConfigPortalTimeout(120);
          if (!wm.startConfigPortal("OnDemandAP","password")) {
            Serial.println("failed to connect or hit timeout");
            delay(3000);
          } else {
            Serial.println("connected...yeey :)");
          }
        }
      } else {
        time_x = millis();
        Serial.println("Button pressed");
      }
    }
  }
}

String getParam(String name){
  String value;
  if(wm.server->hasArg(name)) {
    value = wm.server->arg(name);
  }
  return value;
}

void saveParamCallback(){
  Serial.println("[CALLBACK] saveParamCallback fired");
  Serial.println("PARAM customfieldid = " + getParam("customfieldid"));
}

void wifi_run() {
  checkButton();
  if(wm_nonblocking) wm.process();
  checkButton();
}
