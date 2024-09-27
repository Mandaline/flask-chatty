from flask import Flask
from flask_cors import CORS

from .routes.chat_routes import chat_bp  # Import the chat blueprint
from .routes.product_routes import product_bp  # Import the product blueprint

def create_app():
    app = Flask(__name__)
    CORS(app, origins='*')

    # Register the blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(product_bp)

    return app