parts = [
    {"type": "wokwi-neopixel", "id": "rgb85", "top": -20, "left": 200, "attrs": {}},
    {"type": "wokwi-neopixel", "id": "rgb86", "top": -50, "left": 170, "attrs": {}},
    {"type": "wokwi-neopixel", "id": "rgb87", "top": -50, "left": 235, "attrs": {}},
    {"type": "wokwi-neopixel", "id": "rgb88", "top": -80, "left": 200, "attrs": {}},
    {"type": "wokwi-neopixel", "id": "rgb89", "top": -110, "left": 170, "attrs": {}},
    {"type": "wokwi-neopixel", "id": "rgb90", "top": -110, "left": 235, "attrs": {}},
    {"type": "wokwi-neopixel", "id": "rgb91", "top": -140, "left": 200, "attrs": {}}
  ]

parts_2 = []
j = 14
for i in range(len(parts)):
    j = j + 1
    gg = 'rgb' + str(int(parts[i]["id"].split('rgb')[1]) + 14)

    new_parts = { "type": "wokwi-neopixel", "id": gg, "top": parts[i]["top"], "left": int(parts[i]["left"]) + 400, "attrs": {} }
    parts_2.append(new_parts)


print(parts_2)
#
# j = 28
# for i in parts:
#     j = j + 1
#     new_parts = { "type": "wokwi-neopixel", "id": "rgb" + str(j), "top": i["top"], "left": int(i["left"]) + 600, "attrs": {} }
#     parts_2.append(new_parts)
#
# print(parts_2)
#
# j = 42
# for i in parts:
#     j = j + 1
#     new_parts = { "type": "wokwi-neopixel", "id": "rgb" + str(j), "top": i["top"], "left": int(i["left"]) + 900, "attrs": {} }
#     parts_2.append(new_parts)
#
# print(parts_2)
#
# j = 56
# for i in parts:
#     j = j + 1
#     new_parts = { "type": "wokwi-neopixel", "id": "rgb" + str(j), "top": i["top"], "left": int(i["left"]) + 1200, "attrs": {} }
#     parts_2.append(new_parts)
#
# print(parts_2)
#
# j = 70
# for i in parts:
#     j = j + 1
#     new_parts = { "type": "wokwi-neopixel", "id": "rgb" + str(j), "top": i["top"], "left": int(i["left"]) + 1500, "attrs": {} }
#     parts_2.append(new_parts)
#
# print(parts_2)