import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from meditrain_ai1 import MedicalChatbot
from dbModels import db, ChatMessage

load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Initialize the chatbot
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("No API key found. Please set GROQ_API_KEY in your environment.")

chatbot = MedicalChatbot(api_key)

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()

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
        
        # Store the chat message in the database
        chat_message = ChatMessage(
            user_message=user_message,
            bot_response=bot_response
        )
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat-history', methods=['GET'])
def get_chat_history():
    try:
        messages = ChatMessage.query.order_by(ChatMessage.timestamp.desc()).all()
        return jsonify({
            'history': [message.to_dict() for message in messages]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()  # Initialize the database tables
    app.run(debug=True)