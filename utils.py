import csv
import string
import openai


punctuation_set = set(string.punctuation)
punctuation_set.update(['。', '》', '《', '「', '」', '（', '）', '，', '？', '！', '；', '：', '—', '、'])
    
def load_csv(file_path="scraper.csv"):
    news_dict = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            news_dict[row['title']] = row['article']
    
    return news_dict

def normalize(lst):
    min_val = min(lst)
    max_val = max(lst)
    return [(x - min_val) / (max_val - min_val) for x in lst]

def single_news_get_keywords(news, sentence_processor, threshold=0.96):
    
    title, article = news
    
    # get title's and article's words
    news_words = sentence_processor.word_segmenter([title + article], use_delim=True)[0]
    news_words_seted = list(set(news_words))
    news_words_final = []
    for w in news_words_seted:
        if w not in punctuation_set:
            news_words_final.append(w)

    # print("news_words:", news_words_seted)

    # get all news words' tokens and embeddings
    news_tokens = []
    for word in news_words_final:
        news_tokens.append(sentence_processor.sentences2tokens(word))
    # print(len(news_tokens))

    news_tokens_embeddings = [sentence_processor.tokens2embeddings(token) for token in news_tokens]
    # print("news embeddings: ", news_tokens_embeddings[:3])

    # use article embedding to compare every news word tokens
    # normalize similarities so threshold can be used
    # find out which tokens should be kept as keywords
    article_tokens = sentence_processor.sentences2tokens(article)
    article_embedding = sentence_processor.tokens2embeddings(article_tokens)

    all_embeddings = [article_embedding] + news_tokens_embeddings
    # news_tokens_embeddings.insert(0, article_embedding)
    
    article2news_similarities = sentence_processor.sentences_similarity(all_embeddings)
    # print("article2news_similarities: ", article2news_similarities)
    article2news_similarities = normalize(article2news_similarities)
    
    keywords = []
    for word, simi in zip(news_words_final, article2news_similarities):
        print("token_word and simi: ", word, simi)
        if simi >= threshold:
            keywords.append(word)
    
    return keywords

def gen_article_by_gpt(news_dict, keywords_str, model):

    with open('sk.txt', 'r') as file:
        sk = file.read().strip()

    openai.api_key = sk
    messages = [
    # {"role":"user", "content":"要怎麼發表會引起大眾關注的文章？\n請簡短回答"},
    {"role":"user", "content": keywords_str + "\n請利用上述關鍵字用繁體中文重新改寫下面這篇文章並給出一個標題:\n" + 
     list(news_dict.values())[0] + "\n注意書寫格式為 標題: xxx 換行 內文: xxx"},
    ]

    chat_completion = openai.ChatCompletion.create(
    model=model,
    messages = messages,
    )

    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

