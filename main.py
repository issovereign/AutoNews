# from scraper import scraper
from utils import load_csv, single_news_get_keywords
from sentence_model import SentenceProcessor
import openai

# from utils call generate by gpt
# from utils call push to web

def main():
    # scraper()
    news_dict = load_csv()
    # print(news_dict)
    
    sentence_processor = SentenceProcessor()
    keywords_every_news_list = []

    # for news in news_dict.items():
    #     print(news[0])
    #     curr_news_keywords = single_news_get_keywords(news, sentence_processor)
    #     print("curr_news_keywords: ", curr_news_keywords)
    #     keywords_every_news_list.append(curr_news_keywords)
    
    # print(keywords_every_news_list)
        
    # send first news and keywords to gpt4
    with open('sk.txt', 'r') as file:
        sk = file.read().strip()
        print(sk[:-5])

    model = "gpt-3.5-turbo"

    openai.api_key = sk
    messages = [
    {"role":"user", "content":"要怎麼發表會引起大眾關注的文章？\n請簡短回答"},
    ]

    chat_completion = openai.ChatCompletion.create(
    model=model,
    messages = messages,
    )
    print(chat_completion.choices[0].message.content)

    # let the article fit in html

if __name__ == '__main__':
    main()