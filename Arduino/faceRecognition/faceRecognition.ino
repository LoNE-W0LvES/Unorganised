#define ENROLL_CONFIRM_TIMES 5

#define FACE_ID_SAVE_NUMBER 7

String filepath[35] = {"/1.jpg", "/2.jpg", "/3.jpg", "/4.jpg", "/5.jpg", "/6.jpg", "/7.jpg", "/8.jpg", "/9.jpg", "/10.jpg", "/11.jpg", "/12.jpg", "/13.jpg", "/14.jpg", "/15.jpg", "/16.jpg", "/17.jpg", "/18.jpg", "/19.jpg", "/20.jpg", "/21.jpg", "/22.jpg", "/23.jpg", "/24.jpg", "/25.jpg", "/26.jpg", "/27.jpg", "/28.jpg", "/29.jpg", "/30.jpg", "/31.jpg", "/32.jpg", "/33.jpg", "/34.jpg", "/35.jpg"};  //1.jpg, 2.jpg, ...., 35.jpg
int image_width = 400;  
int image_height = 296;


String recognize_face_matched_name[7] = {"Rana","Tuhin","GalibSir","Name3","Name4","Name5","Name6"};

# include  " soc/soc.h "              // Used for unstable power supply without rebooting
# include  " soc/rtc_cntl_reg.h "     // Used for unstable power supply without rebooting
# include  " esp_camera.h "           // Video function
# include  " img_converters.h "       // Image format conversion function
# include  " fb_gfx.h "               // image drawing function
# include  " fd_forward.h "           // Face detection function
# include  " fr_forward.h "           // Face recognition function
# include  " FS.h "                   // File system functions
# include  " SD_MMC.h "               // SD card access function

// Anxinke ESP32-CAM module pin setting
#define PWDN_GPIO_NUM     32
# define  RESET_GPIO_NUM     - 1
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

// initial value
static mtmn_config_t mtmn_config = {0};
static face_id_list id_list = {0};
int8_t enroll_id = 0;

//https://github.com/espressif/esp-dl/blob/master/face_detection/README.md
box_array_t *net_boxes = NULL;

void  FaceMatched ( int faceid) {   // Recognize the registered face to execute command control
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

void  FaceNoMatched () {   // recognized as a stranger's face to execute command control
  
}

void setup() {
  WRITE_PERI_REG (RTC_CNTL_BROWN_OUT_REG, 0 );   // Settings for restarting when the power supply is unstable
    
  Serial.begin(115200);
  Serial.setDebugOutput ( true ) ;   // Enable diagnostic output
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

  // Video initialization
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    ESP.restart();
  }

  // You can customize the default size of the video frame (resolution size)
  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_CIF);    //解析度 UXGA(1600x1200), SXGA(1280x1024), XGA(1024x768), SVGA(800x600), VGA(640x480), CIF(400x296), QVGA(320x240), HQVGA(240x176), QQVGA(160x120), QXGA(2048x1564 for OV3660)

  // s->set_vflip(s, 1); //Vertical flip
  // s->set_hmirror(s, 1); //horizontal mirroring

  // Flash (GPIO4)
  ledcAttachPin(4, 4);  
  ledcSetup(4, 5000, 8);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);

  encrollImageSD ();   // Read SD card image file to register face
}

void loop() {
  faceRecognition();
  delay(100);
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
  
      image_matrix = dl_matrix3du_alloc ( 1 , image_width, image_height, 3 );   // allocate internal memory
      if (!image_matrix) {
          Serial.println("dl_matrix3du_alloc failed");
      } else {          
          fmt2rgb888 (( uint8_t *)buf, file.size ( ), PIXFORMAT_JPEG, image_matrix-> item );   // Image format conversion to RGB format
          box_array_t *net_boxes = face_detect (image_matrix, &mtmn_config);   // Execute face detection to obtain face frame data
          if (net_boxes){
            Serial.println ( " faces = " + String (net_boxes-> len ) );   // Number of detected faces
            Serial.println();
            for ( int i = 0 ; i < net_boxes-> len ; i++){   // enumerate face position and size
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

                // Register face
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
            Serial.println ( " No Face " ) ;     // No face detected
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
      run_face_recognition (image_matrix, net_boxes);   // Execute face recognition
      dl_lib_free(net_boxes->score);
      dl_lib_free(net_boxes->box);
      dl_lib_free(net_boxes->landmark);
      dl_lib_free(net_boxes);                                
      net_boxes = NULL;
  }
  dl_matrix3du_free(image_matrix);
}

// Face recognition function
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
            Serial.printf("Match Face ID: %u\n", matched_id);
            int name_length = sizeof(recognize_face_matched_name) / sizeof(recognize_face_matched_name[0]);
            if (matched_id<name_length) {
              // Display the recognized name on the video screen
              Serial.printf("Match Face Name: %s\n", recognize_face_matched_name[matched_id]);
            }
            else {
              Serial.printf("Match Face Name: No name");
            }  
            Serial.println();
            FaceMatched (matched_id);   // Recognize the registered face to execute command control
        } else {
            Serial.println ( " No Match Found " );   // Recognized as a stranger's face
            Serial.println();
            matched_id = -1;
            FaceNoMatched ();   // recognized as a stranger's face to execute command control
        }
    } else {
        Serial.println("Face Not Aligned");
        Serial.println();
    }

    dl_matrix3du_free(aligned_face);
    return matched_id;
}
