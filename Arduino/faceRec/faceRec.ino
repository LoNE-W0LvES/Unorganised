#include <WiFi.h>
#include <FirebaseESP32.h>
#include "Base64.h"


//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#define WIFI_SSID "Lab"
#define WIFI_PASSWORD "cselab@221"
#define DATABASE_URL "https://esp32door-f40d1-default-rtdb.firebaseio.com/"
#define API_KEY "PdIwO27LDYoQnLJw2cXkuncYkd1Z2qsJrhuBX5RM"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;


//Face recognition The number of registered images of the same person's face
#define ENROLL_CONFIRM_TIMES 5

//Face recognition registration number
#define FACE_ID_SAVE_NUMBER 7

//The resolution CIF image can be obtained from the get-still button on the web page and saved in the SD card http://192.168.xxx.xxx/capture (FRAMESIZE_CIF)
String filepath[35] = {};
int image_width = 400;  
int image_height = 296;

//Set the name of the person displayed by face recognition
String recognize_face_matched_name[7] = {"Name0","Name1","Name2","Name3","Name4","Name5","Name6"};

#include "soc/soc.h" //Used for unstable power supply without rebooting
#include "soc/rtc_cntl_reg.h" //Used for unstable power supply and restarting
#include "esp_camera.h" //Video function
#include "img_converters.h" //Image format conversion function
#include "fb_gfx.h" //image drawing function
#include "fd_forward.h" //Face detection function
#include "fr_forward.h" //Face recognition function
#include "FS.h" //File system functions
#include "SD_MMC.h" //SD card access function

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

char inByte;
int photoCount;
//initial value
static mtmn_config_t mtmn_config = {0};
static face_id_list id_list = {0};
int8_t enroll_id = 0;

//https://github.com/espressif/esp-dl/blob/master/face_detection/README.md
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


void listDir(fs::FS &fs){
    int countFile = 0;
    File root = fs.open("/");
    if(!root){
        return;
    }
    if(!root.isDirectory()){
        return;
    }
    File file = root.openNextFile();
    while(file){
        if(!file.isDirectory()) {
            String fileX = file.name();
            if (fileX.indexOf(".jpg") > 0){
              filepath[countFile] = fileX;
              countFile += 1;
            }
        }
        file = root.openNextFile();
    }
}


void FaceMatched(int faceid) { //Recognize the registered face to execute command control
  if (faceid==0) {  
  } 
  else if (faceid==1) { 
  }
  else if (faceid==2) { 
  }
  else if (faceid==3) { 
  }
  else if (faceid==4) { 
  }
  else if (faceid==5) { 
  }
  else if (faceid==6) {
  }
  else {
  }   
}

void FaceNoMatched() { //Recognize a stranger's face and execute command control
  
}


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
    Serial.println("detect file: "+filepath[j]);
    if(!file){
      Serial.println("Failed to open file for reading");
      SD_MMC.end();    
    } else {
      Serial.println("file size: "+String(file.size())); 
      char *buf;
      buf = (char*) malloc (sizeof(char)*file.size());
      long i = 0;
      while (file.available()) {
        buf[i] = file.read(); 
        i++;  
      }
  
      image_matrix = dl_matrix3du_alloc(1, image_width, image_height, 3); // allocate internal memory
      if (!image_matrix) {
          Serial.println("dl_matrix3du_alloc failed");
      } else {          
          fmt2rgb888((uint8_t*)buf, file.size(), PIXFORMAT_JPEG, image_matrix->item); //Image format conversion RGB format
          box_array_t *net_boxes = face_detect(image_matrix, &mtmn_config); //Execute face detection to obtain face frame data
          if (net_boxes){
            Serial.println("faces = " + String(net_boxes->len)); //Number of detected faces
            Serial.println();
            for (int i = 0; i < net_boxes->len; i++){ //List the position and size of faces
                Serial.println("index = " + String(i));
                int x = (int)net_boxes->box[i].box_p[0];
                Serial.println("x = " + String(x));
                int y = (int)net_boxes->box[i].box_p[1];
                Serial.println("y = " + String(y));
                int w = (int)net_boxes->box[i].box_p[2] - x + 1;
                Serial.println("width = " + String(w));
                int h = (int)net_boxes->box[i].box_p[3] - y + 1;
                Serial.println("height = " + String(h));
                Serial.println();

                //Register face
                if (i==0) {
                  aligned_face = dl_matrix3du_alloc(1, FACE_WIDTH, FACE_HEIGHT, 3);
                  if (align_face(net_boxes, image_matrix, aligned_face) == ESP_OK){
                    if(!aligned_face){
                        Serial.println("Could not allocate face recognition buffer");
                    } 
                    else {
                      left_sample_face = enroll_face(&id_list, aligned_face);
          
                      if(left_sample_face == (ENROLL_CONFIRM_TIMES - 1)){
                          enroll_id = id_list.tail;
                          Serial.printf("Enrolling Face ID: %d\n", enroll_id);
                      }
                      Serial.printf("Enrolling Face ID: %d sample %d\n", enroll_id, ENROLL_CONFIRM_TIMES - left_sample_face);
                      if (left_sample_face == 0){
                          enroll_id = id_list.tail;
                          //Serial.printf("Enrolled Face ID: %d\n", enroll_id);
                      }
                      Serial.println();
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
          else {
            Serial.println("No Face"); //No face detected
            Serial.println();
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
      Serial.println("Camera capture failed");
      ESP.restart();
  }
  size_t out_len, out_width, out_height;
  uint8_t * out_buf;
  bool s;
  dl_matrix3du_t *image_matrix = dl_matrix3du_alloc(1, fb->width, fb->height, 3);
  if (!image_matrix) {
      esp_camera_fb_return(fb);
      Serial.println("dl_matrix3du_alloc failed");
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
      Serial.println("to rgb888 failed");
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
        Serial.println("Could not allocate face recognition buffer");
        return matched_id;
    }
    if (align_face(net_boxes, image_matrix, aligned_face) == ESP_OK){
        matched_id = recognize_face(&id_list, aligned_face); //face recognition
        if (matched_id >= 0) {
            Serial.printf("Match Face ID: %u\n", matched_id);
            int name_length = sizeof(recognize_face_matched_name) / sizeof(recognize_face_matched_name[0]);
            if (matched_id<name_length) {
              //Display the recognized name on the video screen
              Serial.printf("Match Face Name: %s\n", recognize_face_matched_name[matched_id]);
            }
            else {
              Serial.printf("Match Face Name: No name");
            }  
            Serial.println();
            FaceMatched(matched_id); //Recognize the registered face to execute command control
        } else {
            Serial.println("No Match Found"); //recognized as a stranger's face
            Serial.println();
            matched_id = -1;
            FaceNoMatched(); //Identify as a stranger's face and execute command control
        }
    } else {
        Serial.println("Face Not Aligned");
        Serial.println();
    }

    dl_matrix3du_free(aligned_face);
    return matched_id;
}

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //The setting of restarting when the power is turned off unstable
  Serial.begin(115200);
  delay(2000);
  Serial.setDebugOutput(true); //Enable diagnostic output
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }

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

  //
  // WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
  //            Ensure ESP32 Wrover Module or other board with PSRAM is selected
  //            Partial images will be transmitted if image exceeds buffer size
  //   
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if(psramFound()){ //Whether there is PSRAM(Psuedo SRAM) memory IC
    configcam.frame_size = FRAMESIZE_UXGA;
    configcam.jpeg_quality = 10;
    configcam.fb_count = 2;
  } else {
    configcam.frame_size = FRAMESIZE_SVGA;
    configcam.jpeg_quality = 12;
    configcam.fb_count = 1;
  }

  //Video initialization
  esp_err_t err = esp_camera_init(&configcam);
  if (err != ESP_OK) {
    ESP.restart();
  }

  //You can customize the default size of the video frame (resolution size)
  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_CIF);    //解析度 UXGA(1600x1200), SXGA(1280x1024), XGA(1024x768), SVGA(800x600), VGA(640x480), CIF(400x296), QVGA(320x240), HQVGA(240x176), QQVGA(160x120), QXGA(2048x1564 for OV3660)

  //s->set_vflip(s, 1); //Vertical flip
  //s->set_hmirror(s, 1); //horizontal mirroring

  //Flash (GPIO4)
  ledcAttachPin(4, 4);  
  ledcSetup(4, 5000, 8);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  /* Assign the api key (required) */
  config.api_key = API_KEY;

  config.database_url = DATABASE_URL;
  Firebase.begin(DATABASE_URL, API_KEY);

  //Comment or pass false value when WiFi reconnection will control by your code or third party library
 // Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);
  if(!SD_MMC.begin()){
        return;
    }
    uint8_t cardType = SD_MMC.cardType();

    if(cardType == CARD_NONE){
        return;
    }
    listDir(SD_MMC);
    encrollImageSD(); //Read SD card image file to register face
}

void loop() {
  if (Firebase.ready()) {
    while (Serial.available() > 0) {
      inByte = Serial.read();
      if (inByte == '\n') {
        break;
      }
      if ( inByte == 't') {
        Firebase.getInt(fbdo, "/photo/pictureCount");
        photoCount = fbdo.to<int>();
        Firebase.setString(fbdo, "/photo/picture" + String(photoCount), Photo2Base64());
        if (photoCount == 20){
          photoCount = 0;
        } else {
          photoCount += 1;
        }
        Firebase.setInt(fbdo, "/photo/pictureCount", photoCount);
        Firebase.setInt(fbdo, "/states/takePhoto", 0);
      }
      inByte == 'p';
    }
  }
  faceRecognition();
  delay(100);
}
