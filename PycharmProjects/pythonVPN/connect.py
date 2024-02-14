from subprocess import Popen, PIPE, call
from re import search
# cmd_x = 'netsh interface show interface | find "Connected" | find "OpenVPN TAP-Windows6"'
# cmd_x = 'netsh interface show interface | find "OpenVPN TAP-Windows6"'
# test = str(Popen('netsh interface show interface | find "OpenVPN TAP-Windows6"', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n')[0].split(' ')
# list(filter(None, str(Popen(cmd_x, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n')[0].split(' ')))[1]
# xt = list(filter(None, str(Popen('netsh interface show interface | find "OpenVPN TAP-Windows6"', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n')[0].split(' ')))
#
# print(xt)

# con_stat_arr = []
# for main in list(filter(None, str(
#     Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE, stdout=PIPE,
#           stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
#     con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main.split(' ')))))
#
# if False in con_stat_arr:
#     con_stat = 'Connected'
# else:
#     con_stat = 'Disconnected'

add_route = ''
test = list(filter(None, str(
    Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE, stdout=PIPE,
          stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n')))

for main in test:
    xt = list(filter(None, main.split(' ')))
    if xt[1] == '0.0.0.0':
        add_route = 'route add ' + xt[0] + ' mask ' + xt[1] + ' ' + xt[2]
        delete_route = 'route delete ' + xt[0] + ' mask ' + xt[1] + ' ' + xt[2]
    else:
        call('taskkill.exe /F /IM openvpn.exe', shell=True)

if add_route == '':
    Popen('wmic path win32_networkadapter where PhysicalAdapter=True call disable',
          shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    Popen('wmic path win32_networkadapter where PhysicalAdapter=True call enable',
          shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    network_rs = True

    # if xt[1] != '0.0.0.0':
    #     con_stat = 'Connected'
    # else:
    #     call('taskkill.exe /F /IM openvpn.exe', shell=True)