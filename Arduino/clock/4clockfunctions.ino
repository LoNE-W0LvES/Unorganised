void rtc_init() {
    if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }
  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running, let's set the time!");
    rtc.adjust(DateTime(2022, 1, 14, 5, 5, 5));
  }
}

void rtc_update() {
  DateTime now = rtc.now();
  if (i_time == 0) {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
    } else {
      timeClient.begin();
      int OFFSET = GMT * 3600;
      timeClient.setTimeOffset(OFFSET);
      Serial.print("done");
      i_time = 1;
    }
  }

  if (f_time == 0) {
    timeClient.update();
    time_t epochTime = timeClient.getEpochTime();
    struct tm *ptm = gmtime ((time_t *)&epochTime);
    if (ptm->tm_year+1900 >= now.year()){
      Serial.println(String(ptm->tm_hour) + "-" + String(ptm->tm_min) + "-" + String(ptm->tm_sec) + "-" + String(ptm->tm_wday) + "-" + String(ptm->tm_year+1900) + "-" + String(ptm->tm_mday) + "-" + String(ptm->tm_mon+1));
      rtc.adjust(DateTime(ptm->tm_year+1900, ptm->tm_mon+1, ptm->tm_mday, ptm->tm_hour, ptm->tm_min, ptm->tm_sec));
      f_time = 1;
    Serial.println(now.dayOfTheWeek());
    }
  }
}