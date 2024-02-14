
void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  display_initilize();
  wifi_init();
  rtc_init();
}

