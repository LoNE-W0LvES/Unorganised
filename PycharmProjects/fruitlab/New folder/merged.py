from telethon import TelegramClient, events
import urllib.request
from bs4 import BeautifulSoup
import os
import webbrowser

base_url = ''
html = ''
if os.path.isfile('url_out'):
    os.remove('url_out')

if not os.path.isfile('my_info') or len(open('my_info', 'r').readlines()) < 7:
    open("my_info", "w+")
    Email_Raw = input("Enter your Email (Case sensitive): ")
    Name_Raw = input("Enter your Name (Case sensitive): ")
    ID_Raw = input("Enter your ID (Case sensitive): ")
    Telegram_API_ID = input("Enter Telegram API ID (Case sensitive): ")
    Telegram_API_HASH = input("Enter Telegram API HASH (Case sensitive): ")
    Telegram_Channel_Name = input("Enter Telegram channel name (Case sensitive): ")

    Email_Raw = Email_Raw.replace(' ', '+')
    Name_Raw = Name_Raw.replace(' ', '+')
    ID_Raw = ID_Raw.replace(' ', '+')
    Telegram_API_ID = Telegram_API_ID.replace(' ', '')
    Telegram_API_HASH = Telegram_API_HASH.replace(' ', '')

    with open("my_info", "a") as input_file:
        input_file.write(Email_Raw + '\n')
        input_file.write(Name_Raw + '\n')
        input_file.write(ID_Raw + '\n')
        input_file.write(Telegram_API_ID + '\n')
        input_file.write(Telegram_API_HASH + '\n')
        input_file.write(Telegram_Channel_Name + '\n')
        input_file.close()

with open("my_info", 'r') as telegram_file:
    telegram_files = telegram_file.readlines()
    telegram_file.close()

api_id = telegram_files[3].replace('\n', '')
api_id = int(api_id)
api_hash = telegram_files[4].replace('\n', '')
Channel_name = telegram_files[5].replace('\n', '')


def main():
    print('Link found')
    global base_url
    file00 = open("url_out", 'r')
    count00 = 0
    st = 'docs.google.com'
    # -----------------------------------------------------------------------------------------------------------------#
    for line in file00:
        count00 += 1
        lines = line.strip()
        if st in lines:
            base_url = lines
    file00.close()
    # -----------------------------------------------------------------------------------------------------------------#
    if os.path.isfile('test2'):
        os.remove('test2')
    if not os.path.isfile('test2'):
        open("test2", "w+")
    html = ''

    # -----------------------------------------------------------------------------------------------------------------#
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
                except Exception:
                    1 + 1

    get_questions()
    # -----------------------------------------------------------------------------------------------------------------#
    file = open('out', 'r')
    count = 0
    st = 'data-params'
    # -----------------------------------------------------------------------------------------------------------------#
    for line in file:
        count += 1
        lines = line.strip()
        if st in lines:
            n_line = lines
            # ---------------------------------------------------------------------------------------------------------#
            main_line = n_line.replace('null', '').replace(',0,', '').replace('[', '\n').replace(',', '\n').replace(
                ']',
                '').replace(
                '"', '').replace('true', '').replace('false', '').replace(' ', '')
            # ---------------------------------------------------------------------------------------------------------#
            with open("test3", 'w+') as file7:
                main_line = main_line.lower()
                file7.write(main_line)
                file7.close()
            # ---------------------------------------------------------------------------------------------------------#
            with open("test3", 'r+') as fd:
                lines = fd.readlines()
                fd.seek(0)
                fd.writelines(line for line in lines if line.strip())
                fd.truncate()
                fd.close()
            # ---------------------------------------------------------------------------------------------------------#
            with open("test3", 'r') as file7:
                test = file7.readlines()
                file7.close()
            test = list(map(str.strip, test))
            # ---------------------------------------------------------------------------------------------------------#
            index = 2
            if 'email' in test:
                index = test.index('email')
            if 'mail' in test:
                index = test.index('mail')
            if 'name' in test:
                index = test.index('name')
            if 'id' in test:
                index = test.index('id')
            if 'roll' in test:
                index = test.index('roll')
            # ---------------------------------------------------------------------------------------------------------#
            index_int = index + 1
            first_test = test[index].replace('\n', '').lower()
            second_test = test[index_int].replace('\n', '')
            # ---------------------------------------------------------------------------------------------------------#
            with open('test2', 'a') as file2:
                file2.write(first_test + '\n')
                file2.write(second_test + '\n')
                file2.close()
    file.close()
    # -----------------------------------------------------------------------------------------------------------------#
    with open("test2", 'r+') as fd2:
        lines = fd2.readlines()
        fd2.seek(0)
        fd2.writelines(line for line in lines if line.strip())
        fd2.truncate()
        fd2.close()
    # -----------------------------------------------------------------------------------------------------------------#
    with open("test2", 'r') as file7:
        te = file7.readlines()
        file7.close()
    # -----------------------------------------------------------------------------------------------------------------#
    with open("my_info", 'r') as filex:
        te2 = filex.readlines()
        filex.close()
    # -----------------------------------------------------------------------------------------------------------------#
    mail_id = te2[0].replace('\n', '')
    name = te2[1].replace('\n', '')
    roll = te2[2].replace('\n', '')
    first_url = ''
    second_url = ''
    third_url = ''
    # -----------------------------------------------------------------------------------------------------------------#
    if 'mail' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + mail_id
    if 'name' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + name
    if 'id' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + roll
    if 'roll' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + roll
    # -----------------------------------------------------------------------------------------------------------------#
    if 'mail' in te[2].replace('\n', ''):
        second_url = 'entry.' + te[3].replace('\n', '') + '=' + mail_id
    if 'name' in te[2].replace('\n', ''):
        second_url = 'entry.' + te[3].replace('\n', '') + '=' + name
    if 'id' in te[2].replace('\n', ''):
        second_url = 'entry.' + te[3].replace('\n', '') + '=' + roll
    if 'roll' in te[2].replace('\n', ''):
        first_url = 'entry.' + te[3].replace('\n', '') + '=' + roll
    # -----------------------------------------------------------------------------------------------------------------#
    if 'mail' in te[4].replace('\n', ''):
        third_url = 'entry.' + te[5].replace('\n', '') + '=' + mail_id
    if 'name' in te[4].replace('\n', ''):
        third_url = 'entry.' + te[5].replace('\n', '') + '=' + name
    if 'id' in te[4].replace('\n', ''):
        third_url = 'entry.' + te[5].replace('\n', '') + '=' + roll
    if 'roll' in te[4].replace('\n', ''):
        first_url = 'entry.' + te[5].replace('\n', '') + '=' + roll
    # -----------------------------------------------------------------------------------------------------------------#
    if os.path.isfile('out'):
        os.remove('out')
    if os.path.isfile('test2'):
        os.remove('test2')
    if os.path.isfile('test3'):
        os.remove('test3')
    if os.path.isfile('url_out'):
        os.remove('url_out')
    # -----------------------------------------------------------------------------------------------------------------#
    url_strip = base_url.replace("viewform", 'formResponse')

    new_url = url_strip + '?&' + first_url + '&' + second_url + '&' + third_url + '&submit=SUBMIT'

    print(new_url)

    webbrowser.register('chrome', None,
                        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(new_url)
    print('Submitted.')
#######################################################################################################################


client = TelegramClient('anon', api_id, api_hash)


@client.on(events.NewMessage(chats=Channel_name))
async def my_event_handler(event):
    print('Waiting for the link . . . ')

    search = 'docs.google.com'
    if search in event.raw_text:
        with open("url_out", "w") as out0:
            out0.write(event.raw_text)
        out0.close()

        file00 = open("url_out", 'r')
        count00 = 0
        st = 'docs.google.com'

        for line in file00:
            count00 += 1
            lines = line.strip()
            if st in lines:
                with open("url_out", "w") as out01:
                    out01.write(lines)
                out01.close()
        file00.close()
        main()
        print(event.raw_text)

client.start()
client.run_until_disconnected()
