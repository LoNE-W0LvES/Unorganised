import asyncio
import tkinter as tk
from os.path import isfile
from threading import Thread
from pyppeteer import launch
from pystray import Icon, Menu, MenuItem
from PIL import Image
import io
import base64
import os
from subprocess import call
from pyppeteer.errors import ElementHandleError, BrowserError, NetworkError
from image import base64_icon

string_sub = " "
browser_close = 0
url_file_path = "url.txt"
if not isfile(url_file_path):
    open(url_file_path, 'w+')

original_text = 0
url = ""
url_bak = ""
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def save_url_and_exit(root):
    global url
    url_popup = UrlPopup(root)
    root.wait_window(url_popup.top)

    # Save the URL
    with open(url_file_path, "w") as file:
        file.write(url)


class GlobalOverlay:
    def __init__(self, master, translate_text=" "):
        self.master = master
        self.master.title("Global Overlay")
        self.master.attributes("-topmost", True)
        self.master.attributes("-alpha", 0.7)
        self.master.overrideredirect(True)

        self.translate_text = translate_text

        self.subtitle_label = tk.Label(self.master, text=self.translate_text, font=("Arial", 14))
        self.subtitle_label.pack(expand=True, fill=tk.BOTH)

        self.position_at_bottom_middle()
        self.update_subtitle()

    def position_at_bottom_middle(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width - self.master.winfo_reqwidth()) // 2
        y = screen_height - self.master.winfo_reqheight()

        self.master.geometry(f"+{x}+{y}")

    def update_subtitle(self):
        global string_sub
        self.set_subtitle_text(string_sub)

        self.master.after(1000, self.update_subtitle)

    def set_subtitle_text(self, new_text):
        self.translate_text = new_text
        self.subtitle_label.config(text=self.translate_text)


class UrlPopup:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Enter URL")
        self.top.attributes("-topmost", True)
        self.top.attributes("-alpha", 0.7)

        self.url_label = tk.Label(self.top, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.top, width=100)
        self.url_entry.pack()

        self.ok_button = tk.Button(self.top, text="OK", command=self.save_url_and_close)
        self.ok_button.pack()

        self.center_window()

    def center_window(self):
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()

        x = (screen_width - self.top.winfo_reqwidth()) // 2
        y = (screen_height - self.top.winfo_reqheight()) // 2

        self.top.geometry(f"+{x}+{y}")

    def save_url_and_close(self):
        global url
        url = self.url_entry.get().strip()
        with open(url_file_path, "w") as file:
            file.write(url)
        self.top.destroy()


def load_url_from_file():
    try:
        with open(url_file_path, "r") as file:
            global url
            url = file.read().strip()
            return bool(url)
    except FileNotFoundError:
        return False


def main():
    global string_sub, browser_close, url
    root = tk.Tk()
    root.overrideredirect(True)
    global_overlay = GlobalOverlay(root)

    def close():
        global browser_close
        browser_close = 1

    def update_from_function():
        global string_sub
        global_overlay.set_subtitle_text(string_sub)
        root.after(300, update_from_function)

    def show_original():
        global original_text
        original_text = 1
        print(original_text)

    def show_translate():
        global original_text
        original_text = 0
        print(original_text)

    # Ensure that base64_icon contains the actual base64-encoded image data
    image = Image.open(io.BytesIO(base64.b64decode(base64_icon.split(',')[1])))
    menu = (Menu(MenuItem('Close', lambda icon_, item: close()),
                 MenuItem('Save URL', lambda icon_, item: save_url_and_exit(root)),
                 MenuItem('Show Translate Only', lambda icon_, item: show_translate()),
                 MenuItem('Show Original Text', lambda icon_, item: show_original())))

    icon = Icon("name", image, menu=menu)

    def tray():
        icon.run()

    tray_thread = Thread(target=tray)
    tray_thread.start()

    if not load_url_from_file():
        url_popup = UrlPopup(root)
        root.wait_window(url_popup.top)
    root.after(1000, update_from_function)
    root.mainloop()


async def main_x():
    global string_sub, browser_close, url, url_bak, original_text
    chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    existing_user_data_dir = "C:\\Users\\nafim\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2"

    browser = await launch(args=['--window-size=1920,1080', '--use-fake-ui-for-media-stream', '--no-pooling'],
                           defaultViewport=None, headless=False,
                           executablePath=chrome,
                           userDataDir=existing_user_data_dir)
    page = await browser.newPage()
    while True:
        if url is not None and url.strip() != "" and url != 'https://':
            if 'https://' not in url:
                url = 'https://' + url
            try:
                await page.goto(url)
            except (ElementHandleError, BrowserError, NetworkError):
                pass
            url_bak = url
            break

    while True:
        if url != url_bak:
            if 'https://' not in url:
                url = 'https://' + url
            try:
                await page.goto(url)
            except (ElementHandleError, BrowserError, NetworkError):
                pass
            url_bak = url

        if 'sayonari.github.io/jimakuChan' in url:
            try:
                if original_text == 1:
                    text_content = await page.evaluate(
                        '(element) => element.textContent', await page.querySelector(
                            '#speech_text-fg')) + '\n' + await page.evaluate(
                        '(element) => element.textContent', await page.querySelector('#trans_text-fg'))
                else:
                    text_content = await page.evaluate(
                        '(element) => element.textContent', await page.querySelector('#trans_text-fg'))
                if string_sub != text_content:
                    string_sub = text_content
            except (ElementHandleError, BrowserError, NetworkError):
                call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
                pass
        if browser_close == 1:
            await browser.close()
            break
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)


if __name__ == "__main__":
    thread = Thread(target=main)
    thread.start()
    asyncio.run(main_x())
