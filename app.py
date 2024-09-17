from flask import Flask, jsonify, request
from flask_cors import CORS
from services import chat_response, generate_optimized_description, generate_keywords
from supabase_operations import upload_image_to_supabase, store_in_supabase, get_image_data, get_product_by_id, delete_product_by_id, delete_image_from_storage
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route('/')
def hello_world():
    return 'Hello, World!'

print(hello_world())

@app.route('/api/chat', methods=['POST'])
def chat():
    
    data = request.get_json()  # Get JSON data from request
    user_query = data.get("message")  # Extract user's message
    print(f"Request body: {data}")
    if not user_query:
        return "No message provided", 400
    
    # Pass the query to the chat_response function and return the response directly
    return chat_response(user_query)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    print("running")
    
    # Check if the image, title, and description are provided in the request
    if 'image' not in request.files or 'description' not in request.form or 'title' not in request.form:
        return jsonify({"error": "Image, title, and description are required"}), 400

    # Extract the image file, title, and description from the request
    image_file = request.files['image']
    user_description = request.form['description']
    title = request.form['title']

    # Validate if the file extension is allowed
    if image_file and allowed_file(image_file.filename):
        # Secure the filename to prevent issues like directory traversal
        filename = secure_filename(image_file.filename)
        print(f"filename uuuuuuu: {filename}")
        # Upload the image to Supabase Storage and get the public URL
        image_url = upload_image_to_supabase(image_file, filename)

        if not image_url:
            return jsonify({"error": "Failed to upload image to Supabase"}), 500

        # Generate an optimized description for the image using OpenAI
        optimized_description = generate_optimized_description(image_url, user_description, title)

        keywords = generate_keywords(optimized_description)

        # Store the metadata in the Supabase database
        store_in_supabase(title, user_description, optimized_description, image_url, keywords)

        # Return the optimized description as the response
        return jsonify({"optimized_description": optimized_description})

    return jsonify({"error": "Invalid file type"}), 400


@app.route('/api/get-images', methods=['GET'])
def get_images():
    data = get_image_data()
    return jsonify(data)

@app.route('/api/delete-image/<int:id>', methods=['DELETE'])
def delete_image(id):

    product = get_product_by_id(id)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404

    image_url = product.get('image_url')

    error = delete_product_by_id(id)

    if error:
        return jsonify({"error": f"Failed to delete product: {error}"}), 500

    delete_image_from_storage(image_url)

    return jsonify({"message": "Product deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=8080)