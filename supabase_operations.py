from dotenv import load_dotenv
import os
import supabase

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
        public_url = supabase_client_public.storage.from_(bucket_name).get_public_url(path_on_supastorage)
		
        if public_url:
            print(f"Image already exists. Returning public URL: {public_url}")
            return public_url

        file_data = image_file.read()

        response = supabase_client.storage.from_(bucket_name).upload(
            path=path_on_supastorage,
            file=file_data,
            file_options={"content-type": image_file.content_type}
        )
		
        if response.status_code != 200:
            error_message = response.json().get('error', 'Unknown error occurred')
            print(f"Error uploading image: {error_message}")
            return None

        public_url = supabase_client.storage.from_(bucket_name).get_public_url(path_on_supastorage)
        return public_url

    except Exception as e:
        print(f"Error uploading image to Supabase: {e}")
        return None

def store_in_supabase(title, user_description, optimized_description, image_url):
    data = {
        "title": title,
        "user_description": user_description,
        "optimized_description": optimized_description,
        "image_url": image_url
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
    if response.error:
        return response.error
    return None 

def delete_image_from_storage(image_url):
    if image_url:
        path = image_url.split("/")[-1]
        supabase_client.storage.from_('images').remove([path])