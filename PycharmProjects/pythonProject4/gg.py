from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

browser = webdriver.Firefox()


def slow_type(element: WebElement, text: str):
    for character in text:
        element.send_keys(character)
        sleep(0.005)
    element.send_keys(Keys.RETURN)


ss = open('ss.txt', encoding="utf8").readlines()

q = 0
for ff in ss:
    q = q + 1
    print(q)
    browser.get('https://scholar.google.com/')

    input_user = WebDriverWait(browser, 30).until(visibility_of_element_located((By.ID, "gs_hdr_tsi")))
    slow_type(input_user, ff)
    sleep(15)

    elem = browser.find_elements(By.CLASS_NAME, 'gs_or_svg')[1]
    elem.click()
    sleep(5)
    elem = browser.find_elements(By.CLASS_NAME, 'gs_citi')[0]
    elem.click()
    html = browser.page_source
    gf = html.split('<pre>')[1].split('</pre>')[0]
    open('sa.txt', 'a').write(gf)
    print(gf)

