import pyrebase
import base64
import os
from random import randrange
firebaseConfig = {
    "apiKey": "AIzaSyBbp2cfneMxzdOVgBfdad3jGzpK8FLy5Jg",
    "authDomain": "esp32door-f40d1.firebaseapp.com",
    "databaseURL": "https://esp32door-f40d1-default-rtdb.firebaseio.com",
    "projectId": "esp32door-f40d1",
    "storageBucket": "esp32door-f40d1.appspot.com",
    "messagingSenderId": "55722602984",
    "appId": "1:55722602984:web:06cdf4777118e7a01eb45d",
    "measurementId": "G-GLETQMWTZK"
}
oldDoorStateApp = ""
oldLightStateApp = ""
oldFanStateApp = ""
oldFanSpeed = ""
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

while True:
    doorStateApp = db.child("states").child("doorStateApp").get().val()
    fanStateApp = db.child("states").child("fanStateApp").get().val()
    fanSpeed = db.child("states").child("fanSpeed").get().val()
    lightStateApp = db.child("states").child("lightStateApp").get().val()
    takePhoto = db.child("states").child("takePhoto").get().val()

    if oldDoorStateApp != doorStateApp:
        oldDoorStateApp = doorStateApp
        if doorStateApp == "1":
            print("opening Door")
            db.child("states").child("doorStateDevice").set("1")
        if doorStateApp == "0":
            print("Closing Door")
            db.child("states").child("doorStateDevice").set("0")

    if oldLightStateApp != lightStateApp:
        oldLightStateApp = lightStateApp
        if lightStateApp == "1":
            print("Turning on Light")
            db.child("states").child("lightStateDevice").set("1")
        if lightStateApp == "0":
            print("Turning off Light")
            db.child("states").child("lightStateDevice").set("0")

    if oldFanStateApp != fanStateApp:
        oldFanStateApp = fanStateApp
        if fanStateApp == "1":
            print("Turning on fan")
            db.child("states").child("fanStateDevice").set("1")
        if fanStateApp == "0":
            print("Turning off fan")
            db.child("states").child("fanStateDevice").set("0")

    if oldFanSpeed != fanSpeed:
        oldFanSpeed = fanSpeed
        print("Fan Speed: " + fanSpeed)

    if takePhoto == "1":
        print("Taking photo")
        path = r'C:\\Users\\nafim\\PycharmProjects\\pythonProject4\\picture'
        filelist = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".jpg"):
                    filelist.append(os.path.join(root, file))

        with open(filelist[randrange(0, len(filelist))], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            gg = str(encoded_string).strip("b'").strip("'")
        db.child("photo").child("picture").set(gg)
        db.child("states").child("takePhoto").set("0")

# bellStateDevice = input()
