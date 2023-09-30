# from scraper import scraper
from utils import load_csv, single_news_get_keywords
from sentence_model import SentenceProcessor

# from utils call generate by gpt
# from utils call push to web

def main():
    # scraper()
    news_dict = load_csv()
    # print(news_dict)
    
    sentence_processor = SentenceProcessor()
    keywords_every_news_list = []

    for news in news_dict.items():
        print(news[0])
        curr_news_keywords = single_news_get_keywords(news, sentence_processor)
        print("curr_news_keywords: ", curr_news_keywords)
        keywords_every_news_list.append(curr_news_keywords)
    
    print(keywords_every_news_list)
        
    # send first news and keywords to gpt4


if __name__ == '__main__':
    main()