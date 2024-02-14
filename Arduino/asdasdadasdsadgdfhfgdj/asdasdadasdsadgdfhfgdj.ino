#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

const char* ssid = "wolves";
const char* password = "wanda@201cse";
const int jsonSize = 1024;

WebServer server(80);

const char* index_html = R"=====(
<!DOCTYPE html>
<html lang="en">

<head>
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
  <title>{v}</title>
  <style>  :root{ --primarycolor:#1fa3ec; }  body.invert, body.invert a, body.invert h1 { background-color:rgb(108, 108, 108); color:white; } body.invert .msg{ background-color: #282828; border-top: 1px solid #555; border-right: 1px solid #555; border-bottom: 1px solid #555; color:#fff; } body.invert .q[role=img] { -webkit-filter: invert(1); filter: invert(1); } .c, body { text-align: center; font-family: verdana } .wrap { text-align:left; display:inline-block; min-width:260px; max-width:500px; } div, input,select { padding: 5px; font-size: 1em; margin: 5px 0; box-sizing: border-box; } div{ margin: 5px 0; } input,button,select,.msg{ border-radius:.3rem; width: 100%; } input[type=radio],input[type=checkbox]{ width: auto; } button,input[type='button'],input[type='submit'] { border: 0; background-color: var(--primarycolor); color: #fff; line-height: 2.4rem; font-size: 1.2rem; } input[type='file']{ border: 1px solid var(--primarycolor); } a { color: #000; font-weight: 700; text-decoration: none; } a:hover { color: var(--primarycolor); text-decoration: underline; } .h { display: none; } .q { height: 16px; margin: 0; padding: 0 5px; text-align: right; min-width: 38px; float:right; } .q.q-0:after { background-position-x: 0; } .q.q-1:after { background-position-x: -16px; } .q.q-2:after { background-position-x: -32px; } .q.q-3:after { background-position-x: -48px; } .q.q-4:after { background-position-x: -64px; } .q.l:before { background-position-x: -80px; padding-right: 5px } .ql .q { float: left; }  .q:after, .q:before { content: '';width:16px;height:16px;display:inline-block;background-repeat:no-repeat;background-position: 16px 0; background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAQCAMAAADeZIrLAAAAJFBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADHJj5lAAAAC3RSTlMAIjN3iJmqu8zd7vF8pzcAAABsSURBVHja7Y1BCsAwCASNSVo3/v+/BUEiXnIoXkoX5jAQMxTHzK9cVSnvDxwD8bFx8PhZ9q8FmghXBhqA1faxk92PsxvRc2CCCFdhQCbRkLoAQ3q/wWUBqG35ZxtVzW4Ed6LngPyBU2CobdIDQ5oPWI5nCUwAAAAASUVORK5CYII='); } @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) { .q:before, .q:after { 	background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALwAAAAgCAMAAACfM+KhAAAALVBMVEX///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAOrOgAAAADnRSTlMAESIzRGZ3iJmqu8zd7gKjCLQAAACmSURBVHgB7dDBCoMwEEXRmKlVY3L//3NLhyzqIqSUggy8uxnhCR5Mo8xLt+14aZ7wwgsvvPA/ofv9+44334UXXngvb6XsFhO/VoC2RsSv9J7x8BnYLW+AjT56ud/uePMdb7IP8Bsc/e7h8Cfk912ghsNXWPpDC4hvN+D1560A1QPORyh84VKLjjdvfPFm++i9EWq0348XXnjhhT+4dIbCW+WjZim9AKk4UZMnnCEuAAAAAElFTkSuQmCC'); 	background-size: 95px 16px; } }  .msg { padding: 20px; margin: 20px 0; border: 1px solid #eee; border-left-width: 5px; border-left-color: #777; }  .msg h4 { margin-top: 0; margin-bottom: 5px; } .msg.P { border-left-color: var(--primarycolor); } .msg.P h4 { color: var(--primarycolor); } .msg.S { border-left-color: #5cb85c; } .msg.S h4 { color: #5cb85c; } .msg.D { border-left-color: #dc3630; } .msg.D h4 { color: #dc3630; }  dt { font-weight: bold; } dd { margin: 0; padding: 0 0 0.5em 0; } td { vertical-align: top; } button.D{ background-color:#dc3630; }  button{ transition: 0s opacity; transition-delay: 3s; transition-duration: 0s; cursor: pointer; }  button:active{ opacity: 50% !important; cursor: wait; transition-delay: 0s; }  :disabled { opacity: 0.5; } </style>

</head>

<body class="invert">
  <div class='wrap'>

    <h2>wifi</h2>
    <hr>
    <a href="javascript:void(0);" onclick="fetchWifiData();">Scan Wi-Fi Networks</a>
    <div id="wifi-list"></div>
    <form method='get' action='wifisave'>
      <label for='s'>SSID</label>
      <br />
      <input id='s' name='s' length=32 placeholder='SSID'>
      <br />
      <label for='p'>Password</label>
      <input id='p' name='p' length=64 type='password' placeholder='password'>
      <input type='checkbox' onclick='f()'> Show Password <br />
      <br /><button type='submit'>Save</button></form>
    <br />
    <form action='/wifi' method='get'><button>Refresh</button></form>
    <dl>
      <dt>IP</dt>
      <dd>192.168.4.1</dd>
    </dl>
  </div>
</body>
<script>
  function c(l) {
    document.getElementById('s').value = l.innerText || l.textContent;
    p = l.nextElementSibling.classList.contains('l');
    document.getElementById('p').disabled = !p;
    if (p) document.getElementById('p').focus()
  };

  function f() {
    var x = document.getElementById('p');
    x.type === 'password' ? x.type = 'text' : x.type = 'password';
  }

  function fetchWifiData() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/scan-wifi", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var wifiData = JSON.parse(xhr.responseText);

        var wifiList = document.getElementById("wifi-list");
        wifiList.innerHTML = "<h2>Available Wi-Fi Networks:</h2>";

        for (var i = 0; i < wifiData.length; i++) {
          var network = wifiData[i];

          var wifiItem = document.createElement("div");
          wifiItem.innerHTML =
            "<a href='#p' onclick='c(this)'>" + network.SSID + "</a>" +
            "<div role='img' class='q q-" + calculateSignalStrengthClass(network.SignalStrength) + (network.Password ? ' l' : '') + "'></div>";

          wifiList.appendChild(wifiItem);
        }
      }
    };
    xhr.send();
  }

  function calculateSignalStrengthClass(signalStrength) {
    if (signalStrength >= -50) {
      return 4;
    } else if (signalStrength >= -60) {
      return 3;
    } else if (signalStrength >= -70) {
      return 2;
    } else if (signalStrength >= -80) {
      return 1;
    } else {
      return 0;
    }
  }

  window.onload = function () {
    fetchWifiData();
  };
</script>

</html>
)=====";

void setup() {
  Serial.begin(115200);
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println(WiFi.localIP());
  // Define routes
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html", index_html);
  });

  server.on("/scan-wifi", HTTP_GET, handleScanWifi);

  // Start the server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}

void handleScanWifi() {
  DynamicJsonDocument jsonDoc(jsonSize);
  JsonArray networkArray = jsonDoc.to<JsonArray>();
  int numNetworks = WiFi.scanNetworks();
  Serial.print("network number: ");
  Serial.println(numNetworks);
  for (int i = 0; i < numNetworks; i++) {
    JsonObject network = networkArray.createNestedObject();
    network["SSID"] = WiFi.SSID(i);
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID(i));
    network["RSSI"] = WiFi.RSSI(i);
    Serial.print("RSSI: ");
    Serial.println(WiFi.RSSI(i));
    network["SignalStrength"] = WiFi.RSSI(i) + 100;
    network["Password"] = WiFi.encryptionType(i) != 0;
  }

  String jsonString;
  serializeJson(jsonDoc, jsonString);
  server.send(200, "application/json", jsonString);
}
