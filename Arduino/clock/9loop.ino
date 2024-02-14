

void loop() {
  DateTime now = rtc.now();
  wifi_run();
  rtc_update();
  show_time(now.hour(), now.minute(), now.second());
  show_date(now.day(), now.month());
  // delay(1000);
  show_weeks(now.dayOfTheWeek());
  // test_weeks();
  show_point();
}
