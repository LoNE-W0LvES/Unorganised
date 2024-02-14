#include <WiFi.h>
#include <FirebaseESP32.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "Base64.h"

#include "esp_camera.h"

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#define WIFI_SSID "Lab"
#define WIFI_PASSWORD "cselab@221"
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"


//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

//CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

String doorBellDevice, doorStateApp,  fanSpeed, fanStateApp, lightStateApp, takePhoto;
String oldDoorStateApp = "2";
String oldFanStateApp = "2";
String oldLightStateApp = "2";
String oldFanSpeed = "200";
String dataUpdate = "1";
String firstDataUpdate = "1";
String input_string;
unsigned long timeX, timeY;
int timeSwitch = 0;


String Photo2Base64() {
    camera_fb_t * fb = NULL;
    fb = esp_camera_fb_get();  
    if(!fb) {
      Serial.println("Camera capture failed");
      return "";
    }
  
    String imageFile = "";
    char *input = (char *)fb->buf;
    char output[base64_enc_len(3)];
    for (int i=0;i<fb->len;i++) {
      base64_encode(output, (input++), 3);
      if (i%3==0) imageFile += urlencode(String(output));
    }

    esp_camera_fb_return(fb);
    String decoded=urldecode(imageFile);
    return decoded;
}

void setup()
{
WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  Serial.begin(115200);
delay(2000);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  camera_config_t configcam;
  configcam.ledc_channel = LEDC_CHANNEL_0;
  configcam.ledc_timer = LEDC_TIMER_0;
  configcam.pin_d0 = Y2_GPIO_NUM;
  configcam.pin_d1 = Y3_GPIO_NUM;
  configcam.pin_d2 = Y4_GPIO_NUM;
  configcam.pin_d3 = Y5_GPIO_NUM;
  configcam.pin_d4 = Y6_GPIO_NUM;
  configcam.pin_d5 = Y7_GPIO_NUM;
  configcam.pin_d6 = Y8_GPIO_NUM;
  configcam.pin_d7 = Y9_GPIO_NUM;
  configcam.pin_xclk = XCLK_GPIO_NUM;
  configcam.pin_pclk = PCLK_GPIO_NUM;
  configcam.pin_vsync = VSYNC_GPIO_NUM;
  configcam.pin_href = HREF_GPIO_NUM;
  configcam.pin_sscb_sda = SIOD_GPIO_NUM;
  configcam.pin_sscb_scl = SIOC_GPIO_NUM;
  configcam.pin_pwdn = PWDN_GPIO_NUM;
  configcam.pin_reset = RESET_GPIO_NUM;
  configcam.xclk_freq_hz = 20000000;
  configcam.pixel_format = PIXFORMAT_JPEG;
    //init with high specs to pre-allocate larger buffers
  if(psramFound()){
    configcam.frame_size = FRAMESIZE_UXGA;
    configcam.jpeg_quality = 10;  //0-63 lower number means higher quality
    configcam.fb_count = 2;
  } else {
    configcam.frame_size = FRAMESIZE_SVGA;
    configcam.jpeg_quality = 12;  //0-63 lower number means higher quality
    configcam.fb_count = 1;
  }
    // camera init
  esp_err_t err = esp_camera_init(&configcam);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    delay(1000);
    ESP.restart();
  }
  sensor_t * s = esp_camera_sensor_get();
  s->set_framesize(s, FRAMESIZE_QQVGA);  // VGA|CIF|QVGA|HQVGA|QQVGA   ( UXGA? SXGA? XGA? SVGA? )
  
  /* Assign the api key (required) */
  config.api_key = API_KEY;

  config.database_url = DATABASE_URL;
  Firebase.begin(DATABASE_URL, API_KEY);

  //Comment or pass false value when WiFi reconnection will control by your code or third party library
 // Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);

}

void loop()
{
  if(Serial.available()>0){
    input_string = Serial.readString();
    input_string.trim();
  }
  if (Firebase.ready()) 
  {
    if (input_string == "doorBell") {
      Firebase.setString(fbdo, "/states/doorBellDevice", "1");
      timeSwitch = 1;
      timeX = millis();
    }
    timeY = millis();
    if (timeSwitch = 1) {
      if((timeY - timeX)> 30000){
        Firebase.setString(fbdo, "/states/doorBellDevice", "0");
        Serial.println();
      }
    }
    Firebase.getString(fbdo, "/states/dataUpdate");
    dataUpdate = fbdo.to<String>();
    if ((dataUpdate == "1") || (firstDataUpdate == "1")) {
      firstDataUpdate = "0";
      dataUpdate = "0";
      Firebase.setString(fbdo, "/states/dataUpdate", "0");
      Firebase.getString(fbdo, "/states/doorStateApp");
      doorStateApp = fbdo.to<String>();
      Firebase.getString(fbdo, "/states/lightStateApp");
      lightStateApp = fbdo.to<String>();
      Firebase.getString(fbdo, "/states/fanStateApp");
      fanStateApp = fbdo.to<String>();
      Firebase.getString(fbdo, "/states/fanSpeed");
      fanSpeed = fbdo.to<String>();
      Firebase.getString(fbdo, "/states/takePhoto");
      takePhoto = fbdo.to<String>();
    }
    if (oldDoorStateApp != doorStateApp) {
      oldDoorStateApp = doorStateApp;
      if (doorStateApp == "0"){
        Serial.print("doorStateApp: 0");
        Serial.println();
        Firebase.setString(fbdo, "/states/doorStateDevice", "0");
      }
      if (doorStateApp == "1"){
        Serial.print("doorStateApp: 1");
        Serial.println();
        Firebase.setString(fbdo, "/states/doorStateDevice", "1");
      }
    }

    if (oldLightStateApp != lightStateApp) {
      oldLightStateApp = lightStateApp;
      if (lightStateApp == "0"){
        Serial.print("lightStateApp: 0");
        Serial.println();
        Firebase.setString(fbdo, "/states/lightStateDevice", "0");
      }
      if (lightStateApp == "1"){
        Serial.print("lightStateApp: 1");
        Serial.println();
        Firebase.setString(fbdo, "/states/lightStateDevice", "1");
      }
    }
    
    if (oldFanStateApp != fanStateApp) {
      oldFanStateApp = fanStateApp;
      if (fanStateApp == "0"){
        Serial.print("fanStateApp: 0");
        Serial.println();
        Firebase.setString(fbdo, "/states/fanStateDevice", "0");
      }
      if (fanStateApp == "1"){
        Serial.print("fanStateApp: 1");
        Serial.println();
        Firebase.setString(fbdo, "/states/fanStateDevice", "1");
      }
    }
    if (oldFanSpeed != fanSpeed) {
      oldFanSpeed = fanSpeed;
      Serial.print("fanSpeed: " + fanSpeed);
      Serial.println();
    }
    if (takePhoto == "1"){
      Firebase.setString(fbdo, "/states/takePhoto", "0");
      Firebase.setString(fbdo, "/photo/picture", Photo2Base64());
    }
  }
}
