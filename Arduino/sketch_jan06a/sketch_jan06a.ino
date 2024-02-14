#include <WiFi.h>
#include <WiFiClientSecure.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "esp_camera.h"
#include "fd_forward.h"
#include "FS.h"
#include "SD_MMC.h"
#include <Preferences.h>
Preferences preferences;

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

box_array_t *net_boxes = NULL;
char img = 'z';
void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
    
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

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
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    ESP.restart();
  }

  sensor_t * s = esp_camera_sensor_get();
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_CIF);  // UXGA|SXGA|XGA|SVGA|VGA|CIF|QVGA|HQVGA|QQVGA

  ledcAttachPin(4, 4);  
  ledcSetup(4, 5000, 8);

  //SD Card
  if(!SD_MMC.begin()){
    Serial.println("Card Mount Failed");
    return;
  }

  uint8_t cardType = SD_MMC.cardType();

  if(cardType == CARD_NONE){
    Serial.println("No SD_MMC card attached");
    SD_MMC.end();
    return;
  }

  Serial.print("SD_MMC Card Type: ");
  if(cardType == CARD_MMC){
      Serial.println("MMC");
  } else if(cardType == CARD_SD){
      Serial.println("SDSC");
  } else if(cardType == CARD_SDHC){
      Serial.println("SDHC");
  } else {
      Serial.println("UNKNOWN");
  }    

  Serial.printf("SD_MMC Card Size: %lluMB\n", SD_MMC.cardSize() / (1024 * 1024));
  Serial.printf("Total space: %lluMB\n", SD_MMC.totalBytes() / (1024 * 1024));
  Serial.printf("Used space: %lluMB\n", SD_MMC.usedBytes() / (1024 * 1024));
  Serial.println();
  preferences.begin("SD", false);
  preferences.putUInt("number", 0);
  preferences.end();
  SD_MMC.end();  
   
  /*
  preferences.begin("SD", false);
  preferences.putUInt("number", 0);
  preferences.end(); 
  */ 
}

void loop() {
  if (Serial.available()) {
    img = Serial.read();
  }
  if (img == 't') {
    img = 'z';
    Serial.println("Starting");
    saveCapturedImage2SD();
    delay(3000);
  }
}

void saveCapturedImage2SD() {
  dl_matrix3du_t *image_matrix = NULL;
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();
  if(!SD_MMC.begin()){
    Serial.println("Card Mount Failed");
    return;
  } 
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  } else {
      image_matrix = dl_matrix3du_alloc(1, fb->width, fb->height, 3);  //分配內部記憶體
      if (!image_matrix) {
          Serial.println("dl_matrix3du_alloc failed");
      } else {
          //臉部偵測參數設定  https://github.com/espressif/esp-face/blob/master/face_detection/README.md
          static mtmn_config_t mtmn_config = {0};
          mtmn_config.type = FAST;
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
          
          fmt2rgb888(fb->buf, fb->len, fb->format, image_matrix->item);  //影像格式轉換RGB格式
          net_boxes = face_detect(image_matrix, &mtmn_config);  //執行人臉偵測取得臉框數據
          if (net_boxes){
            preferences.begin("SD", false);
            int n = preferences.getUInt("number", 0);
            String path = "/"+ String(n+1) +".jpg";
            fs::FS &fs = SD_MMC; 
            Serial.printf("Picture file name: %s\n", path.c_str());
          
            File file = fs.open(path.c_str(), FILE_WRITE);
            if(!file){
              Serial.println("Failed to open file in writing mode");
            } 
            else {
              file.write(fb->buf, fb->len);
              Serial.printf("Saved file to path: %s\n", path.c_str());
            }
            file.close();
            
            file = fs.open(path.c_str());
            Serial.println("File Size = " + String(file.size()));
            
            if (file.size()==0) {
              Serial.println("Failed");
              file.close();
              
              Serial.println("Try again...");
          
              file = fs.open(path.c_str(), FILE_WRITE);
              if (file) {
                file.write(fb->buf, fb->len);
                file.close();
              
                file = fs.open(path.c_str());
                Serial.println("File Size = " + String(file.size()));
                if (file.size()==0) {
                  Serial.println("Failed");
                }
                else {
                  Serial.println("Success");
                }
              }
              else {
                Serial.println("Failed");
              }
            }
            else {
              Serial.println("Success");
            }
            file.close();
            SD_MMC.end();
            preferences.putUInt("number", (n+1));
            preferences.end();
            Serial.println("");  
//            dl_lib_free(net_boxes->score);
//            dl_lib_free(net_boxes->box);
//            dl_lib_free(net_boxes->landmark);
//            dl_lib_free(net_boxes);                                
//            net_boxes = NULL;
          } else {
            Serial.println("No Face");    //未偵測到的人臉
            Serial.println();
          }
          dl_lib_free(net_boxes->score);
          dl_lib_free(net_boxes->box);
          dl_lib_free(net_boxes->landmark);
          dl_lib_free(net_boxes);                                
          net_boxes = NULL;
          dl_matrix3du_free(image_matrix);
      }
      esp_camera_fb_return(fb);
  }
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);  
}


void listDir(fs::FS &fs, const char * dirname, uint8_t levels){
    Serial.printf("Listing directory: %s\n", dirname);

    File root = fs.open(dirname);
    if(!root){
        Serial.println("Failed to open directory");
        return;
    }
    if(!root.isDirectory()){
        Serial.println("Not a directory");
        return;
    }

    File file = root.openNextFile();
    while(file){
        if(file.isDirectory()){
            Serial.print("  DIR : ");
            Serial.println(file.name());
            if(levels){
                listDir(fs, file.name(), levels -1);
            }
        } else {
            Serial.print("  FILE: ");
            Serial.print(file.name());
            Serial.print("  SIZE: ");
            Serial.println(file.size());
        }
        file = root.openNextFile();
    }
}

void createDir(fs::FS &fs, const char * path){
    Serial.printf("Creating Dir: %s\n", path);
    if(fs.mkdir(path)){
        Serial.println("Dir created");
    } else {
        Serial.println("mkdir failed");
    }
}

void removeDir(fs::FS &fs, const char * path){
    Serial.printf("Removing Dir: %s\n", path);
    if(fs.rmdir(path)){
        Serial.println("Dir removed");
    } else {
        Serial.println("rmdir failed");
    }
}

void readFile(fs::FS &fs, const char * path){
    Serial.printf("Reading file: %s\n", path);

    File file = fs.open(path);
    if(!file){
        Serial.println("Failed to open file for reading");
        return;
    }

    Serial.print("Read from file: ");
    while(file.available()){
        Serial.write(file.read());
    }
}

void writeFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("Writing file: %s\n", path);

    File file = fs.open(path, FILE_WRITE);
    if(!file){
        Serial.println("Failed to open file for writing");
        return;
    }
    if(file.print(message)){
        Serial.println("File written");
    } else {
        Serial.println("Write failed");
    }
}

void appendFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("Appending to file: %s\n", path);

    File file = fs.open(path, FILE_APPEND);
    if(!file){
        Serial.println("Failed to open file for appending");
        return;
    }
    if(file.print(message)){
        Serial.println("Message appended");
    } else {
        Serial.println("Append failed");
    }
}

void renameFile(fs::FS &fs, const char * path1, const char * path2){
    Serial.printf("Renaming file %s to %s\n", path1, path2);
    if (fs.rename(path1, path2)) {
        Serial.println("File renamed");
    } else {
        Serial.println("Rename failed");
    }
}

void deleteFile(fs::FS &fs, const char * path){
    Serial.printf("Deleting file: %s\n", path);
    if(fs.remove(path)){
        Serial.println("File deleted");
    } else {
        Serial.println("Delete failed");
    }
}

void testFileIO(fs::FS &fs, const char * path){
    File file = fs.open(path);
    static uint8_t buf[512];
    size_t len = 0;
    uint32_t start = millis();
    uint32_t end = start;
    if(file){
        len = file.size();
        size_t flen = len;
        start = millis();
        while(len){
            size_t toRead = len;
            if(toRead > 512){
                toRead = 512;
            }
            file.read(buf, toRead);
            len -= toRead;
        }
        end = millis() - start;
        Serial.printf("%u bytes read for %u ms\n", flen, end);
        file.close();
    } else {
        Serial.println("Failed to open file for reading");
    }


    file = fs.open(path, FILE_WRITE);
    if(!file){
        Serial.println("Failed to open file for writing");
        return;
    }

    size_t i;
    start = millis();
    for(i=0; i<2048; i++){
        file.write(buf, 512);
    }
    end = millis() - start;
    Serial.printf("%u bytes written for %u ms\n", 2048 * 512, end);
    file.close();
}
