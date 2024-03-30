from transformers import AutoTokenizer, AutoModel, BertTokenizerFast
from ckip_transformers.nlp import CkipWordSegmenter

from sklearn.metrics.pairwise import cosine_similarity
import torch
import torch.nn.functional as F

class SentenceProcessor:
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2') -> None:

        # self.model = AutoModel.from_pretrained(model_name)
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained('ckiplab/bert-base-chinese-ws')
        self.tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')

        # word segmenter must eat a ["string"], not a "string", so it can segment word correctly
        self.word_segmenter = CkipWordSegmenter(model="bert-base")

    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def sentences2tokens(self, sentences):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        return encoded_input

    def tokenids2words(self, encoded_input):
        token_inputs_ids = encoded_input['input_ids'].tolist()[0]
        token_words = self.tokenizer.convert_ids_to_tokens(token_inputs_ids)
        return token_words

    def tokens2embeddings(self, encoded_input):
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        tokens_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        tokens_embeddings = F.normalize(tokens_embeddings, p=2, dim=1)

        return tokens_embeddings

    def sentences_similarity(self, embeddings):
        # print("Embeddings: ", embeddings)
        sim_list = []
        for i in range(1, len(embeddings)):
            curr_sim = cosine_similarity(embeddings[0].reshape(1, -1), embeddings[i].reshape(1, -1))[0][0]
            # print(curr_sim)
            sim_list.append(curr_sim)
        
        return sim_list
