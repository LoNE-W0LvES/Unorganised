# gg = open('gg.txt', 'r').read().split('\n')
# kk = []
#
# for i in gg:
#     ff, hh = i.split('GMT')[1].split(')')[0].split(':')
#     ii = int(ff) + int(hh)/60
#     # print(ff)
#     print(ii)
#     jj = i.replace("Custom", str(ii))
#     kk.append(jj)
#
# open('ws.txt', 'w').write('\n'.join(kk))

n = 2%2

print(n)