/*
 * SPDX-FileCopyrightText: 2022-2023 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
#include "SPI.h"
#include <TFT_eSPI.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "webserver_index_html.h"
#include <WebServer.h>
#include <Preferences.h>
#include "usb/usb_host.h"

#include <ArduinoSort.h>
#include "hid_host.h"
#include "hid_usage_keyboard.h"
#include <Adafruit_NeoPixel.h>

#define PIN        48
#define buttonSw 13
#define Sensor 11
#define ldr 10

#define NUMPIXELS  1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
/* GPIO Pin number for quit from example logic */
#define APP_QUIT_PIN                GPIO_NUM_4

TFT_eSPI tft = TFT_eSPI();
Preferences preferences;
const int jsonSize = 1024;

int valuesSonar[7] = {};
unsigned long mtime = 0;
unsigned long stime = 0;
WebServer server(80);
HTTPClient http0;
int http_switch = 0;
long lastTimeButtonStateChanged = 0;
int buttonState;
int mode_wifi = 0;
int start_ap = 0;
int lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long time_wifi = 0;
unsigned long time_wifi1 = 0;
String wifi_ssid = "";
String wifi_password = "";
String secret_code = "";
int count = 0;
int flag = 0;
int swOn = 0;

String white = "#ffffff";
String black = "#000000";
String red = "#ff0000";
String green = "#00ff00";
String blue = "#0000ff";
String orange = "#ff7b00";
String pink = "#ff00ff";
String yellow = "#ffee00";
String purple = "#b703ff";

String qr_code;
String final_qr;
unsigned char key_char_x;
static const char *TAG = "example";
QueueHandle_t hid_host_event_queue;
bool user_shutdown = false;
int xx = 0;
/**
 * @brief HID Host event
 *
 * This event is used for delivering the HID Host event from callback to a task.
 */
typedef struct {
  hid_host_device_handle_t hid_device_handle;
  hid_host_driver_event_t event;
  void *arg;
} hid_host_event_queue_t;

/**
 * @brief HID Protocol string names
 */
static const char *hid_proto_name_str[] = {"NONE", "KEYBOARD"};

/**
 * @brief Key event
 */
typedef struct {
  enum key_state { KEY_STATE_PRESSED = 0x00, KEY_STATE_RELEASED = 0x01 } state;
  uint8_t modifier;
  uint8_t key_code;
} key_event_t;

/* Main char symbol for ENTER key */
#define KEYBOARD_ENTER_MAIN_CHAR '\r'
/* When set to 1 pressing ENTER will be extending with LineFeed during serial
 * debug output */
#define KEYBOARD_ENTER_LF_EXTEND 1

const uint8_t keycode2ascii[57][2] = {
    {0, 0},     /* HID_KEY_NO_PRESS        */
    {0, 0},     /* HID_KEY_ROLLOVER        */
    {0, 0},     /* HID_KEY_POST_FAIL       */
    {0, 0},     /* HID_KEY_ERROR_UNDEFINED */
    {'a', 'A'}, /* HID_KEY_A               */
    {'b', 'B'}, /* HID_KEY_B               */
    {'c', 'C'}, /* HID_KEY_C               */
    {'d', 'D'}, /* HID_KEY_D               */
    {'e', 'E'}, /* HID_KEY_E               */
    {'f', 'F'}, /* HID_KEY_F               */
    {'g', 'G'}, /* HID_KEY_G               */
    {'h', 'H'}, /* HID_KEY_H               */
    {'i', 'I'}, /* HID_KEY_I               */
    {'j', 'J'}, /* HID_KEY_J               */
    {'k', 'K'}, /* HID_KEY_K               */
    {'l', 'L'}, /* HID_KEY_L               */
    {'m', 'M'}, /* HID_KEY_M               */
    {'n', 'N'}, /* HID_KEY_N               */
    {'o', 'O'}, /* HID_KEY_O               */
    {'p', 'P'}, /* HID_KEY_P               */
    {'q', 'Q'}, /* HID_KEY_Q               */
    {'r', 'R'}, /* HID_KEY_R               */
    {'s', 'S'}, /* HID_KEY_S               */
    {'t', 'T'}, /* HID_KEY_T               */
    {'u', 'U'}, /* HID_KEY_U               */
    {'v', 'V'}, /* HID_KEY_V               */
    {'w', 'W'}, /* HID_KEY_W               */
    {'x', 'X'}, /* HID_KEY_X               */
    {'y', 'Y'}, /* HID_KEY_Y               */
    {'z', 'Z'}, /* HID_KEY_Z               */
    {'1', '!'}, /* HID_KEY_1               */
    {'2', '@'}, /* HID_KEY_2               */
    {'3', '#'}, /* HID_KEY_3               */
    {'4', '$'}, /* HID_KEY_4               */
    {'5', '%'}, /* HID_KEY_5               */
    {'6', '^'}, /* HID_KEY_6               */
    {'7', '&'}, /* HID_KEY_7               */
    {'8', '*'}, /* HID_KEY_8               */
    {'9', '('}, /* HID_KEY_9               */
    {'0', ')'}, /* HID_KEY_0               */
    {KEYBOARD_ENTER_MAIN_CHAR, KEYBOARD_ENTER_MAIN_CHAR}, /* HID_KEY_ENTER */
    {0, 0},      /* HID_KEY_ESC             */
    {'\b', 0},   /* HID_KEY_DEL             */
    {0, 0},      /* HID_KEY_TAB             */
    {' ', ' '},  /* HID_KEY_SPACE           */
    {'-', '_'},  /* HID_KEY_MINUS           */
    {'=', '+'},  /* HID_KEY_EQUAL           */
    {'[', '{'},  /* HID_KEY_OPEN_BRACKET    */
    {']', '}'},  /* HID_KEY_CLOSE_BRACKET   */
    {'\\', '|'}, /* HID_KEY_BACK_SLASH      */
    {'\\', '|'},
    /* HID_KEY_SHARP           */ // HOTFIX: for NonUS Keyboards repeat
                                  // HID_KEY_BACK_SLASH
    {';', ':'},                   /* HID_KEY_COLON           */
    {'\'', '"'},                  /* HID_KEY_QUOTE           */
    {'`', '~'},                   /* HID_KEY_TILDE           */
    {',', '<'},                   /* HID_KEY_LESS            */
    {'.', '>'},                   /* HID_KEY_GREATER         */
    {'/', '?'}                    /* HID_KEY_SLASH           */
};

static inline bool hid_keyboard_is_modifier_shift(uint8_t modifier) {
  if (((modifier & HID_LEFT_SHIFT) == HID_LEFT_SHIFT) ||
      ((modifier & HID_RIGHT_SHIFT) == HID_RIGHT_SHIFT)) {
    return true;
  }
  return false;
}

static inline bool hid_keyboard_get_char(uint8_t modifier, uint8_t key_code, unsigned char *key_char) {
  uint8_t mod = (hid_keyboard_is_modifier_shift(modifier)) ? 1 : 0;
  if ((key_code >= HID_KEY_A) && (key_code <= HID_KEY_SLASH)) {
    *key_char = keycode2ascii[key_code][mod];
  } else {
    return false;
  }
  return true;
}

static inline void hid_keyboard_print_char(unsigned char key_char) {
  if (!!key_char) {
    char keyCharArray[2];
    keyCharArray[0] = key_char;
    keyCharArray[1] = '\0';
    qr_code += String(keyCharArray);
#if (KEYBOARD_ENTER_LF_EXTEND)
    if (KEYBOARD_ENTER_MAIN_CHAR == key_char) {
      final_qr = qr_code;
      qr_code = "";
    }
#endif
  }
}

static void key_event_callback(key_event_t *key_event) {
  unsigned char key_char;
  if (key_event->KEY_STATE_PRESSED == key_event->state) {
    if (hid_keyboard_get_char(key_event->modifier, key_event->key_code, &key_char)) {                       
      hid_keyboard_print_char(key_char);
    }
  }
}

static inline bool key_found(const uint8_t *const src, uint8_t key, unsigned int length) {
  for (unsigned int i = 0; i < length; i++) {
    if (src[i] == key) {
      return true;
    }
  }
  return false;
}

static void hid_host_keyboard_report_callback(const uint8_t *const data, const int length) {
  hid_keyboard_input_report_boot_t *kb_report =
      (hid_keyboard_input_report_boot_t *)data;
  if (length < sizeof(hid_keyboard_input_report_boot_t)) {
    return;
  }
  static uint8_t prev_keys[HID_KEYBOARD_KEY_MAX] = {0};
  key_event_t key_event;
  for (int i = 0; i < HID_KEYBOARD_KEY_MAX; i++) {
    if (prev_keys[i] > HID_KEY_ERROR_UNDEFINED &&
        !key_found(kb_report->key, prev_keys[i], HID_KEYBOARD_KEY_MAX)) {
      key_event.key_code = prev_keys[i];
      key_event.modifier = 0;
      key_event.state = key_event.KEY_STATE_RELEASED;
      key_event_callback(&key_event);
    }

    // key has been pressed verification
    if (kb_report->key[i] > HID_KEY_ERROR_UNDEFINED &&
        !key_found(prev_keys, kb_report->key[i], HID_KEYBOARD_KEY_MAX)) {
      key_event.key_code = kb_report->key[i];
      key_event.modifier = kb_report->modifier.val;
      key_event.state = key_event.KEY_STATE_PRESSED;
      key_event_callback(&key_event);
    }
  }
  memcpy(prev_keys, &kb_report->key, HID_KEYBOARD_KEY_MAX);
}


void hid_host_interface_callback(hid_host_device_handle_t hid_device_handle, const hid_host_interface_event_t event, void *arg) {
  uint8_t data[64] = {0};
  size_t data_length = 0;
  hid_host_dev_params_t dev_params;
  ESP_ERROR_CHECK(hid_host_device_get_params(hid_device_handle, &dev_params));

  switch (event) {
  case HID_HOST_INTERFACE_EVENT_INPUT_REPORT:
    ESP_ERROR_CHECK(hid_host_device_get_raw_input_report_data(
        hid_device_handle, data, 64, &data_length));

    if (HID_SUBCLASS_BOOT_INTERFACE == dev_params.sub_class) {
      if (HID_PROTOCOL_KEYBOARD == dev_params.proto) {
        hid_host_keyboard_report_callback(data, data_length);
      }
    }

    break;
  case HID_HOST_INTERFACE_EVENT_DISCONNECTED:
    ESP_LOGI(TAG, "HID Device, protocol '%s' DISCONNECTED",
             hid_proto_name_str[dev_params.proto]);
    ESP_ERROR_CHECK(hid_host_device_close(hid_device_handle));
    break;
  case HID_HOST_INTERFACE_EVENT_TRANSFER_ERROR:
    ESP_LOGI(TAG, "HID Device, protocol '%s' TRANSFER_ERROR",
             hid_proto_name_str[dev_params.proto]);
    break;
  default:
    ESP_LOGE(TAG, "HID Device, protocol '%s' Unhandled event",
             hid_proto_name_str[dev_params.proto]);
    break;
  }
}

void hid_host_device_event(hid_host_device_handle_t hid_device_handle,
                           const hid_host_driver_event_t event, void *arg) {
  hid_host_dev_params_t dev_params;
  ESP_ERROR_CHECK(hid_host_device_get_params(hid_device_handle, &dev_params));
  const hid_host_device_config_t dev_config = {
      .callback = hid_host_interface_callback, .callback_arg = NULL};


  switch (event) {
  case HID_HOST_DRIVER_EVENT_CONNECTED:
    ESP_LOGI(TAG, "HID Device, protocol '%s' CONNECTED",
             hid_proto_name_str[dev_params.proto]);

    ESP_ERROR_CHECK(hid_host_device_open(hid_device_handle, &dev_config));
    if (HID_SUBCLASS_BOOT_INTERFACE == dev_params.sub_class) {
      ESP_ERROR_CHECK(hid_class_request_set_protocol(hid_device_handle,
                                                     HID_REPORT_PROTOCOL_BOOT));
      if (HID_PROTOCOL_KEYBOARD == dev_params.proto) {
        ESP_ERROR_CHECK(hid_class_request_set_idle(hid_device_handle, 0, 0));
      }
    }
    ESP_ERROR_CHECK(hid_host_device_start(hid_device_handle));
    break;
  default:
    break;
  }
}

static void usb_lib_task(void *arg) {
  const gpio_config_t input_pin = {
      .pin_bit_mask = BIT64(APP_QUIT_PIN),
      .mode = GPIO_MODE_INPUT,
      .pull_up_en = GPIO_PULLUP_ENABLE,
  };
  ESP_ERROR_CHECK(gpio_config(&input_pin));

  const usb_host_config_t host_config = {
      .skip_phy_setup = false,
      .intr_flags = ESP_INTR_FLAG_LEVEL1,
  };

  ESP_ERROR_CHECK(usb_host_install(&host_config));
  xTaskNotifyGive(arg);

  while (gpio_get_level(APP_QUIT_PIN) != 0) {
    uint32_t event_flags;
    usb_host_lib_handle_events(portMAX_DELAY, &event_flags);

    // Release devices once all clients has deregistered
    if (event_flags & USB_HOST_LIB_EVENT_FLAGS_NO_CLIENTS) {
      usb_host_device_free_all();
      ESP_LOGI(TAG, "USB Event flags: NO_CLIENTS");
    }
    // All devices were removed
    if (event_flags & USB_HOST_LIB_EVENT_FLAGS_ALL_FREE) {
      ESP_LOGI(TAG, "USB Event flags: ALL_FREE");
    }
  }
  // App Button was pressed, trigger the flag
  user_shutdown = true;
  ESP_LOGI(TAG, "USB shutdown");
  // Clean up USB Host
  vTaskDelay(10); // Short delay to allow clients clean-up
  ESP_ERROR_CHECK(usb_host_uninstall());
  vTaskDelete(NULL);
}

void hid_host_task(void *pvParameters) {
  hid_host_event_queue_t evt_queue;
  hid_host_event_queue = xQueueCreate(10, sizeof(hid_host_event_queue_t));

  // Wait queue
  while (!user_shutdown) {
    if (xQueueReceive(hid_host_event_queue, &evt_queue, pdMS_TO_TICKS(50))) {
      hid_host_device_event(evt_queue.hid_device_handle, evt_queue.event, evt_queue.arg);
    }
  }

  xQueueReset(hid_host_event_queue);
  vQueueDelete(hid_host_event_queue);
  vTaskDelete(NULL);
}

void hid_host_device_callback(hid_host_device_handle_t hid_device_handle,
                              const hid_host_driver_event_t event, void *arg) {
  const hid_host_event_queue_t evt_queue = {
      .hid_device_handle = hid_device_handle, .event = event, .arg = arg};
  xQueueSend(hid_host_event_queue, &evt_queue, 0);
}

void app_main(void) {
  BaseType_t task_created;
  ESP_LOGI(TAG, "HID Host example");
  task_created =
      xTaskCreatePinnedToCore(usb_lib_task, "usb_events", 4096,
                              xTaskGetCurrentTaskHandle(), 2, NULL, 0);
  assert(task_created == pdTRUE);
  ulTaskNotifyTake(false, 1000);
  const hid_host_driver_config_t hid_host_driver_config = {
      .create_background_task = true,
      .task_priority = 5,
      .stack_size = 4096,
      .core_id = 0,
      .callback = hid_host_device_callback,
      .callback_arg = NULL};

  ESP_ERROR_CHECK(hid_host_install(&hid_host_driver_config));
  user_shutdown = false;
  task_created =
      xTaskCreate(&hid_host_task, "hid_task", 4 * 1024, NULL, 2, NULL);
  assert(task_created == pdTRUE);
}

void getTime() {
  int tz           = -5;
  int dst          = 0;
  time_t now       = time(nullptr);
  unsigned timeout = 5000; // try for timeout
  unsigned start   = millis();
  configTime(tz * 3600, dst * 3600, "pool.ntp.org", "time.nist.gov");
  Serial.print("Waiting for NTP time sync: ");
  while (now < 8 * 3600 * 2 ) { // what is this ?
    delay(100);
    Serial.print(".");
    now = time(nullptr);
    count += 1;
    if(count == 60) {
      Serial.println("Reset..");
      ESP.restart();
    }
    if((millis() - start) > timeout){
      Serial.println("\n[ERROR] Failed to get NTP time.");
      return;
    }
  }
  Serial.println("");
  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.print("Current time: ");
  Serial.print(asctime(&timeinfo));
}


void setup() { 
  Serial.begin(115200);
  pixels.begin();
  pixels.setBrightness(80);
  show_color(white);
  app_main();
  loadWifiCredentials();
  getTime();
  server.on("/", HTTP_GET, []() {server.send(200, "text/html", index_html);});
  server.on("/scan-wifi", HTTP_GET, handleScanWifi);
  server.on("/wifisave", HTTP_GET, handleWifiSave);
  server.begin();
  Serial.println("HTTP server started");
  pinMode(buttonSw, INPUT);
  pinMode(Sensor, INPUT);
  pinMode(ldr, INPUT);
  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);
  qr_power();
}

int ldrRead(){
    for(int & i : valuesSonar){
        i = analogRead(ldr);
        delay(20);
    }
    sortArray(valuesSonar, 7);
    return valuesSonar[6];
}


void loop() {
  server.handleClient();
  // qr_power();
  // delete_cred();

  if(millis()-mtime > 10000 ){
    if(WiFi.status() == WL_CONNECTED){
      getTime();
      if (flag == 0) {
        show_color(green);
      } else if (flag == 1) {
        show_color(red);
      } else if (flag == 2) {
        show_color(blue);
      } else if (flag == 3) {
        show_color(purple);
      }
    } else {
      Serial.println("No Wifi");
      show_color(orange);
    }
    mtime = millis();
  }

  if (digitalRead(Sensor) == LOW) {
    if ((ldrRead() < 2000) && (swOn == 0)) {
      qr_power();
      delay(500);
    } else {
      swOn = 1;
    }
    if (final_qr != ""){
      show_color(pink);
      web_check_qr_code(final_qr);
      final_qr = "";
    }
  } else {
    if (analogRead(ldr) > 2000) {
      swOn = 0;
      qr_power();
      delay(500);
    }
  }
}
