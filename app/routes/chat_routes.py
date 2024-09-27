from flask import Blueprint, jsonify, request
from ..services import chat_service, product_service
from supabase_utils.supabase_operations import get_product_by_id

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = data.get("message")
    screenshot = data.get("screenshot", None)
    selected_shape = data.get("faceShape", None)

    if not user_query:
        return "No message provided", 400

    chat_result = chat_service.chat_response(user_query, screenshot, selected_shape)
    product_ids = product_service.extract_product_ids_from_response(chat_result)

    products = [get_product_by_id(pid) for pid in product_ids if get_product_by_id(pid)]

    response_data = {
        "message": chat_result,
        "products": products
    }

    return jsonify(response_data)
