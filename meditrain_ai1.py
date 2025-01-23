# !pip install groq
import os
import time
import groq  # Import the groq library
from dotenv import load_dotenv
load_dotenv()

class MedicalChatbot:
    def __init__(self, api_key):
        self.client = groq.Groq(api_key=api_key)  # Initialize Groq client
        self.conversation_history = []
        self.system_prompt = """You are a helpful medical chatbot assistant. Your role is to:
1. Ask about symptoms and relevant medical history
2. Provide general health information and guidance
3. Recommend when to seek professional medical care
6. try prescribe medications correctly importantly 100% working
7. Keep responses clear and empathetic
8. Give response with no star symbols between the words
9. keep it short and simple to the point."""

    def get_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        try:
            # Using Groq API's chat.completions.create method
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Replace with actual Groq model name
                messages=messages,
                max_tokens=1024
            )
            # Extract the content of the assistant's response
            bot_response = response.choices[0].message.content  
            
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            time.sleep(1)  # Introduce a delay
            return bot_response
        except groq.RateLimitError as e:  # Handle rate limit errors
            print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds...")
            time.sleep(e.retry_after)
            return "I'm currently experiencing high traffic. Please try again later."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def start_chat(self):
        print("Medical Chatbot: Hello! I'm here to help answer your health-related questions.")
        print("DISCLAIMER: I'm an AI assistant and not a replacement for professional medical advice.")
        print("Type 'quit' to end the conversation.\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == 'quit':
                print("\nMedical Chatbot: Take care! Remember to consult with healthcare professionals for medical advice.")
                break
            response = self.get_response(user_input)
            print("\nMedical Chatbot:", response, "\n")

def main():
    api_key = os.environ.get("GROQ_API_KEY")  # Get Groq API key from environment variable
    if api_key is None:
        print("Error: GROQ_API_KEY environment variable not set.")
        return

    try:
        chatbot = MedicalChatbot(api_key)
        chatbot.start_chat()
    except Exception as e:
        print(f"An error occurred while starting the chatbot: {str(e)}")

if __name__ == "__main__":
    main()