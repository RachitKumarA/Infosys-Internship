import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from meditrain_ai1 import MedicalChatbot

load_dotenv()

app = Flask(__name__)

# Initialize the chatbot once
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("No API key found. Please set GROQ_API_KEY in your environment.")

chatbot = MedicalChatbot(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        bot_response = chatbot.get_response(user_message)
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)