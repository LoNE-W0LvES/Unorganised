import urllib.request
from bs4 import BeautifulSoup
import os
from threading import Thread
import webbrowser

main_switch = False

if os.path.isfile('out.txt'):
    os.remove('out.txt')

base_url = ''
html = ''


def switch():
    global main_switch
    while True:
        if os.path.isfile('out.txt'):
            main_switch = True
        if not os.path.isfile('out.txt'):
            main_switch = False

switch_thread: Thread = Thread(target=switch)
switch_thread.start()


def main():
    while main_switch:
        base_url00 = ''
        file00 = open('out.txt', 'r')
        count00 = 0

        st = 'docs.google.com'

        for line in file00:
            count00 += 1
            lines = line.strip()
            if st in lines:
                base_url00 = lines
        file00.close()

        base_url = base_url00

        if os.path.isfile('test2.txt'):
            os.remove('test2.txt')
        if not os.path.isfile('test2.txt'):
            open("test2.txt", "w+")
        html = ''

        def get_questions():
            global html
            global base_url
            print(base_url)
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
        n_line = ''
        st = 'data-params'
        for line in file:
            count += 1
            lines = line.strip()
            if st in lines:
                n_line = lines

                main_line = n_line.replace('null', '').replace(',0,', '').replace('[', '\n').replace(',', '\n').replace(
                    ']',
                    '').replace(
                    '"', '').replace('true', '').replace('false', '')
                with open("test3.txt", 'w+') as file7:
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

                index = ''
                if 'Email\n' in test:
                    index = test.index('Email\n')
                if 'Name\n' in test:
                    index = test.index('Name\n')
                if 'ID\n' in test:
                    index = test.index('ID\n')

                index_int = index + 1
                first_test = test[index].replace('\n', '')
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

        with open("myfile.txt", 'r') as filex:
            te2 = filex.readlines()
            filex.close()

        mail_id = te2[0].replace('\n', '')
        name = te2[1].replace('\n', '')
        roll = te2[2].replace('\n', '')
        first_url = ''
        second_url = ''
        third_url = ''

        if te[0].replace('\n', '') == 'Email':
            first_url = 'entry.' + te[1].replace('\n', '') + '=' + mail_id
            print(first_url)
        if te[0].replace('\n', '') == 'Name':
            first_url = 'entry.' + te[1].replace('\n', '') + '=' + name
            print(first_url)
        if te[0].replace('\n', '') == 'ID':
            first_url = 'entry.' + te[1].replace('\n', '') + '=' + roll
            print(first_url)
        ################################################################################################################
        if te[2].replace('\n', '') == 'Email':
            second_url = 'entry.' + te[3].replace('\n', '') + '=' + mail_id
        if te[2].replace('\n', '') == 'Name':
            second_url = 'entry.' + te[3].replace('\n', '') + '=' + name
        if te[2].replace('\n', '') == 'ID':
            second_url = 'entry.' + te[3].replace('\n', '') + '=' + roll
        ################################################################################################################
        if te[4].replace('\n', '') == 'Email':
            third_url = 'entry.' + te[5].replace('\n', '') + '=' + mail_id
        if te[4].replace('\n', '') == 'Name':
            third_url = 'entry.' + te[5].replace('\n', '') + '=' + name
        if te[4].replace('\n', '') == 'ID':
            third_url = 'entry.' + te[5].replace('\n', '') + '=' + roll
        ################################################################################################################
        if os.path.isfile('out.txt'):
            os.remove('out.txt')

        new_url = base_url + '?usp=pp_url&' + first_url + '&' + second_url + '&' + third_url

        print(new_url)

        webbrowser.register('chrome', None,
                            webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open(new_url)


main_thread: Thread = Thread(target=main)
main_thread.start()

