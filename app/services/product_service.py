from dotenv import load_dotenv
import os
from openai import OpenAI
from bs4 import BeautifulSoup
from constants import sunglass_styles

load_dotenv()

client = OpenAI()

openai_api_key = os.getenv("OPENAI_API_KEY")

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