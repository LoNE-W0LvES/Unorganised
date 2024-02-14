String urlencode(String str)
{
    String encodedString="";
    char c;
    char code0;
    char code1;
    char code2;
    for (int i =0; i < str.length(); i++){
      c=str.charAt(i);
      if (i == str.length() - 1) {
        if (c == '\r') {
          return encodedString;
        }
      }
      if (c == ' '){
        encodedString+= '+';
      } else if (isalnum(c)){
        encodedString+=c;
      } else{
        code1=(c & 0xf)+'0';
        if ((c & 0xf) >9){
            code1=(c & 0xf) - 10 + 'A';
        }
        c=(c>>4)&0xf;
        code0=c+'0';
        if (c > 9){
            code0=c - 10 + 'A';
        }
        code2='\0';
        encodedString+='%';
        encodedString+=code0;
        encodedString+=code1;
        //encodedString+=code2;
      }
      yield();
    }
    return encodedString;
}

String transformHash(const String &hash) {
    String transformedHash = "";
    for (size_t i = 0; i < hash.length(); i++) {
        char c = hash.charAt(i);
        if (c >= 'A' && c <= 'Z') {
            c = c + 32;
        } else if (c >= 'a' && c <= 'z') {
            c = c - 32;
        }
        transformedHash += c;
    }
    return transformedHash;
}

void web_check_qr_code(String QrCode) {
  if (secret_code.length() <= 0) {
    secret_code = "value";
  }
  String url0 = "https://www.justehall.com/orders/scan/" + secret_code + "/" + urlencode(QrCode);
  Serial.println(url0);
  http0.begin(url0);
  int httpCode0 = http0.GET();

  if (httpCode0 == HTTP_CODE_OK) {
    String http_str = http0.getString();
    Serial.println(http_str);
    mtime = millis() - 11000;
    if (http_str == "0") {
      flag = 1;
      show_color(red);
    } else {
      flag = 2;
      show_color(blue);
    }
  } else {
    Serial.println("Failed to fetch data. HTTP Status Code: " + String(httpCode0));
    mtime = millis() - 11000;
    flag = 3;
    show_color(purple);
  }
  http0.end();
}

void show_color(String hexColor) {
  unsigned long rgbColor = strtoul(hexColor.c_str() + 1, NULL, 16);
  int red = (rgbColor >> 16) & 0xFF;
  int green = (rgbColor >> 8) & 0xFF;
  int blue = rgbColor & 0xFF;
  pixels.setPixelColor(0, pixels.Color(red, green, blue));
  pixels.show(); 
}


void qr_power() { 
  digitalWrite(12, LOW);
  delay(50);
  digitalWrite(12, HIGH);
}
