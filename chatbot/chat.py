from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Load and clean document data
def load_document(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return "Error: Unable to load document."

DOCUMENT_DATA = load_document("dsa_content.txt")

# Split document into sections (each concept block)
def extract_relevant_sections(doc, user_input):
    sections = doc.strip().split("\n\n")
    relevant = [sec for sec in sections if any(word.lower() in sec.lower() for word in user_input.split())]
    return "\n\n".join(relevant) if relevant else "No exact match, but try this overview:\n\n" + doc

# Gemini setup
genai.configure(api_key="AIzaSyBAcSi9ToAbYGeqqvKijDAXzbm-0ySsiQc")  # Replace with your real key
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    data = request.get_json()
    user_input = data.get('message', '').strip()
    if not user_input:
        return jsonify({'error': 'Please provide a message'}), 400

    # Filter document content based on user input
    relevant_data = extract_relevant_sections(DOCUMENT_DATA, user_input)

    # Optimized prompt
    prompt = f"""
You are a DSA tutor. Refer only to the following document sections to answer the user prompt clearly.

--- DOCUMENT SECTION ---
{relevant_data}
--- END ---

Now answer this question: {user_input}
"""

    try:
        response = chat.send_message(prompt)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)
