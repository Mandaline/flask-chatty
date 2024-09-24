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
from face_shapes import face_shapes_guide_prompt, face_shapes_guide, sunglass_styles


load_dotenv()

client = OpenAI()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, max_tokens=300)

def get_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return response.data[0].embedding

def get_type_recommendation(image_url):

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
          {
            "role": "user",
            "content": [
              { "type": "text", "text": face_shapes_guide_prompt},
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
    
    type_recommendation = response.choices[0].message.content

    return type_recommendation

def get_type_recommendation_text(selected_shape):
    prompt = f"""
    This is the user's selected face shape: {selected_shape}. 
    Please respond with the user's face shape and and provide recommendations for sunglasses that would suit that shape
    based on the following face shapes guide: 
    {face_shapes_guide}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {
            "role": "user",
            "content": prompt
          },
        ],
        max_tokens=300,
    )

    shape_recommendation = response.choices[0].message.content

    return shape_recommendation


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


def chat_response(user_query, screenshot, selected_shape): 
    if screenshot:
        shape_recommendation = get_type_recommendation(screenshot) 
    else:
        shape_recommendation = get_type_recommendation_text(selected_shape)
   
    # combined_text = f"User's request: {user_query}\nType recommendation: {shape_recommendation}"
    # print(f"combined_text: {combined_text}")
    user_embedding = get_embedding(user_query)

    top_products = find_top_products(user_embedding, top_n=4)

    recommended_products = [
        {"id": product["id"], "title": product["title"], "description": product["optimized_description"]}
        for product, similarity in top_products
    ]
    
    prompt_text = """
    	You are a helpful shopping assistant trying to match customers with the right product. 
    	You will be given a {question} from a customer, and a list of {recommended_products} of the products available for sale that roughly match the customer's question.
    	Among the products given, find two that best match their question but also their face shape based on this recommendation about what style of glasses look best for their face shape {shape_recomendation}.
        If there are none matching their question, apologize and make an alternative recommendation that is the closest match to their request.
        Respond with the face shape identified in the shape recommendation using <strong> tags, no parantheses, along with the two best product matches, with the title of each product, then a short summary of why the product is a good match for the customer, including what makes it appropriate for the face shape. 
    	Wrap the title in a strong tag, like <strong>(title)</strong> and add a <br> before and after it. Use the product's id wrapped in a <span> tag with the className='hidden' and the id='product-id'
    """

    recommended_products = json.dumps(recommended_products)
    prompt = ChatPromptTemplate.from_template(prompt_text)
    
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
		"question": user_query,
		"recommended_products": recommended_products,
		"shape_recomendation": shape_recommendation
	})

def generate_optimized_description(image_url, user_description, title):
    
    sunglass_styles_prompt = f"""
		Create a product description for a pair of sunglasses based on the image. 
		The title of the product is {title}. The materials used in the construction of the sunglasses are in the {user_description}. 
		Explain the style, shape, and details of the sunglasses based on what you see in the image, using the this guide to sunglasses to create a description {sunglass_styles}
		Include the following in the final product description, but be concise and try to use only what you see in the image, the styles guide, and user description. Make sure to include the shape. 
		Frame types: Describe the specific shape and style of the frames.
		Style: Comment on the overall aesthetic. 
		Materials: Describe the materials, lens types and colors.
		Face shape matches: What face shapes are best and why. Include all the best for recommendations in the sunglass styles guide.
		Use an ### for the first title and ** for the bolded subtitles.
	""" 

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {
            "role": "user",
            "content": [
              { "type": "text", "text": sunglass_styles_prompt},
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
	keyword_prompt = f"Extract the most important keywords or key phrases from this {description}. Return the keywords as a comma-separated list. The word 'sunglasses', 'frame types' and the title of the glasses should be excluded. Also exclude the face shapes mentioned."

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

    for span in soup.find_all("span", id="product-id"):
        product_id = span.get_text()
        product_ids.append(product_id)

    return product_ids