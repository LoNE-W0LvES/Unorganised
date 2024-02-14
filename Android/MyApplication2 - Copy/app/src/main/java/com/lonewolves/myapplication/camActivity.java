package com.lonewolves.myapplication;


import android.Manifest;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.github.dhaval2404.imagepicker.ImagePicker;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Objects;

public class camActivity extends AppCompatActivity {
    private static final int CAMERA_REQ_CODE=100;
    ImageView camImage;
    Button capture;
    Button goBack;
    Button saveDeviceIp;
//    Button saveCamIp;
    EditText deviceIP0;
    EditText deviceIP1;
    EditText deviceIP2;
    EditText deviceIP3;
    EditText cameraIp0;
    EditText cameraIp1;
    EditText cameraIp2;
    EditText cameraIp3;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cam);
        camImage = findViewById(R.id.camImage);
        capture = findViewById(R.id.capture);
        goBack = findViewById(R.id.goBack);
        saveDeviceIp = findViewById(R.id.saveIp);

        deviceIP0 = findViewById(R.id.deviceIp0);
        deviceIP1 = findViewById(R.id.deviceIp1);
        deviceIP2 = findViewById(R.id.deviceIp2);
        deviceIP3 = findViewById(R.id.deviceIp3);
        cameraIp0 = findViewById(R.id.cameraIp0);
        cameraIp1 = findViewById(R.id.cameraIp1);
        cameraIp2 = findViewById(R.id.cameraIp2);
        cameraIp3 = findViewById(R.id.cameraIp3);

        saveDeviceIp.setOnClickListener(view -> writeToFile("deviceIP.txt", "deviceIP:" + deviceIP0.getText().toString() + "." + deviceIP1.getText().toString() + "." + deviceIP2.getText().toString() + "." + deviceIP3.getText().toString() + "\n" + "camIP:" + cameraIp0.getText().toString() + "." + cameraIp1.getText().toString() + "." + cameraIp1.getText().toString() + "." + cameraIp3.getText().toString()));

        File picDir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES).toString() + "/faceRecognition");
        if (!picDir.exists())
        {
            picDir.mkdirs();
        }
        ActivityCompat.requestPermissions(camActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},1);
        ActivityCompat.requestPermissions(camActivity.this, new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},1);
        capture.setOnClickListener(view -> ImagePicker.with(camActivity.this).cameraOnly().crop(50f, 37f).compress(100).maxResultSize(400, 296).saveDir(getExternalFilesDir(Environment.DIRECTORY_PICTURES)).start());
        goBack.setOnClickListener(view -> finish());
    }
    public void writeToFile(String fileName, String content) {
        File path = getApplicationContext().getFilesDir();
        try {
            FileOutputStream writer = new FileOutputStream(new File(path, fileName));
            writer.write(content.getBytes());
            writer.close();
            Toast.makeText(getApplicationContext(), "Saved", Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        assert data != null;
        String outFileName = null;
        Uri img = data.getData();
        camImage.setImageURI(img);
        String rawPath = getExternalFilesDir(Environment.DIRECTORY_PICTURES).toString();
        String newPath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES).toString() + "/faceRecognition";
        File picFolderRaw = new File(rawPath);
        File picFolder = new File(newPath);

        File[] files0 = picFolderRaw.listFiles();
        assert files0 != null;
        for (File value : files0) {
            File[] files1 = picFolder.listFiles();
            assert files1 != null;
            for (File file : files1) {
                Log.d("Files1", "FileName:" + file.getName());
                for (int i=36; i > 0; i--){
                    String tempOutFileName = i + ".jpg";
                    if (!tempOutFileName.equals(file.getName().toLowerCase())){
                        outFileName = tempOutFileName;
                    } else {
                        break;
                    }
                }
            }
            if (outFileName == null){
                moveFile(rawPath, value.getName(), "1.jpg", newPath);
            }

            if (!Objects.equals(outFileName, "36.jpg")){
                moveFile(rawPath, value.getName(), outFileName, newPath);
            } else {
                Toast.makeText(camActivity.this, "Max number reached, please delete some images.", Toast.LENGTH_SHORT).show();
                break;
            }
        }
    }

    private void moveFile(String inputPath, String inputFile, String outFile, String outputPath) {

        InputStream in = null;
        OutputStream out = null;
        try {

            //create output directory if it doesn't exist
            File dir = new File (outputPath);
            if (!dir.exists())
            {
                dir.mkdirs();
            }

            in = new FileInputStream(inputPath + "/" + inputFile);
            out = new FileOutputStream(outputPath + "/" + outFile);

            byte[] buffer = new byte[1024];
            int read;
            while ((read = in.read(buffer)) != -1) {
                out.write(buffer, 0, read);
            }
            in.close();
            in = null;

            // write the output file
            out.flush();
            out.close();
            out = null;

            // delete the original file
            new File(inputPath + "/" + inputFile).delete();


        }

        catch (FileNotFoundException fnfe1) {
            Log.e("tag", fnfe1.getMessage());
        }
        catch (Exception e) {
            Log.e("tag", e.getMessage());
        }

    }
}




