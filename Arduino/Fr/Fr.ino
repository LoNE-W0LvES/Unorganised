/*
ESP32-CAM Load images from SD card to enroll faces and recognize faces automatically.
Author : ChungYi Fu (Kaohsiung, Taiwan) 2021-6-29 21:30
https://www.facebook.com/francefu
*/

// Face recognition number of registered images of the same person's face
#define ENROLL_CONFIRM_TIMES 5

// You can get the resolution CIF image from the get-still button on the webpage and save it to the SD card http://192.168.xxx.xxx/capture (FRAMESIZE_CIF)
String filepath[35] = {"/1.jpg", "/2.jpg", "/3.jpg", "/4.jpg", "/5.jpg", "/6.jpg", "/7.jpg", "/8.jpg", "/9.jpg", "/10.jpg", "/11.jpg", "/12.jpg", "/13.jpg", "/14.jpg", "/15.jpg", "/16.jpg", "/17.jpg", "/18.jpg", "/19.jpg", "/20.jpg", "/21.jpg", "/22.jpg", "/23.jpg", "/24.jpg", "/25.jpg", "/26.jpg", "/27.jpg", "/28.jpg", "/29.jpg", "/30.jpg", "/31.jpg", "/32.jpg", "/33.jpg", "/34.jpg", "/35.jpg"};  //1.jpg, 2.jpg, ...., 35.jpg
int image_width = 400;  
int image_height = 296;

// Face recognition number of registered images of the same person's face
#define ENROLL_CONFIRM_TIMES 5
// Face recognition registration number
#define FACE_ID_SAVE_NUMBER 7

// Set the name of the person displayed by face recognition
String recognize_face_matched_name[7] = {"Name0","Name1","Name2","Name3","Name4","Name5","Name6"};
# include  "ESP32Servo.h"
# include  "soc/soc.h"              // Used for unstable power supply
# include  "soc/rtc_cntl_reg.h"     // Used for unstable power supply
# include  "esp_camera.h"           // Video function
# include  "img_converters.h"       // Image format conversion function
# include  "fb_gfx.h"               // image drawing function
# include  "fd_forward.h"           // Face detection function
# include  "fr_forward.h"           // Face recognition function
# include  "FS.h"                   // File system functions
# include  "SD_MMC.h"               // SD card access function
#include "WiFi.h"
#include "esp_timer.h"
#include "driver/rtc_io.h"
#include <ESPAsyncWebServer.h>
#include <StringArray.h>
#include <SPIFFS.h>
#include <EEPROM.h>            // read and write from flash memory
// #include "Arduino.h"

// Anxinke ESP32-CAM module pin setting
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

#define EEPROM_SIZE 1
Servo myservo;
// initial value
static mtmn_config_t mtmn_config = {0};
static face_id_list id_list = {0};
int8_t enroll_id = 0;
int pictureNumber = 0;

//https://github.com/espressif/esp-dl/blob/master/face_detection/README.md
box_array_t *net_boxes = NULL;

// Replace with your network credentials
const char* ssid = "Lab";
const char* password = "cselab@221";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

boolean takeNewPhoto = false;
boolean lockDoor = false;
boolean openDoor = false;
boolean doorClosed = false;
boolean doorBell = false;

// Photo File Name to save in SPIFFS
#define FILE_PHOTO "/photo.jpg"

void  FaceMatched ( int faceid) {   // Identify the registered face and execute the command control
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

void  FaceNoMatched () {   // Identify as a stranger face and execute command control
  
}


// Check if photo capture was successful
bool checkPhoto( fs::FS &fs ) {
  File f_pic = fs.open( FILE_PHOTO );
  unsigned int pic_sz = f_pic.size();
  return ( pic_sz > 100 );
}

// Capture Photo and Save it to SPIFFS
void capturePhotoSaveSpiffs( void ) {
  camera_fb_t * fb = NULL; // pointer
  bool ok = 0; // Boolean indicating if the picture has been taken correctly

  do {
    // Take a photo with the camera
    Serial.println("Taking a photo...");

    fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed");
      return;
    }

    // Photo file name
    Serial.printf("Picture file name: %s\n", FILE_PHOTO);
    File file = SPIFFS.open(FILE_PHOTO, FILE_WRITE);

    // Insert the data in the photo file
    if (!file) {
      Serial.println("Failed to open file in writing mode");
    }
    else {
      file.write(fb->buf, fb->len); // payload (image), payload length
      Serial.print("The picture has been saved in ");
      Serial.print(FILE_PHOTO);
      Serial.print(" - Size: ");
      Serial.print(file.size());
      Serial.println(" bytes");
    }
    // Close the file
    file.close();
    esp_camera_fb_return(fb);

    // check if file has been correctly saved in SPIFFS
    ok = checkPhoto(SPIFFS);
    digitalWrite(4, LOW);
  } while ( !ok );
}


void encrollImageSD() {
  // Face detection parameter setting https://github.com/espressif/esp-face/blob/master/face_detection/README.md
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
  
      image_matrix = dl_matrix3du_alloc ( 1 , image_width, image_height, 3 );   // allocate internal memory
      if (!image_matrix) {
          Serial.println("dl_matrix3du_alloc failed");
      } else {          
          fmt2rgb888 (( uint8_t *)buf, file.size (), PIXFORMAT_JPEG, image_matrix-> item );   // Image format conversion to RGB format
          box_array_t *net_boxes = face_detect (image_matrix, &mtmn_config);   // Execute face detection to get face frame data
          if (net_boxes){
            Serial. println ( " faces = " + String (net_boxes-> len ));   // Number of detected faces
            Serial.println();
            for ( int i = 0 ; i < net_boxes-> len ; i++){   // List face position and size
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

                // register face
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
            Serial. println ( " No Face " );     // No face detected
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
  box_array_t *net_boxes = face_detect (image_matrix, &mtmn_config);   // Execute face detection
  if (net_boxes){
      pinMode(4, OUTPUT);
      digitalWrite(4, HIGH);
      delay(1000);
      capturePhotoSaveSpiffs();
      run_face_recognition (image_matrix, net_boxes);   // Execute face recognition
      dl_lib_free(net_boxes->score);
      dl_lib_free(net_boxes->box);
      dl_lib_free(net_boxes->landmark);
      dl_lib_free(net_boxes);                                
      net_boxes = NULL;
  }
  dl_matrix3du_free(image_matrix);
}

// face recognition function
static int run_face_recognition(dl_matrix3du_t *image_matrix, box_array_t *net_boxes){  
    dl_matrix3du_t *aligned_face = NULL;
    int matched_id = 0;

    aligned_face = dl_matrix3du_alloc(1, FACE_WIDTH, FACE_HEIGHT, 3);
    if(!aligned_face){
        Serial.println("Could not allocate face recognition buffer");
        return matched_id;
    }
    if (align_face(net_boxes, image_matrix, aligned_face) == ESP_OK){
        matched_id = recognize_face (&id_list, aligned_face);   // face recognition
        if (matched_id >= 0) {
            myservo.write(180);
            Serial.printf("Match Face ID: %u\n", matched_id);
            int name_length = sizeof(recognize_face_matched_name) / sizeof(recognize_face_matched_name[0]);
            if (matched_id<name_length) {
              // Display the recognized name in the video screen
              Serial.printf("Match Face Name: %s\n", recognize_face_matched_name[matched_id]);
            }
            else {
              Serial.printf("Match Face Name: No name");
            }  
            Serial.println();
            FaceMatched (matched_id);   // Identify the registered face and execute the command control
        } else {
            Serial. println ( " No Match Found " );   // Identified as a stranger's face
            Serial.println();
            matched_id = -1;
            FaceNoMatched ();   // Identify as a stranger face and execute command control
        }
    } else {
        Serial.println("Face Not Aligned");
        Serial.println();
    }

    dl_matrix3du_free(aligned_face);
    return matched_id;
}

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { text-align:center; }
    .vert { margin-bottom: 10%; }
    .hori{ margin-bottom: 0%; }
  </style>
</head>
<body>
  <div id="container">
    <h2>ESP32-CAM Last Photo</h2>
    <p>It might take more than 5 seconds to capture a photo.</p>
    <p>
      <button onclick="rotatePhoto();">ROTATE</button>
      <button onclick="capturePhoto()">CAPTURE PHOTO</button>
      <button onclick="lock()">LOCK</button>
      <button onclick="unlock()">UNLOCK</button>
      <button onclick="location.reload();">REFRESH PAGE</button>
    </p>
  </div>
  <div><img src="saved-photo" id="photo" width="70%"></div>
</body>
<script>
  if (!!window.EventSource) {
    var source = new EventSource('/events');
    
    source.addEventListener('open', function(e) {
      console.log("Events Connected");
    }, false);
    source.addEventListener('error', function(e) {
      if (e.target.readyState != EventSource.OPEN) {
        console.log("Events Disconnected");
      }
    }, false);
    
    source.addEventListener('message', function(e) {
      console.log("message", e.data);
    }, false);
    
    source.addEventListener('temperature', function(e) {
      console.log("temperature", e.data);
      document.getElementById("temp").innerHTML = e.data;
    }, false);
    
    source.addEventListener('humidity', function(e) {
      console.log("humidity", e.data);
      document.getElementById("hum").innerHTML = e.data;
    }, false);
    
    source.addEventListener('pressure', function(e) {
      console.log("pressure", e.data);
      document.getElementById("pres").innerHTML = e.data;
    }, false);
  }
  var deg = 0;
  function capturePhoto() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/capture", true);
    xhr.send();
  }
    function lock() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/lock", true);
    xhr.send();
  }
      function unlock() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/unlock", true);
    xhr.send();
  }
  function rotatePhoto() {
    var img = document.getElementById("photo");
    deg += 90;
    if(isOdd(deg/90)){ document.getElementById("container").className = "vert"; }
    else{ document.getElementById("container").className = "hori"; }
    img.style.transform = "rotate(" + deg + "deg)";
  }
  function isOdd(n) { return Math.abs(n % 2) == 1; }
</script>
</html>)rawliteral";

void setup() {
  WRITE_PERI_REG (RTC_CNTL_BROWN_OUT_REG, 0 );   // Setting to restart when the power supply is unstable
    
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  if (!SPIFFS.begin(true)) {
    Serial.println("An Error has occurred while mounting SPIFFS");
    ESP.restart();
  }
  else {
    delay(500);
    Serial.println("SPIFFS mounted successfully");
  }

  // Print ESP32 Local IP Address
  Serial.print("IP Address: http://");
  Serial.println(WiFi.localIP());

  // Turn-off the 'brownout detector'
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  Serial.setDebugOutput ( true );   // Enable diagnostic output
  Serial.println();

  // Video configuration settings https://github.com/espressif/esp32-camera/blob/master/driver/include/esp_camera.h
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  //
  // WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
  //            Ensure ESP32 Wrover Module or other board with PSRAM is selected
  //            Partial images will be transmitted if image exceeds buffer size
  //   
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if ( psramFound ()){   // Whether there is PSRAM (Psuedo SRAM) memory IC
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
    
  // SD card initialization
  if(!SD_MMC.begin()){
    Serial.println("Card Mount Failed");
    ESP.restart();
  }  
  // Initialize video
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    ESP.restart();
  }

  // Can customize the default video frame size (resolution size)
  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_CIF);    //解析度 UXGA(1600x1200), SXGA(1280x1024), XGA(1024x768), SVGA(800x600), VGA(640x480), CIF(400x296), QVGA(320x240), HQVGA(240x176), QQVGA(160x120), QXGA(2048x1564 for OV3660)

  // s->set_vflip(s, 1); // vertical flip
  // s->set_hmirror(s, 1); //horizontal mirror

  // Flash(GPIO4)
  ledcAttachPin(4, 4);  
  ledcSetup(4, 5000, 8);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest * request) {
    request->send_P(200, "text/html", index_html);
  });

  server.on("/capture", HTTP_GET, [](AsyncWebServerRequest * request) {
    takeNewPhoto = true;
    request->send_P(200, "text/plain", "Taking Photo");
  });
  server.on("/lock", HTTP_GET, [](AsyncWebServerRequest * request) {
    lockDoor = true;
    request->send_P(200, "text/plain", "Locking Door");
  });
  
  server.on("/unlock", HTTP_GET, [](AsyncWebServerRequest * request) {
    openDoor = true;
    request->send(200, "text/plain", "Unlocking Door");
  });

  server.on("/saved-photo", HTTP_GET, [](AsyncWebServerRequest * request) {
    request->send(SPIFFS, FILE_PHOTO, "image/jpg", false);
  });

  // Start server
  	// Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    // standard 50 hz servo
	myservo.attach(12, 500, 2400); // attaches the servo on pin 18 to the servo object
	// using default min/max of 1000us and 2000us
	// different servos may require different min/max settings
	// for an accurate 0 to 180 sweep
  pinMode(13, INPUT);
  pinMode(14, INPUT);
  pinMode(15, INPUT);
  pinMode(16, INPUT);
  server.begin();
  encrollImageSD ();   // Read SD card image file to register face
}

void loop() {
  // timeX = millis();
  // if (digitalRead(13) == HIGH) {
  //   doorClosed = true;
  // } else {
  //   doorClosed = false;
  // }
  // if (digitalRead(14) == HIGH) {
  //   lockDoor = true;
  // }
  // if (digitalRead(15) == HIGH) {
  //   openDoor = true;
  // }
  // if (digitalRead(16) == HIGH) {
  //   doorBell = true;
  //   timeY = millis();
  // }

  // if ((timeX - timeY) > 10000){
  //   doorBell = false;
  //   lockDoor = true;
  // }
  // if (lockDoor){
  //   if (doorClosed){
  //     myservo.write(0);
  //     lockDoor = false;
  //   }
  // }

  // if ((openDoor) || (!doorClosed)) {
  //   myservo.write(180);
  //   openDoor = false;
  // }

  if (takeNewPhoto) {
    capturePhotoSaveSpiffs();
    takeNewPhoto = false;
  }
  if (!lockDoor){
    // starting dalay
    delay(20000);
    lockDoor = true;

  }
  //after 20 sec refrash page to see if changed anything
  doorBell = true;
  faceRecognition();
  delay(100);
}
