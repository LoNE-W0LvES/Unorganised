ss = open('ss.txt', encoding="utf8").readlines()

ff = []
for i in range(len(ss)):
    print(ss[i].split(')')[1])
    ff.append(ss[i].split(')')[1])


print(ff)