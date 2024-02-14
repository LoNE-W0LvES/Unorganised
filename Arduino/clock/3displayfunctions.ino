


void display_initilize(){
  for (int num=0; num < 4; num++) {
    NeoPixel[num].begin();
  }
}
void show_point(){
  for (int pixel=0; pixel < 6; pixel++) {
    NeoPixel[3].setPixelColor(pixel, NeoPixel[3].Color(255, 0, 0));
    NeoPixel[3].show();
  }
}

void print_display(int number, int seg, int led, int dt){
  for (int pixel=0; pixel < 7; pixel++) {
    int n = ((led/7)*pixel) + (seg*led);
    for (int i=0; i < (led/7); i++) {
      if (digitSegments[number][pixel] == 0) {
        NeoPixel[dt].setPixelColor(n + i, NeoPixel[dt].Color(0, 0, 0));
      } else {
        NeoPixel[dt].setPixelColor(n + i, NeoPixel[dt].Color(255, 0, 0));
      }
    }
    NeoPixel[dt].show();
  }
}

void show_weeks(int number){
  for (int seg=0; seg < 3; seg++) {
    for (int pixel=0; pixel < 12; pixel++) {
      if (weekSegments[weekDays[number][seg]][pixel] == 0) {
        NeoPixel[2].setPixelColor(pixel + (seg*12), NeoPixel[2].Color(0, 0, 0));
      } else {
        NeoPixel[2].setPixelColor(pixel + (seg*12), NeoPixel[2].Color(255, 0, 0));
      }
    }
  }
  NeoPixel[2].show();
}

void test_weeks(){
  for (int seg=0; seg < 3; seg++) {
    for (int pixel=0; pixel < 12; pixel++) {
      NeoPixel[2].setPixelColor(pixel + (seg*12), NeoPixel[2].Color(255, 0, 0));
      delay(250);
      NeoPixel[2].show();
    }
  }
  
  for (int seg=0; seg < 3; seg++) {
    for (int pixel=0; pixel < 12; pixel++) {
      NeoPixel[2].setPixelColor(pixel + (seg*12), NeoPixel[2].Color(0, 0, 0));
      delay(250);
      NeoPixel[2].show();
    }
  }
}

void show_time(int h, int m, int s) {
  if (h_b != h) {
    int h1 = h/10;
    int h2 = h-(h1*10);
    print_display(h1, 5, 14, 0);
    print_display(h2, 4, 14, 0);
    h_b = h;
  }
  if (m_b != m) {
    int m1 = m/10;
    int m2 = m-(m1*10);
    print_display(m1, 3, 14, 0);
    print_display(m2, 2, 14, 0);
    m_b = m;
  }
  if (s_b != s) {
    int s1 = s/10;
    int s2 = s-(s1*10);
    print_display(s1, 1, 14, 0);
    print_display(s2, 0, 14, 0);
    s_b = s;
  }
}

void show_date(int d, int mo) {
  if (d_b != d) {
    int d1 = d/10;
    int d2 = d-(d1*10);
    print_display(d1, 3, 7, 1);
    print_display(d2, 2, 7, 1);
    d_b = d;
  }
  if (mo_b != mo) {
    int mo1 = mo/10;
    int mo2 = mo-(mo1*10);
    print_display(mo1, 1, 7, 1);
    print_display(mo2, 0, 7, 1);
    mo_b = mo;
  }
}
