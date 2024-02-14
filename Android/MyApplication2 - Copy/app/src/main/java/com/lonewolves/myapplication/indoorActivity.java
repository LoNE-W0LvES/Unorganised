package com.lonewolves.myapplication;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.media.RingtoneManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Objects;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class indoorActivity extends AppCompatActivity {
    ImageView photo;
    Button doorSwitch;
    Button lightSwitch;
    Button fanSwitch;
    Button takePic;
    TextView roomTempText;
    TextView roomHumText;
    TextView fireAlertText;
    SeekBar fanSpeed;

    public int doorStateApp;
    public int doorStateDevice;
    public int fanStateApp;
    public int fanSpeedValue;
    public int fanStateDevice;
    public int lightStateApp;
    public int lightStateDevice;
    public int oldDoorStateDevice;
    public int doorBellDevice;
    public double roomTemp;
    public double roomTempFer;
    public double roomHum;
    public int fireAlert;
    public int pictureCount;
    public int oldDoorBellDevice = 2;
    public String bothIP;
    public String devIP;
    public String camIP;
    public String base64Data;
    OkHttpClient okHttpClient = new OkHttpClient.Builder().build();
    public String readFromFile(String fileName) {
        File path = getApplicationContext().getFilesDir();
        File readFrom = new File(path, fileName);
        byte[] content = new byte[(int) readFrom.length()];
        try {
            FileInputStream stream = new FileInputStream(readFrom);
            stream.read(content);
            return new String(content);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    NotificationManagerCompat notificationManager0;
    NotificationCompat.Builder builder0;
    NotificationManagerCompat notificationManager1;
    NotificationCompat.Builder builder1;
    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_indoor);
        lightSwitch = findViewById(R.id.light);
        fanSwitch = findViewById(R.id.fan);
        takePic = findViewById(R.id.takePhoto);
        doorSwitch = findViewById(R.id.doorState);
        fanSpeed = findViewById(R.id.fanSpeed);
        photo = findViewById(R.id.picture);
        roomTempText = findViewById(R.id.roomTemp);
        roomHumText = findViewById(R.id.roomHum);
        fireAlertText = findViewById(R.id.fireAlert);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel("Smart Door", "Smart Door", NotificationManager.IMPORTANCE_DEFAULT);
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }

        Intent intent = new Intent(this, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE);

        NotificationCompat.Builder builder0 = new NotificationCompat.Builder(this, "Smart Door")
                .setSmallIcon(R.drawable.notify_icon)
                .setContentTitle("Smart Door")
                .setContentText("Someone just ranged a bell")
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
                .setDefaults(Notification.DEFAULT_VIBRATE)
                .setLights(getResources().getColor(R.color.nahida), 500, 500)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true);
        NotificationManagerCompat notificationManager0 = NotificationManagerCompat.from(this);

        NotificationCompat.Builder builder1 = new NotificationCompat.Builder(this, "Smart Door")
                .setSmallIcon(R.drawable.notify_icon)
                .setContentTitle("Smart Door")
                .setContentText("There is fire in the room!!")
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
                .setDefaults(Notification.DEFAULT_VIBRATE)
                .setLights(getResources().getColor(R.color.nahida), 500, 500)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true);
        NotificationManagerCompat notificationManager1 = NotificationManagerCompat.from(this);

        try {
            bothIP = readFromFile("deviceIP.txt");
        } catch (RuntimeException e) {
            bothIP = "0.0.0.0\n0.0.0.0";
        }

//        devIP = "http://" + bothIP.split("\n")[0];
        devIP = "http://192.168.3.5";
        camIP = "http://" + bothIP.split("\n")[1];
//        url = "http://192.168.3.4/doorUnlock";

        final Handler handler = new Handler();
        final int delay = 1000; // 1000 milliseconds == 1 second

        handler.postDelayed(new Runnable() {
            public void run() {
                openUrl(devIP + "/cheakDevice");
                handler.postDelayed(this, delay);
            }
        }, delay);
        if (oldDoorBellDevice != doorBellDevice){
            if (doorBellDevice == 1){
                notificationManager0.notify(500, builder0.build());
            }
            oldDoorBellDevice = doorBellDevice;
        }
        roomHumText.setText(String.valueOf(roomHum).concat(" %"));
        roomTempText.setText(String.valueOf(roomTemp).concat(" °C (").concat(String.valueOf(roomTempFer)).concat(" °F)"));
        if (Objects.equals(fireAlert, 0)){
            fireAlertText.setText(R.string.normal);
        } else if (Objects.equals(fireAlert, 1)){
            fireAlertText.setText(R.string.fire);
            notificationManager1.notify(500, builder1.build());
        }
        takePic.setBackgroundColor(getResources().getColor(R.color.darkNahida));
        if (Objects.equals(doorStateDevice, 0)) {
            doorSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
        } else if (Objects.equals(doorStateDevice, 1)) {
            doorSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
        }
        if (Objects.equals(lightStateDevice, 0)) {
            lightSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
        } else if (Objects.equals(lightStateDevice, 1)) {
            lightSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
        }
        if (Objects.equals(fanStateDevice, 0)) {
            fanSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
        } else if (Objects.equals(fanStateDevice, 1)) {
            fanSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
        }

        doorSwitch.setOnClickListener(view -> {
            if(doorStateDevice == 0) {
                Toast.makeText(getApplicationContext(),"Opening Door", Toast.LENGTH_SHORT).show();
                openUrl(devIP + "/doorUnlock");
            } else if (doorStateDevice == 1) {
                Toast.makeText(getApplicationContext(),"Closing Door", Toast.LENGTH_SHORT).show();
                openUrl(devIP + "/doorLock");
            }
        });
        fanSwitch.setOnClickListener(view -> {
            if (Objects.equals(fanStateDevice, 0)){
                Toast.makeText(getApplicationContext(),"Turning On Fan", Toast.LENGTH_SHORT).show();
                openUrl(devIP + "/fanOn");
            } else if(Objects.equals(fanStateDevice, 1)) {
                Toast.makeText(getApplicationContext(),"Turning Off Fan", Toast.LENGTH_SHORT).show();
                openUrl(devIP + "/fanOff");
            }
        });
        lightSwitch.setOnClickListener(view -> {
            if (Objects.equals(lightStateDevice, 0)){
                Toast.makeText(getApplicationContext(),"Turning On Light", Toast.LENGTH_SHORT).show();
                openUrl(devIP + "/lightOn");
            } else if(Objects.equals(lightStateDevice, 1)) {
                Toast.makeText(getApplicationContext(),"Turning Off Light", Toast.LENGTH_SHORT).show();
                openUrl(devIP + "/lightOff");
            }
        });

        fanSpeed.setProgress(fanSpeedValue);

        fanSpeed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                fanSpeedValue = progress;
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                Toast.makeText(getApplicationContext(),"Fan Speed: " + (fanSpeedValue*100)/255, Toast.LENGTH_SHORT).show();
                openUrl(devIP + "/fanSpeed?value=" + fanSpeedValue);
            }
        });
    }


    void openUrl(String url) {

        try {
            run(url);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    void run(String url) throws IOException {

        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(url)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                call.cancel();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {

                final String myResponse = response.body().string();

                indoorActivity.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        if (Objects.equals(url, devIP + "/cheakDevice")){
                            String[] response = myResponse.split("-");
                            try {
                                lightStateDevice = Integer.parseInt(response[1]);
                                fanStateDevice = Integer.parseInt(response[2]);
                                doorStateDevice = Integer.parseInt(response[3]);
                                fanSpeedValue = Integer.parseInt(response[4]);
                                roomTemp = Double.parseDouble(response[5]);
                                roomTempFer = Double.parseDouble(response[6]);
                                roomHum = Double.parseDouble(response[7]);;
                                fireAlert = Integer.parseInt(response[8]);
                                doorBellDevice = Integer.parseInt(response[9]);
                            } catch (ArrayIndexOutOfBoundsException e) {
                                lightStateDevice = 0;
                                fanStateDevice = 0;
                                doorStateDevice = 0;
                                fanSpeedValue = 0;
                            }
                            fanSpeed.setProgress(fanSpeedValue);
                            roomHumText.setText(String.valueOf(roomHum).concat(" %"));
                            roomTempText.setText(String.valueOf(roomTemp).concat(" °C (").concat(String.valueOf(roomTempFer)).concat(" °F)"));
                            if (Objects.equals(fireAlert, 0)){
                                fireAlertText.setText(R.string.normal);
                            } else if (Objects.equals(fireAlert, 1)){
                                fireAlertText.setText(R.string.fire);
                            }
                            if (Objects.equals(doorStateDevice, 0)){
                                doorSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                            } else if(Objects.equals(doorStateDevice, 1)) {
                                doorSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                            }
                            if (Objects.equals(lightStateDevice, 0)){
                                lightSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                            } else if(Objects.equals(lightStateDevice, 1)) {
                                lightSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                            }
                            if (Objects.equals(fanStateDevice, 0)){
                                fanSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                            } else if(Objects.equals(fanStateDevice, 1)) {
                                fanSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                            }
                            Log.i("gg", myResponse);
                        }
                        if (Objects.equals(myResponse, "door Unlock")){
                            doorSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                            doorStateDevice = 1;
                        } else if(Objects.equals(myResponse, "door Lock")) {
                            doorSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                            doorStateDevice = 0;
                        }
                        if (Objects.equals(myResponse, "light On")){
                            lightSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                            lightStateDevice = 1;
                        } else if(Objects.equals(myResponse, "light Off")) {
                            lightSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                            lightStateDevice = 0;
                        }
                        if (Objects.equals(myResponse, "fan On")){
                            fanSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                            fanStateDevice = 1;
                        } else if(Objects.equals(myResponse, "fan Off")) {
                            fanSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                            fanStateDevice = 0;
                        }
                        if (myResponse.contains("fanSpeed")){
                            fanSpeedValue = Integer.parseInt(myResponse.split("-")[1]);
                        }
                    }
                });

            }
        });
    }
}