from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

class SentenceProcessor:
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2') -> None:
        self.model = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    #Mean Pooling - Take attention mask into account for correct averaging
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
        sim_list = []
        for i in range(1, len(embeddings)):

            curr_sim = util.cos_sim(embeddings[0], embeddings[i])
            print("{0:.4f}".format(curr_sim.tolist()[0][0]))
            sim_list.append(curr_sim.tolist()[0][0])
        
        return sim_list

# original ver.
# def sentences_similarity(model, sentences):

#     embeddings = model.encode(sentences)
#     print(embeddings)

#     sim_list = []
#     for i in range(1, len(embeddings)):

#         curr_sim = util.cos_sim(embeddings[0], embeddings[i])
#         print("{0:.4f}".format(curr_sim.tolist()[0][0]))
#         sim_list.append(curr_sim.tolist()[0][0])
    
#     return sim_list