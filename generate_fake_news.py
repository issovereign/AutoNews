from scraper import scraper
from utils import load_csv, single_news_get_keywords, gen_article_by_gpt
from sentence_model import SentenceProcessor


def generate_fake_news(api_key, keyword="", model="gpt-4o"):
    # need to edit scraper() to eat argument from web
    # scraper()
    news_dict = load_csv()
    # print(news_dict)
    
    # sentence_processor = SentenceProcessor()
    # keywords_every_news_list = []

    # for news in news_dict.items():
    #     print(news[0])
    #     curr_news_keywords = single_news_get_keywords(news, sentence_processor)
    #     print("curr_news_keywords: ", curr_news_keywords)
    #     keywords_every_news_list.append(curr_news_keywords)
    
    # if you don't want to wait for extracting keywords actions above, here is a keywords list for you to test 
    keywords_every_news_list = [['倪協理', '薪資單', '夏倪協理', '時長'], ['00 PM\n'], ['6 Plus'], 
                                ['Apple', ' Watch', '就是', '的', 'Bloomberg', '小', ' Series', ' Ultra', '錶殼', '為了', '了', '做足', 'Phone', ' Mark', ' X ', ' iPhone', ' X', '像是', '但', 'Gurman', 'Watch', '嗎', 'LED ', 'Series', ' Apple'], 
                                ['效益', '內容'], [' M2 ', ' GPU ', '是', '的', ' Max', ' M2', '小', 'M2 ', ' CPU ', '了', ' iMac', 'M3 ', 'Book', 'Phone', ' Mac ', ' Air', ' M3 ', ' Mark', 'GB ', ' CPU', ' Mac', ' M3', 'Pro', ' iPhone', ' N4', 'Air', 'Mac', 'Gurman', 'Watch', ' Macbook', 'Max ', ' Studio', ' Apple', ' GPU', 'P ', ' A17', '而', ' Pro'], 
                                ['買單', '而言', '地位', '周一'], ['多頭', 'UBS) ', 'EV)'], [' 3C ', 'Apple', 'Gadget', 'iPhone', '的', 'Tendency', '應對', 'John', '該', ' iPhone', ' Apple ', ' IP68', 'Ternus', 'INSIDE '], 
                                ['亮點', '同比', '第二季'], ['Play', 'AR ', 'USD ', ' Standards', 'Meta ', ' VR', ' Joint', ' Mac ', ' Metaverse', '它', ' Maya', ' Games', 'DAE ', 'OBJ', ' Pro ', 'Google ', 'Apple', 'Forum', ' Vision', 'HTC ', 'Epic', '的', 'FBX', ' iPad', ' Maxon', ' Linux ', '了', '該', 'App', '至關', ' Google', 'Autodesk', ' Open', ' Meta ', 'USD', 'Sony', 
                                ' WWDC ', ' Pixar', '而', 'Adobe', 'Adobe ', ' Nvidia ', '被', ' Foundation', 'Open', ' USD', ' NVIDIA ', 'XR ', ' App ', ' AOUSD', ' Autodesk', 'Quest', ' Substance', ' 但', 'Nvidia', 'JDF', 'iPhone', ' XR ', ' USD ', 'Android', 'The', ' MR ', 'Vision', ' Development', ' Vison', 'Pro', 'Alliance', ' Store', ' Meta', ' O', 'Station', ' Apple', ' Pro', ' 3D '], 
                                ['他行', '轉存', '繼續', '消金', '無縫', '高利息', '運通', '活存', '不合'], ['待在'], ['的', 'X ', '更新', ' App Store', 'X', 'Corp', '了', 'Connect', 'Elon', ' Paypal ', 'App', ' Twitter', ' Musk', '月', ' X ', '而言', ' X', ' Store', '但', ' App', ' Bon', 'Blaze', 'Jovi', '為'], 
                                ['有些', 'Apple', '的', 'Collection', '了', '該', '它', ' iPhone', '但', ' Apple']]
    
    print(keywords_every_news_list)

    keywords_str_list = ["\n".join(keywords) for keywords in keywords_every_news_list]
    keywords_str = "\n".join(keywords_str_list)
    
    # send first news and all keywords to gpt
    fake_news = gen_article_by_gpt(news_dict, keywords_str, model, api_key)

    return fake_news

if __name__ == '__main__':
    with open('sk.txt', 'r') as file:
        sk = file.read().strip()
    generate_fake_news(sk)