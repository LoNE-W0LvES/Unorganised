# t = ["<divclass=m2data-params='%.@.\n", '389415461\n', 'email\n', '242657979\n', 'i1\n', 'i2\n', 'i3\n', "'jsmodel=cp1ow>"]
# test = list(map(str.strip,t))
# print(testtt)

# if not os.path.isfile('./Essentials/taskkill.txt'):
#     open("./Essentials/taskkill.txt", "w+")
# with open("./Essentials/taskkill.txt", 'r+') as fd:
#     lines = fd.readlines()
#     fd.seek(0)
#     fd.writelines(line for line in lines if line.strip())
#     fd.truncate()
#     fd.close()
#     array2.clear()
#     for x in open("./Essentials/taskkill.txt").readlines():
#         array2.append(x.replace("\n", ""))
# window["-APP-LIST-"].Update(array2)

# with open("file.txt") as f:
# clean = "".join(line for line in open("./Essentials/taskkill.txt") if not line.isspace())
# p = open("./Essentials/taskkilel.txt", 'r').readlines()
# print(p)
import base64
import csv
import ntpath
from io import StringIO
from urllib import parse

import pandas as pd
import requests
from github import Github

g = Github("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")
# header = {"Authorization": "token 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",
#           "Accept": "application/vnd.github.v4.raw"}
# url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/vpn-ip.csv'
# vpn_ip_response = requests.get(url, headers=header)
# tg = StringIO(vpn_ip_response.text)
#
# print(vpn_ip_response.text)

# vpn_raw = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
#     parse.quote('servers.csv'), ref="main").content).decode("utf-8").split('\r') if i]

# te = open('./Essentials/servers.csv').readlines()
# print(te[0].replace('\n', ' ').split(','))

# tx = base64.b64decode((g.get_user().get_repo('essential')).get_contents(parse.quote('servers.csv'), ref="main").content).decode("utf-8").replace('\r', '')
# print(tx)
# tx2 = tx.split('\n')
# print((tx.split('\n'))[0].split(','))

# data_1 = pd.read_csv(StringIO(tx), usecols=['Albania']).T.values.tolist()[0]
# array = [x for x in data_1 if not pd.isnull(x)]
# print(array)
# vpn_raw1 = base64.b64decode((g.get_user().get_repo('essential')).get_contents(parse.quote('vpn-raw.ovpn'), ref="main").content).decode("utf-8").split('\r')
# print(vpn_raw1)
# vpn_raw2 = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
#     parse.quote('vpn-raw.ovpn'), ref="main").content).decode("utf-8").split('\r') if i]
# print(open('./Essentials/theme.txt', 'r').readline().strip().replace('\n', ''))

array2 = open("./Essentials/taskkill.txt").readlines()

test = [i.replace('\n', '') for i in array2]
print(test)

App_name = ntpath.basename("C:\\Users\\WoLvES\\Documents\\GitHub\\essential\\servers.csv")
print(App_name)
