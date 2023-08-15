from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv



options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

chrome = webdriver.Chrome(options=options)
chrome.get("https://www.inside.com.tw/")
chrome.maximize_window()

### KeyWord Search
search_icon = chrome.find_element(By.CLASS_NAME, 'js-search_submit.search_submit.icon-search')
search_icon.click()
search = chrome.find_element(By.ID, 'search')
time.sleep(1)
search.send_keys('Musk', Keys.ENTER)

### Article List
time.sleep(2)
nums = len(chrome.find_elements(By.CLASS_NAME, 'post_list_item'))
page = 0

article_dict = {}
article_dict['title'] = []
article_dict['article'] = []


# while page != 0:
for i in range(2):
    titles = chrome.find_elements(By.CLASS_NAME, 'post_list_item')
    title = titles[i]
    t = title.find_element(By.CLASS_NAME, 'js-auto_break_title ')
    t.click()

    titlename = chrome.find_elements(By.CLASS_NAME, 'post_header_title.js-auto_break_title')[0].text
    article_dict['title'].append(titlename)

    print(titlename, '\n')
    content = chrome.find_elements(By.CLASS_NAME, 'ck-section')
    article = ""
    for cont in content:
        if "加入 INSIDE 會員" in cont.text:
            break
        print(cont.text, '\n')
        article = article + cont.text
    
    article_dict['article'].append(article)

    time.sleep(3)
    chrome.back()
    time.sleep(1)

    chrome.execute_script("window.scrollBy(0, 300);")

# chrome.find_element(By.CLASS_NAME, 'pagination_item-next-wrapper').click()
# page += 1
a = pd.DataFrame(article_dict)
csvPath = 'test.csv'
a.to_csv(csvPath, encoding='utf_8_sig')
print(pd.DataFrame(article_dict))
# soup = BeautifulSoup(chrome.page_source, 'html.parser')
# titles = soup.find_all('div', class_='post_list_item_content')
# # print(titles)


# for title in titles:
#     post = title.find('h3', class_='post_title')
#     if post:
#         print(post.getText())
#     # print(post)

