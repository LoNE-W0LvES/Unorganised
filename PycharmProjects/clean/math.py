



# var1 + var2 + var5 + var6 + var3 + var4 + var0 + var7
from subprocess import call, PIPE, Popen

import psutil


# def cleanup():
#     if 'openvpn.exe' in (i.name() for i in psutil.process_iter()):
#         call('taskkill.exe /F /IM openvpn.exe', shell=True)
#     if 'chrome.exe' in (i.name() for i in psutil.process_iter()):
#         call('taskkill.exe /F /IM chrome.exe', shell=True)
#     if 'node.exe' in (i.name() for i in psutil.process_iter()):
#         call('taskkill.exe /F /IM node.exe', shell=True)
#     call('wmic path win32_networkadapter where PhysicalAdapter=True call disable', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
#     call('wmic path win32_networkadapter where PhysicalAdapter=True call enable', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
#
#
# cleanup()
#  route -p add 0.0.0.0 mask 0.0.0.0 192.168.31.1.split('\\r\\n')
# 'route print | find "0.0.0.0" | findstr /vc:"On-link"'

# route print findstr /vc:"On-link"


add_route = ''
delete_route = ''
network_rs = True
while network_rs:
    network_rs = False
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
        call('wmic path win32_networkadapter where PhysicalAdapter=True call disable', shell=True, stdout=PIPE,
             stderr=PIPE)
        call('wmic path win32_networkadapter where PhysicalAdapter=True call enable', shell=True, stdout=PIPE,
             stderr=PIPE)
        network_rs = True

'route add 0.0.0.0 mask 0.0.0.0 192.168.31.1'
'route delete 0.0.0.0 mask 0.0.0.0 192.168.31.1'
'          0.0.0.0          0.0.0.0     192.168.31.1   192.168.31.237     35'
'          0.0.0.0          0.0.0.0     192.168.31.1   192.168.31.165     55'

print(add_route)
print(delete_route)
