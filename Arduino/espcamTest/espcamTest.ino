char radar0;
String Radar_String0, Radar_String1;
const unsigned int MAX_MESSAGE_LENGTH = 50;
static char message[MAX_MESSAGE_LENGTH];
static unsigned int message_pos = 0;
HardwareSerial GG(1);
void setup() {
  Serial.begin(115200);
  GG.begin(115200);
}

//void loop() {
//  while (GG.available()>0) {
//    radar0 = GG.read();
//    Serial.print("r0: ");
//    Serial.println(radar0);
//  }
//  while (radar0 == 'w') {
//    while (GG.available()) {
//      char radar1 = GG.read();
//      Radar_String0 += radar1;
//    }
//    Serial.print("Radar String0: ");
//    Serial.println(Radar_String0);
//    radar0 = (char)0;
//  }
//  while (radar0 == 'p') {
//    while (GG.available()) {
//      char radar2 = GG.read();
//      Radar_String1 += radar2;
//    }
//    Serial.print("Radar String1: ");
//    Serial.println(Radar_String1);
//    radar0 = (char)0;
//  }
//}



void loop() {

 while (GG.available() > 0) {
   char inByte = GG.read();
   if ( inByte == '\n') {
    break;
   }
   if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) ) {
     message[message_pos] = inByte;
     message_pos++;
   } else {
     message[message_pos] = '\0';
     Serial.println(message);
     message_pos = 0;
   }
 }
  Serial.print("message: ");
  Serial.print(message);
  Serial.println("message end");
  while (message_pos < MAX_MESSAGE_LENGTH - 1) {
     message[message_pos] = (char)0;
     message_pos++;
     if (message_pos == MAX_MESSAGE_LENGTH){
         message_pos = 0;
     }
   }
}
