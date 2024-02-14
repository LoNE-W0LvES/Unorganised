import json

# some JSON:
x = '{ "TranslationUrl":"", "DiscordChannelUrl":"", "AuthorizationDiscord":""}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
y["TranslationUrl"] = 'https://sayonari.github.io/jimakuChan/main.html?textAlign=center&v_align=top&recog=th&bgcolor=#1e326b&size1=25&weight1=900&color1=#ffffff&st_color1=#000000&st_width1=6&size2=25&weight2=900&color2=#ffffff&st_color2=#000000&st_width2=6&size3=25&weight3=900&color3=#ffffff&st_color3=#000000&st_width3=6&trans=en&speech_text_font=M PLUS Rounded\ 1c&trans_text_font=M PLUS Rounded\ 1c&trans_text2_font=M PLUS Rounded\ 1c&short_pause=750&gas_key=AKfycby-_tHUirDdFwxnltGIl2JzYd4v0jrH60WbWCOEbZQvv2dA8-vUp4f9Jwb7qW-s80_ehw'

with open('url.json', 'w') as outfile:
    json.dump(y, outfile)

with open('url.json', 'r') as out:
    data = json.load(out)

print(data)