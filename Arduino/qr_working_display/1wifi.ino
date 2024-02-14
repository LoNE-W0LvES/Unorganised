void saveWifiCredentials(String ssid, String password) {
  preferences.begin("wifi", false);  // Open the preferences with a read-write mode
  preferences.putString("ssid", ssid);
  Serial.println(ssid);
  preferences.putString("password", password);
  Serial.println(password);
  preferences.end();  // Close the preferences
  ESP.restart();
}

void loadWifiCredentials() {
  preferences.begin("wifi", true);
  wifi_ssid = preferences.getString("ssid", "");
  wifi_password = preferences.getString("password", "");
  preferences.end();
  if (wifi_ssid == "") {
    startAccessPoint();
  } else {
    WiFi.mode(WIFI_STA);
    WiFi.begin(wifi_ssid, wifi_password);
    mode_wifi = 1;
    time_wifi = millis();
    time_wifi1 = millis();
    start_ap = 0;
    // Wait for connection
    while (true) {
      if ((millis() - time_wifi) >1000) {
        if (WiFi.status() != WL_CONNECTED) {
          Serial.println("Connecting...");
          time_wifi = millis();
          if ((millis() - time_wifi1) >3000) {
            WiFi.disconnect();
            Serial.println("Connection Failed! Retrying...");
            WiFi.begin(wifi_ssid, wifi_password);
            time_wifi1 = millis();
          }
        } else {
          break;
        }
      }
      if (millis() - lastTimeButtonStateChanged > 50) {
        byte buttonState = digitalRead(0);
        if (buttonState != lastButtonState) {
          lastTimeButtonStateChanged = millis();
          lastButtonState = buttonState;
          if (buttonState == LOW) {
            start_ap = 1;
            break;
          }
        }
      }
    }
    if (start_ap == 1){
      startAccessPoint();
    } else {
      Serial.println(WiFi.localIP());
    }
  }
}

void startAccessPoint() {
  Serial.println("Starting Access Point...");
  mode_wifi = 0;
  WiFi.mode(WIFI_AP);
  WiFi.softAP("Hall system", "LoNEWoLvES");

  Serial.println("Access Point Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());
}

void handleWifiSave() {
  String ssid = server.arg("s");
  String password = server.arg("p");

  if (ssid.length() > 0) {
    // Save the new Wi-Fi credentials
    saveWifiCredentials(ssid.c_str(), password.c_str());
    loadWifiCredentials();
    // Respond with a success message
    server.send(200, "text/plain", "Wi-Fi credentials saved successfully");
  } else {
    // Respond with an error message if parameters are missing
    server.send(400, "text/plain", "Missing parameters");
  }
}

void delete_cred() {
  if (millis() - lastTimeButtonStateChanged > 50) {
    byte buttonState = digitalRead(0);
    if (buttonState != lastButtonState) {
      lastTimeButtonStateChanged = millis();
      lastButtonState = buttonState;
      if (buttonState == LOW) {
        preferences.begin("wifi", false);
        preferences.putString("ssid", "");
        preferences.putString("password", "");
        preferences.end();
        ESP.restart();
      }
    }
  }
}


void handleScanWifi() {
  DynamicJsonDocument jsonDoc(jsonSize);
  JsonArray networkArray = jsonDoc.to<JsonArray>();
  int numNetworks = WiFi.scanNetworks();
  Serial.print("network number: ");
  Serial.println(numNetworks);
  for (int i = 0; i < numNetworks; i++) {
    JsonObject network = networkArray.createNestedObject();
    network["SSID"] = WiFi.SSID(i);
    network["RSSI"] = WiFi.RSSI(i);
    network["SignalStrength"] = WiFi.RSSI(i) + 100;
    network["Password"] = WiFi.encryptionType(i) != 0;
  }

  String jsonString;
  serializeJson(jsonDoc, jsonString);
  server.send(200, "application/json", jsonString);
}
