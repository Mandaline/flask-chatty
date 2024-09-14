from flask import Flask, jsonify, request
from flask_cors import CORS
from services import chat_response 


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


if __name__ == "__main__":
    app.run(debug=True, port=8080)