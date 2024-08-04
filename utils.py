import openai
import faiss
import numpy as np
from dotenv import load_dotenv 
import os


load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

def get_openai_embeddings(text, model="text-embedding-3-large"):
    response = openai.embeddings.create(input=text, model=model)
    embeddings = response.data[0].embedding
    return np.array(embeddings)

# This function is to perform similarity search using FAISS
def get_best_match(query, docs):
    # Calculating embeddings for the documents
    doc_embeddings = np.array([get_openai_embeddings(doc) for doc in docs])

    # Creating FAISS index
    dim = doc_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(doc_embeddings)

    # Calculating embedding for the query
    query_embedding = get_openai_embeddings(query).reshape(1, -1)

    # Performing similarity search
    _, indices = index.search(query_embedding, k=10)
    # Extracting the best matches
    best_matches = [docs[idx] for idx in indices[0]]
    # best_match_index = indices[0][0]

    return best_matches # docs[best_match_index]
