import openai
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import numpy as np
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from supabase_operations import get_image_data
import json
from bs4 import BeautifulSoup


load_dotenv()

client = OpenAI()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, max_tokens=300)

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


def chat_response(user_query): 
    user_embedding = get_embedding(user_query)

    top_products = find_top_products(user_embedding, top_n=4)

    recommended_products = [
        {"id": product["id"], "title": product["title"], "description": product["optimized_description"]}
        for product, similarity in top_products
    ]

    recommended_products = json.dumps(recommended_products)
    prompt = ChatPromptTemplate.from_template("You are a helpful shopping assistant trying to match customers with the right product. You will be given a {question} from a customer as and a list of {recommended_products} as the context with the title and description of the products available for sale that roughly match the customer's question. Respond with the two best product matches, with the title of each product, then a short summary of why the product is a good match for the customer. Wrap the title in a strong tag, like <strong>(title)</strong> and add a <br> before and after it. Use the product's id wrapped in a <span> tag with the className='hidden' and the id='product-id'")
    
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
		"question": user_query,
		"recommended_products": recommended_products
	})

def generate_optimized_description(image_url, user_description, title):
    
    prompt = f"Create a product description for a pair of sunglasses based on the image. The title of the product is {title}. The materials used in the construction of the sunglasses are in the {user_description}. Explain the style, shape, and details of the sunglasses based on what you see in the image. Focus particularly on the shape of the frames. Include the following in the final product description: Shape of the frames: Describe the specific geometry and style of the frames, focusing on whether they are round, square, oval, aviator, or any other shape. Style: Comment on the overall aesthetic, such as whether the sunglasses are modern, retro, sporty, or elegant. Materials: Use the materials input by the user to highlight their quality, texture, and how they contribute to design and functionality. Use an ### for the first title and ** for the bolded subtitles."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {
            "role": "user",
            "content": [
              { "type": "text", "text": prompt},
              {
                "type": "image_url",
                "image_url": {
                  "url": image_url,
                },
              },
            ],
          },
        ],
        max_tokens=300,
    )
    
    optimized_description = response.choices[0].message.content

    return optimized_description

def get_embedding_from_description(optimized_description):
    try:
        response = client.embeddings.create(input=[optimized_description], model="text-embedding-ada-002")
        
        embedding = response.data[0].embedding
        
        return embedding
    
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def generate_keywords(description):
	keyword_prompt = f"Extract the most important keywords or key phrases from this {description}. Return the keywords as a comma-separated list. The word 'sunglasses' should be excluded."

	keyword_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {
            "role": "user",
            "content": keyword_prompt,
          },
        ],
        max_tokens=100,
    )

	attributes = keyword_response.choices[0].message.content.strip()

	return attributes

def extract_product_ids_from_response(chat_result):
    soup = BeautifulSoup(chat_result, "html.parser")
    product_ids = []

    # Find all span elements with id="product-id"
    for span in soup.find_all("span", id="product-id"):
        product_id = span.get_text()  # Extract the text inside the span (product ID)
        product_ids.append(product_id)

    return product_ids