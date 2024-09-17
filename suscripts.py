import openai
from dotenv import load_dotenv
import os
import supabase
from langchain_openai import ChatOpenAI
from openai import OpenAI

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_PUBLIC_KEY = os.getenv("SUPABASE_PUBLIC_KEY")
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
supabase_client_public = supabase.create_client(SUPABASE_URL, SUPABASE_PUBLIC_KEY)

client = OpenAI()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, max_tokens=300)

def get_embedding_from_description(optimized_description):
    try:
        response = client.embeddings.create(input=[optimized_description], model="text-embedding-ada-002")
        
        embedding = response.data[0].embedding
        
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def update_product_embedding(product_id):
    try:
        # Step 1: Retrieve the product's optimized_description from Supabase
        response = supabase_client.table('image_data').select('optimized_description').eq('id', product_id).single().execute()

        # Access the 'data' attribute of the response
        product_data = response.data
        
        if not product_data:
            print(f"No product found with ID {product_id}")
            return False

        optimized_description = product_data['optimized_description']

        if not optimized_description:
            print(f"No optimized description found for product ID {product_id}")
            return False

        # Step 2: Generate the embedding from the optimized description
        embedding = get_embedding_from_description(optimized_description)

        if not embedding:
            print("Failed to generate embedding.")
            return False

        # Step 3: Update the product's record with the new embedding
        update_response = supabase_client.table('image_data').update({
            'product_embeddings': embedding
        }).eq('id', product_id).execute()
     
        return True

    except Exception as e:
        print(f"Error processing product ID {product_id}: {e}")
        return False


# Example usage
product_id = 18  # Replace with the actual product ID you want to process
update_product_embedding(product_id)
