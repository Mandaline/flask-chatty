from flask import Flask, jsonify, request
from flask_cors import CORS
from services import chat_response, generate_optimized_description, generate_keywords, get_embedding_from_description, extract_product_ids_from_response
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
    data = request.get_json()
    user_query = data.get("message")
    screenshot = data.get("screenshot", None)
    selected_shape = data.get("faceShape", None)
    
    if not user_query:
        return "No message provided", 400
    
    chat_result = chat_response(user_query, screenshot, selected_shape)

    product_ids = extract_product_ids_from_response(chat_result)

    products = []
    for product_id in product_ids:
        product = get_product_by_id(product_id)
        if product:
            products.append(product)

    response_data = {
        "message": chat_result,
        "products": products
    }

    return jsonify(response_data)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    
    # Check if the image, title, and description are provided in the request
    if 'image' not in request.files or 'description' not in request.form or 'title' not in request.form:
        return jsonify({"error": "Image, title, and description are required"}), 400

    image_file = request.files['image']
    user_description = request.form['description']
    title = request.form['title']

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)

        image_url = upload_image_to_supabase(image_file, filename)

        if not image_url:
            return jsonify({"error": "Failed to upload image to Supabase"}), 500

        # Generate an optimized description for the image using OpenAI and user input
        optimized_description = generate_optimized_description(image_url, user_description, title)

        embeddings = get_embedding_from_description(optimized_description)

        keywords = generate_keywords(optimized_description)

        store_in_supabase(title, user_description, optimized_description, image_url, keywords, embeddings)

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