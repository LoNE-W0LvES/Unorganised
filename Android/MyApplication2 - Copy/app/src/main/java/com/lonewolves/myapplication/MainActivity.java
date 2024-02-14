package com.lonewolves.myapplication;


import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.RingtoneManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Base64;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Objects;

public class MainActivity extends AppCompatActivity {
    FirebaseDatabase firebaseDatabase;
    DatabaseReference databaseReference;
    DatabaseReference databaseReferencePhoto;
    ImageView photo;
    Button doorSwitch;
    public int doorStateApp;
    public int doorStateDevice;
    public int fanStateApp;
    public int fanSpeedValue;
    public int fanStateDevice;
    public int lightStateApp;
    public int lightStateDevice;
    public int doorBellDevice;
    public double roomTemp;
    public double roomTempFer;
//    public double heatIndexCel;
//    public double heatIndexFer;
    public int roomHum;
    public int fireAlert;
    public int pictureCount;
    public int oldDoorBellDevice = 2;
    public String base64Data;

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button history = findViewById(R.id.history);
        Button indoor = findViewById(R.id.inActivity);
        Button addUserAccess = findViewById(R.id.addAccess);
        Button lightSwitch = findViewById(R.id.light);
        Button fanSwitch = findViewById(R.id.fan);
        Button takePic = findViewById(R.id.takePhoto);
        doorSwitch = findViewById(R.id.doorState);
        SeekBar fanSpeed = findViewById(R.id.fanSpeed);
        photo = findViewById(R.id.picture);
        TextView roomTempText = findViewById(R.id.roomTemp);
        //        TextView roomTempIndexText = findViewById(R.id.roomTempIndex);
        TextView roomHumText = findViewById(R.id.roomHum);
        TextView fireAlertText = findViewById(R.id.fireAlert);
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

        firebaseDatabase = FirebaseDatabase.getInstance();
        databaseReference = firebaseDatabase.getReference("states");
        databaseReferencePhoto = firebaseDatabase.getReference("photo");
        databaseReference.addValueEventListener(new ValueEventListener() {
            @RequiresApi(api = Build.VERSION_CODES.S)
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                Object databaseValues = snapshot.getValue(Object.class);
                String value = new Gson().toJson(databaseValues);
                JSONObject jsonObj;
                try {
                    jsonObj = new JSONObject(value);
                    doorStateApp = jsonObj.getInt("doorStateApp");
                    doorStateDevice = jsonObj.getInt("doorStateDevice");
                    fanStateApp = jsonObj.getInt("fanStateApp");
                    fanStateDevice = jsonObj.getInt("fanStateDevice");
                    fanSpeedValue = jsonObj.getInt("fanSpeed");
                    lightStateApp = jsonObj.getInt("lightStateApp");
                    lightStateDevice = jsonObj.getInt("lightStateDevice");
                    doorBellDevice =  jsonObj.getInt("doorBellDevice");
                    roomTemp = jsonObj.getDouble("roomTemp");
                    roomTempFer = jsonObj.getDouble("roomTempFer");
//                    heatIndexCel = jsonObj.getDouble("roomTemp");
//                    heatIndexFer = jsonObj.getDouble("roomTempFer");
                    roomHum =  jsonObj.getInt("roomHum");
                    fireAlert =  jsonObj.getInt("fireAlert");
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                if (oldDoorBellDevice != doorBellDevice){
                    if (doorBellDevice == 1){
                        notificationManager0.notify(500, builder0.build());
                    }
                    oldDoorBellDevice = doorBellDevice;
                }
                roomHumText.setText(String.valueOf(roomHum).concat(" %"));
                roomTempText.setText(String.valueOf(roomTemp).concat(" °C (").concat(String.valueOf(roomTempFer)).concat(" °F)"));
//                roomTempIndexText.setText(String.valueOf(heatIndexCel).concat(" °C (").concat(String.valueOf(heatIndexFer)).concat(" °F)"));
                if (Objects.equals(fireAlert, 0)){
                    fireAlertText.setText(R.string.normal);
                } else if (Objects.equals(fireAlert, 1)){
                    fireAlertText.setText(R.string.fire);
                    notificationManager1.notify(500, builder1.build());
                }
                takePic.setBackgroundColor(getResources().getColor(R.color.darkNahida));
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
                databaseReferencePhoto.addValueEventListener(new ValueEventListener() {
                    @Override
                    public void onDataChange(@NonNull DataSnapshot snapshot) {
                        Object databaseValues = snapshot.getValue(Object.class);
                        String value = new Gson().toJson(databaseValues);
                        JSONObject jsonObj;

                        try {
                            jsonObj = new JSONObject(value);
                            pictureCount = jsonObj.getInt("pictureCount");
                            pictureCount = pictureCount - 1;
                            if (pictureCount < 1){
                                pictureCount = 20;
                            }
                            base64Data = jsonObj.getString("picture" + pictureCount);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        try {
                            byte[] bytes=Base64.decode(base64Data,Base64.DEFAULT);
                            Bitmap bitmap= BitmapFactory.decodeByteArray(bytes,0,bytes.length);
                            photo.setImageBitmap(bitmap);
                        } catch (IllegalArgumentException | java.lang.NullPointerException e) {
                            photo.setImageResource(R.drawable.nahida_sit);
                        }
                    }
                    @Override
                    public void onCancelled(@NonNull DatabaseError error) {
                        Toast.makeText(MainActivity.this, "Fail to get data.", Toast.LENGTH_SHORT).show();
                    }
                });

                doorSwitch.setOnClickListener(view -> {
                    if (Objects.equals(doorStateDevice, 0)){
                        Toast.makeText(getApplicationContext(),"Opening Door", Toast.LENGTH_SHORT).show();
                        databaseReference.child("doorStateApp").setValue(1);
                        databaseReference.child("dataUpdate").setValue(1);
                    } else if(Objects.equals(doorStateDevice, 1)) {
                        Toast.makeText(getApplicationContext(),"Closing Door", Toast.LENGTH_SHORT).show();
                        databaseReference.child("doorStateApp").setValue(0);
                        databaseReference.child("dataUpdate").setValue(1);
                    }
                });
                fanSwitch.setOnClickListener(view -> {
                    if (Objects.equals(fanStateDevice, 0)){
                        Toast.makeText(getApplicationContext(),"Turning On Fan", Toast.LENGTH_SHORT).show();
                        databaseReference.child("fanStateApp").setValue(1);
                        databaseReference.child("dataUpdate").setValue(1);
                    } else if(Objects.equals(fanStateDevice, 1)) {
                        Toast.makeText(getApplicationContext(),"Turning Off Fan", Toast.LENGTH_SHORT).show();
                        databaseReference.child("fanStateApp").setValue(0);
                        databaseReference.child("dataUpdate").setValue(1);
                    }
                });
                lightSwitch.setOnClickListener(view -> {
                    if (Objects.equals(lightStateDevice, 0)){
                        Toast.makeText(getApplicationContext(),"Turning On Light", Toast.LENGTH_SHORT).show();
                        databaseReference.child("lightStateApp").setValue(1);
                        databaseReference.child("dataUpdate").setValue(1);
                    } else if(Objects.equals(lightStateDevice, 1)) {
                        Toast.makeText(getApplicationContext(),"Turning Off Light", Toast.LENGTH_SHORT).show();
                        databaseReference.child("lightStateApp").setValue(0);
                        databaseReference.child("dataUpdate").setValue(1);
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
                        databaseReference.child("fanSpeed").setValue(fanSpeedValue);
                        databaseReference.child("dataUpdate").setValue(1);
                    }
                });
                takePic.setOnClickListener(view -> {
                    databaseReference.child("dataUpdate").setValue(1);
                    databaseReference.child("takePhoto").setValue(1);
                });

            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Toast.makeText(MainActivity.this, "Fail to get data.", Toast.LENGTH_SHORT).show();
            }
        });
        addUserAccess.setOnClickListener(view -> openFirstActivity());
        history.setOnClickListener(view -> openSecondActivity());
        indoor.setOnClickListener(view -> openThirdActivity());
    }
    public void openFirstActivity() {
        Intent intent = new Intent(this, camActivity.class);
        startActivity(intent);
    }
    public void openSecondActivity() {
        Intent intent = new Intent(this, HistoryActivity.class);
        startActivity(intent);
    }
    public void openThirdActivity() {
        Intent intent = new Intent(this, indoorActivity.class);
        startActivity(intent);
    }
}