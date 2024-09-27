from dotenv import load_dotenv
import os
import numpy as np
from openai import OpenAI
import json
from supabase_utils.supabase_operations import get_image_data

load_dotenv()

client = OpenAI()

openai_api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return response.data[0].embedding

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def find_top_products(user_embedding, top_n=4):

    products = get_image_data()
    product_scores = []

    for product in products:
        product_embedding_str = product['product_embeddings']
        product_embedding = json.loads(product_embedding_str)
        
        similarity = cosine_similarity(user_embedding, product_embedding)
        product_scores.append((product, similarity))

    product_scores.sort(key=lambda x: x[1], reverse=True)
    return product_scores[:top_n]
