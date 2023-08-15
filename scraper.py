from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd



options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

chrome = webdriver.Chrome(options=options)
chrome.get("https://www.inside.com.tw/")

# time.sleep(3)
search_icon = chrome.find_element(By.CLASS_NAME, 'js-search_submit.search_submit.icon-search')
search_icon.click()
search = chrome.find_element(By.ID, 'search')
time.sleep(1)
search.send_keys('Musk', Keys.ENTER)


titles = chrome.find_elements(By.CLASS_NAME, 'post_title')

title = titles[0]
title.click()

titlename = chrome.find_element(By.CLASS_NAME, 'post_header_title.js-auto_break_title').text
print(titlename, '\n')
content = chrome.find_elements(By.CLASS_NAME, 'ck-section')
for cont in content:
    print(cont.text, '\n')

# soup = BeautifulSoup(chrome.page_source, 'html.parser')
# titles = soup.find_all('div', class_='post_list_item_content')
# # print(titles)


# for title in titles:
#     post = title.find('h3', class_='post_title')
#     if post:
#         print(post.getText())
#     # print(post)

