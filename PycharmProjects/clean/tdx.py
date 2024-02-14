import sys
import base64
import pyperclip as c

file_paths = sys.argv[1:]
for p in file_paths:
    with open(p, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
c.copy(str(encoded_string))