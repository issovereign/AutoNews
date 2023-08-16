from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

url = "https://www.inside.com.tw/"
options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
driver.get(url)
driver.maximize_window()

def setKeyword(keyword):
    ### KeyWord Search
    search_icon = driver.find_element(By.CLASS_NAME, 'js-search_submit.search_submit.icon-search')
    search_icon.click()
    search = driver.find_element(By.ID, 'search')
    time.sleep(1)
    search.send_keys(f'{keyword}', Keys.ENTER)
    time.sleep(2)
    
def ReadArticle(driver, page=10):
    ### Search Result List

    article_dict = {}
    article_dict['title'] = []
    article_dict['article'] = []

    while page:
        nums = len(driver.find_elements(By.CLASS_NAME, 'post_list_item'))
        for i in range(nums):
            titles = driver.find_elements(By.CLASS_NAME, 'post_list_item')
            title = titles[i]
            t = title.find_element(By.CLASS_NAME, 'js-auto_break_title ')
            t.click()

            titlename = driver.find_elements(By.CLASS_NAME, 'post_header_title.js-auto_break_title')[0].text
            article_dict['title'].append(titlename)

            print(titlename, '\n')
            content = driver.find_elements(By.CLASS_NAME, 'ck-section')
            article = ""
            for cont in content:
                if "加入 INSIDE 會員" in cont.text or "責任編輯" in cont.text or "核稿編輯" in cont.text:
                    break
                print(cont.text, '\n')
                article = article + cont.text
            
            article_dict['article'].append(article)

            time.sleep(5)
            driver.back()
            time.sleep(1)

            driver.execute_script("window.scrollBy(0, 300);")

        driver.find_element(By.CLASS_NAME, 'pagination_item-next-wrapper').click()
        page -= 1
        time.sleep(3)
    
    return article_dict

def CreateCSV(csvPath, article_dict):
    print("Save CSV...")
    a = pd.DataFrame(article_dict) 
    a.to_csv(csvPath, encoding='utf_8_sig')
    print("Complete!")

if __name__ == '__main__':
    keyword = "Musk"
    maxPage = 2
    csvPath = 'test.csv'

    setKeyword(keyword=keyword)
    article_dict = ReadArticle(driver=driver, page=maxPage)
    CreateCSV(csvPath=csvPath, article_dict=article_dict)