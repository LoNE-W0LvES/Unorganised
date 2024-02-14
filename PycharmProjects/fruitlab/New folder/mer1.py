from telethon import TelegramClient, events
import urllib.request
from bs4 import BeautifulSoup
import os
import webbrowser

base_url = ''
html = ''


def get_questions():
    global html
    global base_url
    res = urllib.request.urlopen(base_url)

    soup = BeautifulSoup(res, 'html.parser')
    html = soup.prettify()
    with open("out", "w") as out:
        for i in range(0, len(html)):
            try:
                out.write(html[i])
            except ValueError:
                1 + 1


get_questions()
