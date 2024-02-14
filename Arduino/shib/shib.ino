#define pirPin 3 
#define relayPin 4
 
int time = 0; 
int sw = 0; 
unsigned long time_x, time_y;  
 
void setup() { 
  pinMode(pirPin, INPUT); 
  pinMode(relayPin, OUTPUT); 
 
} 
 
void loop() { 
  if (sw == 0) { 
    if (digitalRead(pirPin) == HIGH) { 
      sw = 1; 
      time_x = millis(); 
      digitalWrite(relayPin, HIGH); 
    } 
  } else { 
    if ((millis() - time_x) > 10000) { 
      if (digitalRead(pirPin) == HIGH) { 
        time_x = millis(); 
      } else { 
        digitalWrite(relayPin, LOW); 
        sw = 0; 
      } 
    } 
  } 
}