from .embedding_service import get_embedding, find_top_products
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
from constants import face_shapes_guide_prompt, face_shapes_guide

load_dotenv()

client = OpenAI()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, max_tokens=300)

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


def chat_response(user_query, screenshot, selected_shape): 
    if screenshot:
        shape_recommendation = get_type_recommendation(screenshot) 
    else:
        shape_recommendation = get_type_recommendation_text(selected_shape)
   
    print(f"recomendation text: {shape_recommendation}")
    user_embedding = get_embedding(user_query)

    top_products = find_top_products(user_embedding, top_n=4)

    recommended_products = [
        {"id": product["id"], "title": product["title"], "description": product["optimized_description"]}
        for product, similarity in top_products
    ]
    
    prompt_text = """
    	You are a helpful shopping assistant trying to match customers with the right product. 
    	You will be given a {question} from a customer, and a list of {recommended_products} of the products available for sale that roughly match the customer's question.
    	Among the products given, find two that best match their question but also their face shapes based on this recommendation about what style of glasses look best for their face shapes {shape_recomendation}.
    	If there are none matching their question, apologize and make an alternative recommendation that is the closest match to their request.
    	Respond with the one or two face shapes identified in the shape recommendation using <strong> tags, no parantheses. If there are two face shapes, name the first as the primary face shape and the second as the secondary one.
    	Then give the two best product matches, with the title of each product, then a short summary of why the product is a good match for the customer, including what makes it appropriate for the face shape. 
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
