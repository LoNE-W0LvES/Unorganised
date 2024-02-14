

#define TRIGGER_PIN 0
long lastTimeButtonStateChanged = 0;
int buttonState;
int lastButtonState = LOW;
unsigned long lastDebounceTime = 0;
long time_x = 0;
int flag = 0;
// Be sure to know how to process loops with no delay() if using non blocking
bool wm_nonblocking = true; // change to true to use non blocking

WiFiManager wm;
WiFiManagerParameter custom_field;


RTC_DS1307 rtc;
#define GMT +6

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "1.pool.ntp.org");

int i_time = 0;
int f_time = 0;



#define TYP_NEO NEO_GRB + NEO_KHZ800
#define DELAY_INTERVAL 250

int num_pixel[] = {84, 28, 36, 6};
int pins[] = {33, 32, 18, 13};
int h_b, m_b, s_b, d_b, mo_b;

Adafruit_NeoPixel NeoPixel[4] = {Adafruit_NeoPixel(num_pixel[0], pins[0], TYP_NEO), 
Adafruit_NeoPixel(num_pixel[1], pins[1], TYP_NEO), 
Adafruit_NeoPixel(num_pixel[2], pins[2], TYP_NEO), 
Adafruit_NeoPixel(num_pixel[3], pins[3], TYP_NEO)};

int weekDays[7][3]={{7, 12, 10}, {7, 8, 6}, {2, 12, 11}, {1, 2, 13}, {12, 4, 11}, {5, 9, 3}, {11, 0, 10}};

int digitSegments[11][7] = {
//   1  2  3  4  5  6  7
    {1, 1, 1, 0, 1, 1, 1},   // Digit 0
    {1, 0, 0, 0, 1, 0, 0},   // Digit 1
    {0, 1, 1, 1, 1, 1, 0},   // Digit 2
    {1, 1, 0, 1, 1, 1, 0},   // Digit 3
    {1, 0, 0, 1, 1, 0, 1},   // Digit 4
    {1, 1, 0, 1, 0, 1, 1},   // Digit 5
    {1, 1, 3, 1, 0, 1, 1},   // Digit 6
    {1, 0, 0, 0, 1, 1, 0},   // Digit 7
    {1, 1, 1, 1, 1, 1, 1},   // Digit 8
    {1, 1, 0, 1, 1, 1, 1},   // Digit 9
    {0, 0, 0, 0, 0, 0, 0} 
};

int weekSegments[14][12] = {
{1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1},    //a 0
{1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0},    //d 1
{0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1},    //e 2
{0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1},    //f 3
{1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1},    //h 4
{0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0},    //i 5
{1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0},    //m 6
{1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0},    //n 7
{1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0},    //o 8
{1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0},    //r 9
// {1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0},    //r 9
{1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1},    //s 10
{0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0},    //t 11
{1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0},    //u 12
{1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0}     //w 13
};