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
    title_tokens = sentence_processor.sentences2tokens(title)
    article_tokens = sentence_processor.sentences2tokens(article)
    news_tokens_embeddings = sentence_processor.tokens2embeddings(title_tokens + article_tokens)

    # use article embedding to compare every tokens
    # normalize similarities so threshold can be used
    # find out those tokens should be keep as keywords
    article_embedding = sentence_processor.tokens2embeddings(article)
    article2news_similarities = sentence_processor.sentences_similarity(article_embedding + news_tokens_embeddings)
    article2news_similarities = normalize(article2news_similarities)
    
    keywords = []
    for token, simi in zip((title_tokens + article_tokens), article2news_similarities):
        if simi >= threshold:
            keywords.append(token)
    
    return keywords

# def call gpt to generate articles

# def push article to our own web
