package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    Button history = findViewById(R.id.goBackHistory);
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        history.setOnClickListener(view -> openFirstActivity());
    }
    public void openFirstActivity() {
        Intent intent = new Intent(this, MainActivity2.class);
        startActivity(intent);
    }
}