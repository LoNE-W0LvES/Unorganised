from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import getpass
import time
import sys
import random


class FBPost:

    fb = open('./auth.txt', 'r').readlines()
    email_ = fb[0].strip().replace('\n', '')
    pass_ = fb[1].strip().replace('\n', '')

    def setup(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--window-size=1036, 674')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })

        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        self.driver.get('https://www.facebook.com/')

        time.sleep(2)
        email = self.driver.find_element_by_id('email')
        email.send_keys(self.email_)

        time.sleep(2)
        password = self.driver.find_element_by_id('pass')
        password.send_keys(self.pass_)

        time.sleep(2)
        submit_button = self.driver.find_element_by_name('login')
        submit_button.click()
        time.sleep(2)
        # page_name = 'your page name'
        # self.driver.get('https://www.facebook.com/' + page_name)

    def post_on_facebook(self, group_x):

        print('Posting  on Facebook group: ', group_x)

        time.sleep(4)
        self.driver.get(group_x)
        time.sleep(2)

        text_to_post = 'The content to post goes here'

        try:
            post_class = 'oajrlxb2 b3i9ofy5 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x cxgpxx05 d1544ag0 sj5x9vvc tw6a2znq i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l bp9cbjyn orhb3f3m czkt41v7 fmqxjp7s emzo65vh btwxx1t3 buofh1pr idiwt2bm jifvfom9 kbf60n1y'
            post_class = post_class.replace(' ', '.')
            click_post = self.driver.find_element_by_class_name(post_class)
            click_post.click()
            time.sleep(5)

            post_content = self.driver.find_element_by_class_name('notranslate._5rpu')
            post_content.send_keys(text_to_post)
            time.sleep(5)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            all_pc = soup.find_all('div', attrs={'id': re.compile("^mount_0_0_")})
            id_ = str(all_pc[0].get('id'))
            xpath = '//*[@id="' + id_ + '"]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div[1]/div'
            post = self.driver.find_element_by_xpath(xpath)
            post.click()
            time.sleep(5)

        except:

            print("Something went wrong, exiting script to avoid conflicts")
            sys.exit()

    def close_browser(self):
        self.driver.close()


fb = FBPost()
fb.setup()


page_urls = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
for group_url in page_urls:
    fb.post_on_facebook(group_url)
fb.close_browser()
