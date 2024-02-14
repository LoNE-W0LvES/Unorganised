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
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
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

    ImageView photo;
    public String doorStateApp;
    public String doorStateDevice;
    public String fanStateApp;
    public String fanStateDevice;
    public String lightStateApp;
    public String lightStateDevice;
    public String base64Data;
    public String doorBellDevice;
    public String oldDoorBellDevice;

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel("Smart Door", "Smart Door", NotificationManager.IMPORTANCE_DEFAULT);
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }

        Intent intent = new Intent(this, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, "Smart Door")
                .setSmallIcon(R.drawable.notify_icon)
                .setContentTitle("Smart Door")
                .setContentText("Someone just ranged a bell")
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
                .setDefaults(Notification.DEFAULT_VIBRATE)
                .setLights(getResources().getColor(R.color.nahida), 500, 500)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true);
        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);

        Button lightSwitch = findViewById(R.id.light);
        Button fanSwitch = findViewById(R.id.fan);
        Button takePic = findViewById(R.id.takePhoto);
        Button doorSwitch = findViewById(R.id.doorState);
        photo = findViewById(R.id.picture);
        firebaseDatabase = FirebaseDatabase.getInstance();
        databaseReference = firebaseDatabase.getReference();
        databaseReference.addValueEventListener(new ValueEventListener() {
            @RequiresApi(api = Build.VERSION_CODES.S)
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                Object object = snapshot.getValue(Object.class);
                String value = new Gson().toJson(object);
                JSONObject jsonObj;

                try {
                    jsonObj = new JSONObject(value);
                    doorStateApp = jsonObj.getString("doorStateApp");
                    doorStateDevice = jsonObj.getString("doorStateDevice");
                    fanStateApp = jsonObj.getString("fanStateApp");
                    fanStateDevice = jsonObj.getString("fanStateDevice");
                    lightStateApp = jsonObj.getString("lightStateApp");
                    lightStateDevice = jsonObj.getString("lightStateDevice");
                    base64Data = jsonObj.getString("picture");
                    doorBellDevice =  jsonObj.getString("doorBellDevice");
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                if (oldDoorBellDevice == null || !oldDoorBellDevice.equals(doorBellDevice)){
                    if (oldDoorBellDevice != null) {
                        Log.i("oldDoorBellDevice", oldDoorBellDevice);
                        Log.i("doorBellDevice", doorBellDevice);
                    }
                    if (doorBellDevice.equals("1")){
                        notificationManager.notify(500, builder.build());
                    }
                    oldDoorBellDevice = doorBellDevice;
                }

                takePic.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                if (Objects.equals(doorStateDevice, "0")){
                    doorSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                } else if(Objects.equals(doorStateDevice, "1")) {
                    doorSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                }
                if (Objects.equals(lightStateDevice, "0")){
                    lightSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                } else if(Objects.equals(lightStateDevice, "1")) {
                    lightSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                }
                if (Objects.equals(fanStateDevice, "0")){
                    fanSwitch.setBackgroundColor(getResources().getColor(R.color.darkNahida));
                } else if(Objects.equals(fanStateDevice, "1")) {
                    fanSwitch.setBackgroundColor(getResources().getColor(R.color.nahida));
                }
                byte[] bytes=Base64.decode(base64Data,Base64.DEFAULT);
                Bitmap bitmap= BitmapFactory.decodeByteArray(bytes,0,bytes.length);
                photo.setImageBitmap(bitmap);

                doorSwitch.setOnClickListener(view -> {
                    if (Objects.equals(doorStateDevice, "0")){
                        databaseReference.child("doorStateApp").setValue("1");
                    } else if(Objects.equals(doorStateDevice, "1")) {
                        databaseReference.child("doorStateApp").setValue("0");
                    }
                });
                fanSwitch.setOnClickListener(view -> {
                    if (Objects.equals(fanStateDevice, "0")){
                        databaseReference.child("fanStateApp").setValue("1");
                    } else if(Objects.equals(fanStateDevice, "1")) {
                        databaseReference.child("fanStateApp").setValue("0");
                    }
                });
                lightSwitch.setOnClickListener(view -> {
                    if (Objects.equals(lightStateDevice, "0")){
                        databaseReference.child("lightStateApp").setValue("1");
                    } else if(Objects.equals(lightStateDevice, "1")) {
                        databaseReference.child("lightStateApp").setValue("0");
                    }
                });
                takePic.setOnClickListener(view -> databaseReference.child("takePhoto").setValue("1"));
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Toast.makeText(MainActivity.this, "Fail to get data.", Toast.LENGTH_SHORT).show();
            }
        });
    }
}