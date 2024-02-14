void print_from_web() {
  String url0 = "https://www.comillait.com/tokenPrint";
  http0.begin(url0);
  int httpCode0 = http0.GET();

  if (httpCode0 == HTTP_CODE_OK) {
    String response = "[" + http0.getString() + "]";
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, response.c_str());
    if (doc.size() > 0) {
      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
      }

      Serial.println("Number of elements in the array: " + String(doc.size()));
      for (JsonVariant obj : doc.as<JsonArray>()) {
        String id = obj["id"];
        String roll_no = obj["rollno"];
        String order_id = obj["order_id"];
        String food_name = obj["food_name"];
        String token_number = obj["token_number"];
        String meal_type = obj["meal_type"];
        String quantity = obj["quantity"];
        String date = obj["date"];

        
        printer.justify('C');
         printer.setSize('L');
        printer.print("Sheikh Hasina Hall");
        
        printer.feed(2);
        qr_print(token_number);
        printer.feed(2);
         printer.setSize('L');
        printer.print("Quantity:");
        printer.print(quantity);
        printer.print("\n");
        printer.print("Meal Type: ");
        printer.print(meal_type);
        printer.print("\n");
        printer.print("Date: ");
        printer.print(date);
        printer.print("\n");
        printer.setSize('M');
        printer.print("Food name: ");
        printer.print(food_name);
        printer.print("\n");
        printer.setSize('S');
        printer.print("Roll No: ");
        printer.print(roll_no);
        printer.print("\n");
        printer.print("Order ID: ");
        printer.print(order_id);
        printer.print("\n");

        printer.feed(3);
        printer.write(0x1D);
        printer.write(0x56);
        printer.write(1);
        String url1 = "https://www.comillait.com/tpqd/" + id + "&" + order_id + "&" + roll_no + "/delete";
        http1.begin(url1);
        int httpCode1 = http1.GET();

        if (httpCode1 == HTTP_CODE_OK) {
          Serial.println(http1.getString());
        } else {
          Serial.println("Failed to fetch data. HTTP Status Code: " + String(httpCode1));
        }
        http1.end();
      }
    }
  } else {
    Serial.println("Failed to fetch data. HTTP Status Code: " + String(httpCode0));
  }
  http0.end();







}