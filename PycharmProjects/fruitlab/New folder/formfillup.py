import urllib.request
from bs4 import BeautifulSoup
import os
from threading import Thread
import webbrowser
import time

# if os.path.isfile('url_out.txt'):
#     os.remove('url_out.txt')





if not os.path.isfile('my_info.txt'):
    open("my_info.txt", "w+")
    Email_Raw = input("Enter your Email: ")
    Name_Raw = input("Enter your Name: ")
    ID_Raw = input("Enter your ID: ")

    Email_Raw = Email_Raw.replace(' ', '+')
    Name_Raw = Name_Raw.replace(' ', '+')
    ID_Raw = ID_Raw.replace(' ', '+')
    with open("my_info.txt", "a") as input_file:
        input_file.write(Email_Raw + '\n')
        input_file.write(Name_Raw + '\n')
        input_file.write(ID_Raw + '\n')
        input_file.close()


def switch():
    while True:
        time.sleep(1)
        print('checking')
        if os.path.isfile("url_out.txt"):
            print('Found')
            time.sleep(3)
            main()


switch_thread: Thread = Thread(target=switch)
switch_thread.start()

base_url = ''
html = ''
def main():
    global base_url
    print('Starting')
    file00 = open("url_out.txt", 'r')
    count00 = 0
    st = 'docs.google.com'

    for line in file00:
        count00 += 1
        lines = line.strip()
        if st in lines:
            base_url = lines
    file00.close()

    if os.path.isfile('test2.txt'):
        os.remove('test2.txt')
    if not os.path.isfile('test2.txt'):
        open("test2.txt", "w+")
    html = ''

    def get_questions():
        global html
        global base_url
        res = urllib.request.urlopen(base_url)
        soup = BeautifulSoup(res, 'html.parser')
        html = soup.prettify()
        with open("out.txt", "w") as out:
            for i in range(0, len(html)):
                try:
                    out.write(html[i])
                except Exception:
                    1 + 1

    get_questions()

    file = open('out.txt', 'r')
    count = 0
    st = 'data-params'
    for line in file:
        count += 1
        lines = line.strip()
        if st in lines:
            n_line = lines

            main_line = n_line.replace('null', '').replace(',0,', '').replace('[', '\n').replace(',', '\n').replace(
                ']',
                '').replace(
                '"', '').replace('true', '').replace('false', '').replace(' ', '')
            with open("test3.txt", 'w+') as file7:
                main_line = main_line.lower()
                file7.write(main_line)
                file7.close()

            with open("test3.txt", 'r+') as fd:
                lines = fd.readlines()
                fd.seek(0)
                fd.writelines(line for line in lines if line.strip())
                fd.truncate()
                fd.close()

            with open("test3.txt", 'r') as file7:
                test = file7.readlines()
                file7.close()
            test = list(map(str.strip, test))

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

            index_int = index + 1
            first_test = test[index].replace('\n', '').lower()
            second_test = test[index_int].replace('\n', '')
            print(first_test)
            print(second_test)
            with open('test2.txt', 'a') as file2:
                file2.write(first_test + '\n')
                file2.write(second_test + '\n')
                file2.close()
    file.close()
    with open("test2.txt", 'r+') as fd2:
        lines = fd2.readlines()
        fd2.seek(0)
        fd2.writelines(line for line in lines if line.strip())
        fd2.truncate()
        fd2.close()

    with open("test2.txt", 'r') as file7:
        te = file7.readlines()
        file7.close()

    with open("my_info.txt", 'r') as filex:
        te2 = filex.readlines()
        filex.close()

    mail_id = te2[0].replace('\n', '')
    name = te2[1].replace('\n', '')
    roll = te2[2].replace('\n', '')
    first_url = ''
    second_url = ''
    third_url = ''

    if 'mail' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + mail_id
    if 'name' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + name
    if 'id' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + roll
    if 'roll' in te[0].replace('\n', ''):
        first_url = 'entry.' + te[1].replace('\n', '') + '=' + roll
    ################################################################################################################
    if 'mail' in te[2].replace('\n', ''):
        second_url = 'entry.' + te[3].replace('\n', '') + '=' + mail_id
    if 'name' in te[2].replace('\n', ''):
        second_url = 'entry.' + te[3].replace('\n', '') + '=' + name
    if 'id' in te[2].replace('\n', ''):
        second_url = 'entry.' + te[3].replace('\n', '') + '=' + roll
    if 'roll' in te[2].replace('\n', ''):
        first_url = 'entry.' + te[3].replace('\n', '') + '=' + roll
    ################################################################################################################
    if 'mail' in te[4].replace('\n', ''):
        third_url = 'entry.' + te[5].replace('\n', '') + '=' + mail_id
    if 'name' in te[4].replace('\n', ''):
        third_url = 'entry.' + te[5].replace('\n', '') + '=' + name
    if 'id' in te[4].replace('\n', ''):
        third_url = 'entry.' + te[5].replace('\n', '') + '=' + roll
    if 'roll' in te[4].replace('\n', ''):
        first_url = 'entry.' + te[5].replace('\n', '') + '=' + roll
    ################################################################################################################
    if os.path.isfile('out.txt'):
        os.remove('out.txt')
    if os.path.isfile('test2.txt'):
        os.remove('test2.txt')
    if os.path.isfile('test3.txt'):
        os.remove('test3.txt')
    if os.path.isfile('url_out.txt'):
        os.remove('url_out.txt')

    url_strip = base_url.replace("viewform", 'formResponse')

    new_url = url_strip + '?&' + first_url + '&' + second_url + '&' + third_url + '&submit=SUBMIT'

    print(new_url)

    webbrowser.register('chrome', None,
                        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(new_url)
