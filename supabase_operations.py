from dotenv import load_dotenv
import os
import supabase
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_PUBLIC_KEY = os.getenv("SUPABASE_PUBLIC_KEY")
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
supabase_client_public = supabase.create_client(SUPABASE_URL, SUPABASE_PUBLIC_KEY)

def upload_image_to_supabase(image_file, filename):
    bucket_name = "images"
    path_on_supastorage = filename

    try:
        # First see if the image url already exists and if it returns a real image
        public_url = supabase_client.storage.from_(bucket_name).get_public_url(path_on_supastorage)

        response = requests.get(public_url)
        if response.status_code == 200:
            print(f"public_url (existing): {public_url}")
            return public_url
        else:
            print(f"Image not found at public URL. Status code: {response.status_code}, message: {response.text}")

        file_data = image_file.read()

        response = supabase_client.storage.from_(bucket_name).upload(
            path=path_on_supastorage,
            file=file_data,
            file_options={"content-type": image_file.content_type}
        )

        response_json = response.json()

        if 'statusCode' in response_json and 'error' in response_json:
            error_code = response_json['error']
            if error_code == 'Duplicate':
                public_url = supabase_client.storage.from_(bucket_name).get_public_url(path_on_supastorage)
                print(f"public_url (from duplicate): {public_url}")
                return public_url
            else:
                return response_json['message']

        public_url = supabase_client.storage.from_(bucket_name).get_public_url(path_on_supastorage)
        print(f"public_url (new upload): {public_url}")
        return public_url

    except Exception as e:
        print(f"Error uploading image to Supabase: {e}")
        return None


def store_in_supabase(title, user_description, optimized_description, image_url, keywords, embeddings):
    data = {
        "title": title,
        "user_description": user_description,
        "optimized_description": optimized_description,
        "image_url": image_url,
        "keywords": keywords,
        "product_embeddings": embeddings
    }
    supabase_client.table('image_data').insert(data).execute()

def get_image_data():
    response = supabase_client.table('image_data').select("*").execute()
    return response.data

def get_product_by_id(product_id):
    response = supabase_client_public.table('image_data').select('*').eq('id', product_id).execute()
    if not response.data:
        return None
    return response.data[0]

def delete_product_by_id(product_id):
    response = supabase_client_public.table('image_data').delete().eq('id', product_id).execute()
    print(f"Response: {response}")

    if 'code' in response and response['code'] != 200:
        return response['message']
    return None

def delete_image_from_storage(image_url):
    if image_url:
        print(f"image url {image_url}")
        path = image_url.split("/")[-1]
        supabase_client.storage.from_('images').remove([path])