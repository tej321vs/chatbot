from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

genai.configure(api_key="AIzaSyBAcSi9ToAbYGeqqvKijDAXzbm-0ySsiQc")

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    data = request.get_json()
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': "Please send a valid message."}), 400

    prompt = f"""
    You are a helpful AI tutor trained in Data Structures and Algorithms.
    Provide clear explanations, examples, and diagrams (if applicable).

    User: {user_input}
    """

    try:
        response = chat.send_message(prompt)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
