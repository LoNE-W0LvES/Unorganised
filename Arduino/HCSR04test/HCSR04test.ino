#include <HCSR04.h>

// HCSR04 hc1(A4, A3); //1
// HCSR04 hc2(3, 4);   //2
// HCSR04 hc3(5, 6);   //3
// HCSR04 hc4(7, 8);   //4

// HCSR04 hc4(7, 8);   //4

HCSR04 hc[4] = {HCSR04(A4, A3), HCSR04(3, 4), HCSR04(5, 6), HCSR04(7, 8)};
void setup()
{
    Serial.begin(9600);
}

void loop()
{ 
  for (int s=0; s < 4; s++) {
    Serial.print(hc[s].dist());
    Serial.print("  ");
    delay(60);
  }
  Serial.println("");
}