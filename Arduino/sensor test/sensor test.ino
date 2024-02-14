
#define SensorPin 
#define ledPin 
unsigned long timeX, timeY;
int ledState = 0;

void setup() {
    Serial.begin(9600);
    pinMode(SensorPin, INPUT);
    pinMode(ledPin, OUTPUT);
}

void loop() {
    if (digitalRead(SensorPin) == LOW) {
        while (true) {
            if (digitalRead(SensorPin) == HIGH) { 
              timeX = milis();
              timeY = milis();
              break; 
            } 
        }
        ledState = 1;
        while ((timeY - timeX) < 2000){
            timeY = milis();
            if (digitalRead(SensorPin) == LOW) {
                while (true) { if (digitalRead(SensorPin) == HIGH) { break; } }
                ledState = 0;
                break;
            }
        }
        delay(200);
    }
    if (ledState == 0){
        digitalWrite(ledPin, LOW);
    } else if (ledState == 1){
        digitalWrite(ledPin, HIGH);
    }
}
