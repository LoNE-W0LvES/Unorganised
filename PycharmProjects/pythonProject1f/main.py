from os.path import isfile


def read_sub(sub):
    return [i.replace('</p>', '').replace('<p ', '').split(' style="s2">') for i in open(sub, 'r', encoding="utf8").read().split('\n') if '<p begin=' in i]


def match_add(thai, english):
    new_sub = [' style="s2">'.join(['<p ' + thai[i][0], thai[i][1] + '<br />' + english[i][1] + '</p>']) for i in range(len(thai)) for j in range(len(english)) if thai[i][0] == english[j][0]]
    gg = []
    read = open('th.ttml', 'r', encoding="utf8").read().split('\n')
    sw = True
    for i in range(len(read)):
        if '<p begin=' not in read[i]:
            gg.append(read[i])
        else:
            if sw:
                gg.extend(new_sub)
                sw = False
    if not isfile('./mix.ttml'):
        open('mix.ttml', 'w+')
    open('mix.ttml', 'w', encoding="utf8").write('\n'.join(gg))


if __name__ == '__main__':
    th = read_sub('th.ttml')
    en = read_sub('en.ttml')
    match_add(thai=th, english=en)
