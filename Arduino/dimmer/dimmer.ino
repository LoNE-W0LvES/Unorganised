//Libraries
#include <RBDdimmer.h>//https://github.com/RobotDynOfficial/RBDDimmer

//Parameters
const int zeroCrossPin  = 1;
const int acdPin  = 2;
int MIN_POWER  = 0;
int MAX_POWER  = 80;
int POWER_STEP  = 2;

//Variables
int power  = 0;

//Objects
dimmerLamp acd(acdPin,zeroCrossPin);

void setup(){
//Init Serial USB
Serial.begin(115200);
Serial.println(F("ESP32 System"));
acd.begin(NORMAL_MODE, ON);
}

void loop(){
  acd.setPower(100);
  delay(100);
}
