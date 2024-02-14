
 
#include <Wire.h>3.
 
#include <Adafruit_INA219.h>
 
#include <LiquidCrystal.h>
 
Adafruit_INA219 ina219;
 
 // initialize the library with the numbers of the interface pins
 
LiquidCrystal Lcd(12, 11, 5, 4, 3, 2);
 
void setup()
 
{
 
ina219.begin(); // Initialize current sensing board (default address 0x40)
 
 // set up the LCD's number of columns and rows:
 
Lcd.begin(16,2) ;
 
 // initialize the serial communications:
 
Serial.begin(9600);
 
}
 
void loop()
 
{
 
float shuntvoltage = 0;
 
float current_mA = 0;
 
float bloodglucose =0;
 
shuntvoltage = ina219.getShuntVoltage_mV();
 
current_mA = ina219.getCurrent_mA();
 
 //set the cursor to column 0, line 0
 
Lcd.setCursor (0,0);
 
Lcd.print("Current: "); Lcd.print(current_mA); Lcd.println(" mA");
 
Lcd.setCursor (0,1);
 
Lcd.print("Blood Glucose: "); Lcd.print(Blood_mM); Lcd.println(" mMole");
 
Lcd.println("");
 
 // Delay program for a few milliseconds
 
delay(500);
 
}