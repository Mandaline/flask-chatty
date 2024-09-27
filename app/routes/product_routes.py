from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from ..services import embedding_service
from supabase_utils.supabase_operations import (
	get_product_by_id,
	store_in_supabase,
	upload_image_to_supabase, get_image_data,
	delete_product_by_id,
	delete_image_from_storage
)

product_bp = Blueprint('product_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product_bp.route('/api/upload-image', methods=['POST'])
def upload_image():
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

		optimized_description = embedding_service.generate_optimized_description(image_url, user_description, title)
		embeddings = embedding_service.get_embedding_from_description(optimized_description)
		keywords = embedding_service.generate_keywords(optimized_description)

		store_in_supabase(title, user_description, optimized_description, image_url, keywords, embeddings)

		return jsonify({"optimized_description": optimized_description})

	return jsonify({"error": "Invalid file type"}), 400

@product_bp.route('/api/get-images', methods=['GET'])
def get_images():
	data = get_image_data()
	return jsonify(data)

@product_bp.route('/api/delete-image/<int:id>', methods=['DELETE'])
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