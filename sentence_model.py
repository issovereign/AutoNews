from sentence_transformers import SentenceTransformer, util

def load_sentence_model():
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    return model

def sentences_similarity(model, sentences):

    embeddings = model.encode(sentences)
    print(embeddings)

    sim_list = []
    for i in range(1, len(embeddings)):

        curr_sim = util.cos_sim(embeddings[0], embeddings[i])
        print("{0:.4f}".format(curr_sim.tolist()[0][0]))
        sim_list.append(curr_sim.tolist()[0][0])
    
    return sim_list