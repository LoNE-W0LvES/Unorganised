from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import PyPDF2
import requests
import io
from os.path import isfile

if not isfile('./The Wolf Bride.txt'):
    open('The Wolf Bride.txt', 'w+')


xx = BeautifulSoup(''.join(str(BeautifulSoup(urlopen(Request('https://talenovel.com/the-wolfs-bride-novel-pdfs-download-read-online/')), features="html.parser")).split('<div class="wp-block-file">')[1:]).split('<div class="clear"></div>')[0], features="html.parser")
links = [link.get('href') for link in xx.findAll('a') if link.get('href')]
l_c = []
for li in links:
    if li not in l_c:
        l_c.append(li)
print(l_c)
print(len(l_c))
zx = 0

for n in links:
    url = n
    zx += 1
    print(zx)
    response = requests.get(url)
    f = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(f)
    pages = reader.pages
    # get all pages data
    text = "\n".join([page.extract_text() for page in pages])
    open('The Wolf Bride.txt', 'a', encoding="utf-8").write(text + '\n')


