package com.lonewolves.myapplication;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

public class HistoryActivity extends AppCompatActivity {
    FirebaseDatabase firebaseDatabase;
    DatabaseReference databaseReferencePhoto;
    ImageView[] picture = new ImageView[20];
    String base64Data;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);
        Button goBackHistory = findViewById(R.id.goBackHistory);
        picture[0] = findViewById(R.id.picture1);
        picture[1] = findViewById(R.id.picture2);
        picture[2] = findViewById(R.id.picture3);
        picture[3] = findViewById(R.id.picture4);
        picture[4] = findViewById(R.id.picture5);
        picture[5] = findViewById(R.id.picture6);
        picture[6] = findViewById(R.id.picture7);
        picture[7] = findViewById(R.id.picture8);
        picture[8] = findViewById(R.id.picture9);
        picture[9] = findViewById(R.id.picture10);
        picture[10] = findViewById(R.id.picture11);
        picture[11] = findViewById(R.id.picture12);
        picture[12] = findViewById(R.id.picture13);
        picture[13] = findViewById(R.id.picture14);
        picture[14] = findViewById(R.id.picture15);
        picture[15] = findViewById(R.id.picture16);
        picture[16] = findViewById(R.id.picture17);
        picture[17] = findViewById(R.id.picture18);
        picture[18] = findViewById(R.id.picture19);
        picture[19] = findViewById(R.id.picture20);
        firebaseDatabase = FirebaseDatabase.getInstance();
        databaseReferencePhoto = firebaseDatabase.getReference("photo");
        databaseReferencePhoto.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                Object databaseValues = snapshot.getValue(Object.class);
                String value = new Gson().toJson(databaseValues);

                JSONObject jsonObj;
                try {
                    jsonObj = new JSONObject(value);
                    for (int i = 1; i < 21; i++) {
                        String fileName = "picture" + i;
                        base64Data = jsonObj.getString(fileName);

                        try {
                            byte[] bytes = Base64.decode(base64Data, Base64.DEFAULT);
                            Bitmap bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                            picture[i-1].setImageBitmap(bitmap);
                            base64Data = null;
                        } catch (IllegalArgumentException | NullPointerException e) {
                            picture[i-1].setImageResource(R.drawable.nahida_sit);
                        }
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }


            }
            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Toast.makeText(HistoryActivity.this, "Fail to get data.", Toast.LENGTH_SHORT).show();
            }
        });
        goBackHistory.setOnClickListener(view -> finish());
    }
}