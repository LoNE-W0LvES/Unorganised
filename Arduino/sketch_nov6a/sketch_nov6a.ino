  String page_title, pot_val, sw_val, sensor, temp, hum;
  //---------------------------------------------------------------------------
  page_title = "<h1 style=color:blue;>"
               "<body bgcolor=\"#FFFF00\">"
               "<p style=font-family:verdana>"
               "ESP8266 Peripheral Data<br>____________________</p>"       
               "<meta http-equiv=\"refresh\" content=\"1\">";
  //---------------------------------------------------------------------------
  float pot = convert_2_volt(analogRead(0));
  pot_val = String("Pot Voltage : ") + String(pot) + String(" V");
  pot_val = "<p style=font-family:arial>" + pot_val;
  //---------------------------------------------------------------------------
  if(digitalRead(D1)==LOW) sw_val = String("Switch Status : ") + String("OFF");
  if(digitalRead(D1)==HIGH) sw_val = String("Switch Status : ") + String("ON");
  sw_val = "<p style=font-family:arial>" + sw_val;
  //---------------------------------------------------------------------------
  if(digitalRead(D2)==HIGH) sensor = String("IR Obstacle : ") + String("NO");
  if(digitalRead(D2)==LOW) sensor = String("IR Obstacle : ") + String("YES");
  sensor = "<p style=font-family:arial>" + sensor;
  //---------------------------------------------------------------------------
  temp = String("Temperature : ") + String(dht11_temp()) + String(" C");
  temp = "<p style=font-family:arial>" + temp;
  hum = String("Humidity : ") + String(dht11_hum()) + String(" %");
  hum = "<p style=font-family:arial>" + hum;
  //---------------------------------------------------------------------------