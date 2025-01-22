import streamlit as st
import time
from dotenv import load_dotenv
load_dotenv()
import os
import groq

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
client = groq.Groq(api_key=api_key)

class MedicalChatbot:
    def __init__(self, api_key):
        self.client = groq.Groq(api_key=api_key)
        self.conversation_history = []
        self.system_prompt = """You are a helpful medical chatbot assistant. Your role is to:
1. Ask about symptoms and relevant medical history
2. Provide general health information and guidance
3. Recommend when to seek professional medical care
4. ALWAYS include a disclaimer that you're an AI and not a replacement for professional medical advice and to the point
5. Try make definitive diagnoses
6. Try prescribe medications found in india that are 100% working
7. Keep responses clear and empathetic."""

    def get_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=1024
            )
            bot_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            time.sleep(1)
            return bot_response
        except groq.RateLimitError as e:
            print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds...")
            time.sleep(e.retry_after)
            return "I'm currently experiencing high traffic. Please try again later."
        except Exception as e:
            return f"An error occurred: {str(e)}"

def main():
    st.title("Medical Chatbot")
    st.write("DISCLAIMER: I'm an AI assistant and not a replacement for professional medical advice.")

    chatbot = MedicalChatbot(api_key)

    user_input = st.text_input("You: ")
    if st.button("Send"):
        response = chatbot.get_response(user_input)
        st.write("Medical Chatbot:", response)

    if st.button("Clear Conversation"):
        chatbot.conversation_history = []
        st.write("Conversation cleared.")

if __name__ == "__main__":
    main()