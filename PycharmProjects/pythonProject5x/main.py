import pyrebase
import base64
import os
from random import randrange
from threading import Thread
from time import sleep

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
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def ring_bell():
    sleep(10)
    db.child("states").child("doorBellDevice").set("0")


t2 = Thread(target=ring_bell)

while True:
    bell = str(input("Input to ring(1/0): "))

    if bell == "0":
        db.child("states").child("doorBellDevice").set("0")
    if bell == "1":
        db.child("states").child("doorBellDevice").set("1")
        # try:
        #     t2.join()
        # except RuntimeError:
        #     print("Can't")
        t2.start()

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
