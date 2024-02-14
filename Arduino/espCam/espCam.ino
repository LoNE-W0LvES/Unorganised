#include <WiFi.h>
#include <FirebaseESP32.h>
#include "Base64.h"

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#include "soc/soc.h" //Used for unstable power supply without rebooting
#include "soc/rtc_cntl_reg.h" //Used for unstable power supply and restarting
#include "esp_camera.h" //Video function
#include "img_converters.h" //Image format conversion function
#include "fb_gfx.h" //image drawing function
#include "fd_forward.h" //Face detection function
#include "fr_forward.h" //Face recognition function
#include "FS.h" //File system functions
#include "SD_MMC.h" //SD card access function
#include <Preferences.h>
#include "ESPAsyncWebServer.h"
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
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"
#define ENROLL_CONFIRM_TIMES 5
#define FACE_ID_SAVE_NUMBER 7

const char* WIFI_SSID = "WIFI_SSID";
const char*  WIFI_PASSWORD = "WIFI_PASSWORD";
Preferences preferences;
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;
AsyncWebServer server(80);
IPAddress IP = {10, 10, 1, 1}; // curly braces
IPAddress gateway = IPAddress (10, 10, 2, 8); // not curly braces
IPAddress NMask = IPAddress (255, 255, 255, 0); // not curly braces
int staApSw = 0;
int takePhoto = 2;
int timeSwitch = 2;
int wifiRetry = 0;
String filepath[35] = {"/1.jpg", "/2.jpg", "/3.jpg", "/4.jpg", "/5.jpg", "/6.jpg", "/7.jpg", "/8.jpg", "/9.jpg", "/10.jpg", "/11.jpg", "/12.jpg", "/13.jpg", "/14.jpg", "/15.jpg", "/16.jpg", "/17.jpg", "/18.jpg", "/19.jpg", "/20.jpg", "/21.jpg", "/22.jpg", "/23.jpg", "/24.jpg", "/25.jpg", "/26.jpg", "/27.jpg", "/28.jpg", "/29.jpg", "/30.jpg", "/31.jpg", "/32.jpg", "/33.jpg", "/34.jpg", "/35.jpg"};
int interval = 5000;

char inByte;
int photoCount;
int faceMatch;
//initial value
static mtmn_config_t mtmn_config = {0};
static face_id_list id_list = {0};
int8_t enroll_id = 0;
unsigned long timeX, timeY, previousMillis;
box_array_t *net_boxes = NULL;


String Photo2Base64() {
    camera_fb_t * fb = NULL;
    fb = esp_camera_fb_get();  
    if(!fb) {
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


//void listDir(fs::FS &fs){
//    int countFile = 0;
//    File root = fs.open("/faceRecognition/");
//    if(!root){
//        return;
//    }
//    if(!root.isDirectory()){
//        return;
//    }
//    File file = root.openNextFile();
//    while(file){
//        if(!file.isDirectory()) {
//            String fileX = file.name();
//            if (fileX.indexOf(".jpg") > 0){
//              filepath[countFile] = "/faceRecognition" + fileX;
//              countFile += 1;
//            }
//        }
//        file = root.openNextFile();
//    }
//}


void encrollImageSD() {
  //Face detection parameter setting https://github.com/espressif/esp-face/blob/master/face_detection/README.md
  mtmn_config.type = FAST;  //FAST or NORMAL
  mtmn_config.min_face = 80;
  mtmn_config.pyramid = 0.707;
  mtmn_config.pyramid_times = 4;
  mtmn_config.p_threshold.score = 0.6;
  mtmn_config.p_threshold.nms = 0.7;
  mtmn_config.p_threshold.candidate_number = 20;
  mtmn_config.r_threshold.score = 0.7;
  mtmn_config.r_threshold.nms = 0.7;
  mtmn_config.r_threshold.candidate_number = 10;
  mtmn_config.o_threshold.score = 0.7;
  mtmn_config.o_threshold.nms = 0.7;
  mtmn_config.o_threshold.candidate_number = 1;
    
  // SD card initialization
  if(!SD_MMC.begin()){
    Serial.println("Card Mount Failed");
    ESP.restart();
  }  
  
  fs::FS &fs = SD_MMC;
  
  face_id_init(&id_list, FACE_ID_SAVE_NUMBER, ENROLL_CONFIRM_TIMES);
  dl_matrix3du_t *aligned_face = NULL;
  int8_t left_sample_face = NULL;
  dl_matrix3du_t *image_matrix = NULL;
  
  for (int j=0;j<sizeof(filepath)/sizeof(*filepath);j++) {
    File file = fs.open(filepath[j]);
    if(!file){
      SD_MMC.end();    
    } else {
      char *buf;
      buf = (char*) malloc (sizeof(char)*file.size());
      long i = 0;
      while (file.available()) {
        buf[i] = file.read(); 
        i++;  
      }

      image_matrix = dl_matrix3du_alloc(1, 400, 296, 3); // allocate internal memory
      if (image_matrix) {          
          fmt2rgb888((uint8_t*)buf, file.size(), PIXFORMAT_JPEG, image_matrix->item); //Image format conversion RGB format
          box_array_t *net_boxes = face_detect(image_matrix, &mtmn_config); //Execute face detection to obtain face frame data
          if (net_boxes){
            for (int i = 0; i < net_boxes->len; i++){ //List the position and size of faces
                int x = (int)net_boxes->box[i].box_p[0];
                int y = (int)net_boxes->box[i].box_p[1];
                int w = (int)net_boxes->box[i].box_p[2] - x + 1;
                int h = (int)net_boxes->box[i].box_p[3] - y + 1;

                //Register face
                if (i==0) {
                  aligned_face = dl_matrix3du_alloc(1, FACE_WIDTH, FACE_HEIGHT, 3);
                  if (align_face(net_boxes, image_matrix, aligned_face) == ESP_OK){
                    if(aligned_face) {
                      left_sample_face = enroll_face(&id_list, aligned_face);
          
                      if(left_sample_face == (ENROLL_CONFIRM_TIMES - 1)){
                          enroll_id = id_list.tail;
                      }
                      if (left_sample_face == 0){
                          enroll_id = id_list.tail;
                      }
                    }
                    dl_matrix3du_free(aligned_face);
                  }
                }
            } 
            dl_lib_free(net_boxes->score);
            dl_lib_free(net_boxes->box);
            dl_lib_free(net_boxes->landmark);
            dl_lib_free(net_boxes);                                
            net_boxes = NULL;
          }
          dl_matrix3du_free(image_matrix);
      }
      free(buf);
    }
    file.close();
  } 
  
  SD_MMC.end();
  Serial.println();

  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);   
}

void faceRecognition() {
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();
  if (!fb) {
      ESP.restart();
  }
  size_t out_len, out_width, out_height;
  uint8_t * out_buf;
  bool s;
  dl_matrix3du_t *image_matrix = dl_matrix3du_alloc(1, fb->width, fb->height, 3);
  if (!image_matrix) {
      esp_camera_fb_return(fb);
      return;
  }
  out_buf = image_matrix->item;
  out_len = fb->width * fb->height * 3;
  out_width = fb->width;
  out_height = fb->height;
  s = fmt2rgb888(fb->buf, fb->len, fb->format, out_buf);
  esp_camera_fb_return(fb);
  if(!s){
      dl_matrix3du_free(image_matrix);
      return;
  }
  box_array_t *net_boxes = face_detect(image_matrix, &mtmn_config); //Execute face detection
  if (net_boxes){
      run_face_recognition(image_matrix, net_boxes); //Execute face recognition
      dl_lib_free(net_boxes->score);
      dl_lib_free(net_boxes->box);
      dl_lib_free(net_boxes->landmark);
      dl_lib_free(net_boxes);                                
      net_boxes = NULL;
  }
  dl_matrix3du_free(image_matrix);
}

//Face recognition function
static int run_face_recognition(dl_matrix3du_t *image_matrix, box_array_t *net_boxes){  
    dl_matrix3du_t *aligned_face = NULL;
    int matched_id = 0;

    aligned_face = dl_matrix3du_alloc(1, FACE_WIDTH, FACE_HEIGHT, 3);
    if(!aligned_face){
        return matched_id;
    }
    if (align_face(net_boxes, image_matrix, aligned_face) == ESP_OK){
        matched_id = recognize_face(&id_list, aligned_face); //face recognition
        if (matched_id >= 0) {
          faceMatch = 1;
          Serial.println("zx");
        }
    }
    dl_matrix3du_free(aligned_face);
    return matched_id;
}

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //The setting of restarting when the power is turned off unstable
  Serial.begin(115200);
  delay(2000);
  Serial.setDebugOutput(true); //Enable diagnostic output
  preferences.begin("wifiCred", false);
  staApSw = preferences.getInt("switch", 0);
  if (staApSw == 1) {
    String ssidStr = preferences.getString("ssid", "");
    String passStr = preferences.getString("pass", "");
    WIFI_SSID = ssidStr.c_str();
    WIFI_PASSWORD = passStr.c_str();
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.println(WIFI_SSID);
    Serial.println(WIFI_PASSWORD);
    while (true) {
      while ((WiFi.status() != WL_CONNECTED) && (wifiRetry < 20)) {
        Serial.print(".");
        delay(300);
        wifiRetry++;
      }
      if (WiFi.status() == WL_CONNECTED){
        break;
      } else {
      wifiRetry = 0;
      WiFi.disconnect();
      WiFi.reconnect();
      staApSw = 0;
      }
    }
  } else if (staApSw == 0) {
    WiFi.mode(WIFI_AP);
    WiFi.softAP("EspCam", "password1234");
    delay(1000);
    WiFi.softAPConfig(IP, IP, NMask);
    delay(1000);
  }

  server.on("/ssid", HTTP_GET, [](AsyncWebServerRequest *request){
    staApSw += 2;
    timeY = millis();
    String ssid;
    if (request->hasParam("value")) {
      ssid = request->getParam("value")->value();
    }
    preferences.putString("ssid", ssid);
    request->send(200, "text/plain", ssid);
  });
  server.on("/pass", HTTP_GET, [](AsyncWebServerRequest *request){
    staApSw += 2;
    timeY = millis();
    String pass;
    if (request->hasParam("value")) {
      pass = request->getParam("value")->value();
    }
    preferences.putString("pass", pass);
    request->send(200, "text/plain", pass);
  });
  server.on("/photo", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", Photo2Base64());
  });
  server.begin();

  //Video configuration settings https://github.com/espressif/esp32-camera/blob/master/driver/include/esp_camera.h
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

  if(psramFound()){
    configcam.frame_size = FRAMESIZE_UXGA;
    configcam.jpeg_quality = 10;
    configcam.fb_count = 2;
  } else {
    configcam.frame_size = FRAMESIZE_SVGA;
    configcam.jpeg_quality = 12;
    configcam.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&configcam);
  if (err != ESP_OK) {
    ESP.restart();
  }

  sensor_t * s = esp_camera_sensor_get();
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  s->set_framesize(s, FRAMESIZE_CIF);
  ledcAttachPin(4, 4);  
  ledcSetup(4, 5000, 8);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  /* Assign the api key (required) */
  config.api_key = API_KEY;

  config.database_url = DATABASE_URL;
  Firebase.begin(DATABASE_URL, API_KEY);

  Firebase.setDoubleDigits(5);
  if(!SD_MMC.begin()){
        return;
    }
    uint8_t cardType = SD_MMC.cardType();

    if(cardType == CARD_NONE){
        return;
    }
    encrollImageSD();
    timeX = millis();
}

void loop() {
  if (staApSw == 1) {
    if ((WiFi.status() != WL_CONNECTED) && (millis() - previousMillis >=interval)) {
      WiFi.disconnect();
      WiFi.reconnect();
      while (true) {
        while ((WiFi.status() != WL_CONNECTED) || (wifiRetry < 10)) {
          Serial.print(".");
          delay(300);
          wifiRetry++;
        }
        if (WiFi.status() == WL_CONNECTED){
          break;
        } else {
        wifiRetry = 0;
        WiFi.disconnect();
        WiFi.reconnect();
        }
      }
      previousMillis = millis();
    }
    if (Firebase.ready()) {
    Firebase.getInt(fbdo, "/states/takePhoto");
    takePhoto = fbdo.to<int>();
    if (takePhoto == 1) {
        takePhoto = 0;
        Firebase.setInt(fbdo, "/states/takePhoto", 0);
        timeSwitch = 1;
        timeX = millis();
        Firebase.getInt(fbdo, "/photo/pictureCount");
        photoCount = fbdo.to<int>();
        if (photoCount == 0)
          photoCount = 1;
        Firebase.setString(fbdo, "/photo/picture" + String(photoCount), Photo2Base64());
        if (photoCount > 20){
          photoCount = 1;
        } else {
          photoCount += 1;
        }
        Firebase.setInt(fbdo, "/photo/pictureCount", photoCount);
        
    }
    if (faceMatch == 1) {
      faceMatch = 0;
      Firebase.setInt(fbdo, "/states/doorStateApp", 1);
      Firebase.setInt(fbdo, "/states/dataUpdate", 1);
    }
    if (timeSwitch == 1) {
      if((millis() - timeX)> 10000){
        Firebase.setInt(fbdo, "/states/doorBellDevice", 0);
        timeSwitch = 0;
      }
    }
  }
  } else if (staApSw >= 4) {
    if (millis() - timeY > 10000){
      preferences.putInt("switch", 1);
      ESP.restart();
    }    
  }
  if (Serial.available()) {
    inByte = Serial.read();
    if (inByte == 'zz'){
      preferences.putInt("switch", 0);
      ESP.restart();
    }
  }
  faceRecognition();
  delay(100);
}
