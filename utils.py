import csv

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

def single_news_get_keywords(news, sentence_processor, threshold=0.8):
    
    title, article = news
    
    # get title's and article's tokens and embeddings
    news_tokens = sentence_processor.sentences2tokens(title + article)
    news_tokens_words = sentence_processor.tokenids2words(news_tokens)
    print("tokens: ", news_tokens)
    print("tokens to words: ", news_tokens_words)

    news_tokens_embeddings = sentence_processor.tokens2embeddings(news_tokens)
    # print("some embeddings: ", news_tokens_embeddings[:3])

    # use article embedding to compare every tokens
    # normalize similarities so threshold can be used
    # find out those tokens should be keep as keywords
    article_tokens = sentence_processor.sentences2tokens(article)
    article_embedding = sentence_processor.tokens2embeddings(article_tokens)
    article2news_similarities = sentence_processor.sentences_similarity(article_embedding + news_tokens_embeddings)
    print(article2news_similarities)
    article2news_similarities = normalize(article2news_similarities)
    
    keywords = []
    for token_word, simi in zip(news_tokens_words, article2news_similarities):
        print("token_word and simi: ", token_word, simi)
        if simi >= threshold:
            keywords.append(token_word)
    
    print(keywords)
    return keywords

# def call gpt to generate articles

# def push article to our own web
