from flask import Flask, request, jsonify, render_template, session
from flask_session import Session  # Make sure to install Flask-Session
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.language_models.llms import LLM

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_very_secret_key'  # Change this to a real key in production
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html') 


model = genai.GenerativeModel(model_name="gemini-1.0-pro")
history = {'user': [], 'bot': []}
def format_history(history):
    conversation = ""
    for user_msg, bot_msg in zip(history["user"], history["bot"]):
        conversation += f"User: {user_msg}\nBot: {bot_msg}\n"
    return conversation
def create_prompt(history):
    formatted_history = format_history(history)
    prompt = (
        "You are an AI chatbot, named MindBot, trained specifically to provide support for mental health issues. Act as if you are the mindbot and response properly "
        "Firstly, if the question seems like a general conversation starter or not directly related to mental health support, "
        "like a simple 'Hi' or 'How can I help you?', respond in a welcoming and helpful manner. "
        "For more detailed inquiries related to mental health, use the following input from the conversation history to provide accurate, "
        "understandable, and empathetic support: \n\n"
        f"{formatted_history}"
        "Based on this context and the above conversation history, analyze this and respond as if you are having a conversation. "
        "If the question does not align with the kind of support you offer, please guide the user to ask a question more relevant to mental health support."
    )
    return prompt

@app.route('/chat', methods=['POST'])
def send_message():
    user_input = request.json['message']
    history['user'].append(user_input)
    convo = model.start_chat(history=[])
    prompt=create_prompt(history)
    convo.send_message(prompt)
    response = convo.last.text
    history['bot'].append(response)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
