# gg = open('stuff.json', 'r').read()

import json
import os


# def write_json(filename, json_data):
  # print(open(filename).read())
  # if os.path.exists(filename) and open(filename).read() is None:
  #     with open(filename) as fx:
  #         obj = json.load(fx)
  #     obj.append(json_data)
  # else:
  #   obj = json_data
  # with open(filename, "w+") as of:
  #   json.dump(obj, of)


# Opening JSON file
# f = open('stuff.json')
# data = json.load(f)
data = {
  "id": "34111111344",
  "Name": "MD Nafiur Rahman",
  "phone": "011111111",
  "Email": "nafimnr00@gmail.com",
  "password": "aaaaaaaa",
  "address": "Jashore"
}

# write_json('customer.json', data)

# Iterating through the json
# list
# for i in data:
#     if i['id'] == '342545623423442':
#         print(i['password'])
# for i in data['stuff']:
#     for j in i['342545623423442']:
#         print(j)

# Closing file