#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

#define bttom1       2
#define bttom2       3
#define bttom3       4
#define bttom4       5
#define heter        6

long int seconds = 0;
int minutes = 0;
int hours = 0;

int t_s = 0, t_set = 0, Start = 0, asd = 0;

void setup() {
  pinMode(bttom1, INPUT);
  pinMode(bttom2, INPUT);
  pinMode(bttom3, INPUT);
  pinMode(bttom4, INPUT);
  pinMode(heter, OUTPUT);
  digitalWrite(heter, HIGH);
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Please Wait");
  delay(1000);
  lcd.clear();
  lcd.setCursor(6, 0);
  lcd.print("UV-C");
  lcd.setCursor(3, 1);
  lcd.print("STERILIZER");
}

void loop() {
  if (Start == 1) {
    if (t_set > 0) {
      lcd.setCursor(0, 0);
      lcd.print("Start Timer.....");
      lcd.setCursor(0, 1);
      {
        if (hours < 10)
        {
          lcd.print("0");
          lcd.print(hours);
        }
        else
        {
          lcd.print(hours);
        }
      }
      lcd.print(":");
      {
        if (minutes < 10)
        {
          lcd.print("0");
          lcd.print(minutes);
          lcd.print(":");
        }
        else
        {
          lcd.print(minutes);
          lcd.print(":");
        }
      }
      {
        if (seconds < 10)
        {
          lcd.print("0");
          lcd.print(seconds);
        }
        else
        {
          lcd.print(seconds);
        }
      }
      t_s = ((((hours * 60) + minutes) * 60) + seconds);
      if (t_s >= t_set) {
        Start = 0;
        t_set = 0;
        t_s = 0;
        seconds = 0;
        minutes = 0;
        hours = 0;
        digitalWrite(heter, HIGH);
        lcd.clear();
        lcd.print("DONE.....");
        delay(2000);
        lcd.clear();
      }
      else {
        digitalWrite(heter, LOW);
      }
    }
    else {
      lcd.setCursor(0, 0);
      lcd.print("Start.....");
      digitalWrite(heter, LOW);
    }
  }
  else {
    lcd.setCursor(6, 0);
    lcd.print("UV-C");
    lcd.setCursor(3, 1);
    lcd.print("STERILIZER");
  }
  checkKeys();
}

void checkKeys()
{
  if (digitalRead(bttom1) == 1)
  {
    lcd.clear();
    lcd.print("Please Wait");
    delay(1000);
    TIME_SET();
  }
  else if (digitalRead(bttom3) == 1 && Start == 1)
  {
    lcd.clear();
    lcd.print("Please Wait");
    delay(1000);
    lcd.clear();
    lcd.print("Stoping.....");
    delay(1000);
    Start = 0;
    t_set = 0;
    t_s = 0;
    seconds = 0;
    minutes = 0;
    hours = 0;
    digitalWrite(heter, HIGH);
    lcd.clear();
    return;
  }
  else if (digitalRead(bttom4) == 1)
  {
    lcd.clear();
    lcd.print("Please Wait");
    delay(1000);
    lcd.clear();
    lcd.print("Starting.....");
    delay(1000);
    lcd.clear();
    Start = 1;
    return;
  }
}

void TIME_SET()
{
  int count = 1;
  lcd.clear();
  lcd.print("Time Set");
  lcd.setCursor(0, 1);
  lcd.print("Sec. :");
  while (1)
  {
    lcd.setCursor(9, 1);
    lcd.print(count);
    lcd.print("   ");
    if (digitalRead(bttom1) == 1)
    {
      count++;
      if (count > 600)
        count = 1;
      delay(500);
    }
    else if (digitalRead(bttom2) == 1)
    {
      count--;
      if (count < 1)
        count = 600;
      delay(500);
    }
    else if (digitalRead(bttom4) == 1)
    {
      t_set = count;
      lcd.clear();
      return;
    }
    else if (digitalRead(bttom3) == 1)
    {
      lcd.clear();
      return;
    }
  }
}