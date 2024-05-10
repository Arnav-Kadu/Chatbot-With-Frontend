from flask import Flask, render_template, request, jsonify,redirect,session
from dotenv import load_dotenv
from typing import List, Optional, Any, Mapping
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
import os
from flask import make_response
import pyrebase

app = Flask(__name__)
firebaseConfig = {
  'apiKey': "AIzaSyB3Dya2tTYef2VlaxZVQVxkO_Avfc5UOfg",
  'authDomain': "mindbot-9bcc7.firebaseapp.com",
  'projectId': "mindbot-9bcc7",
  'storageBucket': "mindbot-9bcc7.appspot.com",
  'messagingSenderId': "80842807023",
  'appId': "1:80842807023:web:68f43ebf6e5875d21f6d1a",
  'databaseURL':''
}
firbase=pyrebase.initialize_app(firebaseConfig)
auth=firbase.auth()
app.secret_key='secret'
# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Define custom GeminiProLLM class inheriting from LLM
class GeminiProLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "gemini-1.0-pro"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        
        # Configure GenerativeAI with API key
        genai.configure(api_key=GEMINI_API_KEY)
        system_instruction = '''
        You are a friendly AI chatbot , Your Name is MindBot trained specifically to provide support for mental health issues.Use cognitive behavioral therapy to answer the user prompts and always ask them "What is the problem they are facing" or "how can you help them" and similar questions
Also if your answer includes points,list them in bullet points while displaying the answer

Start by greeting the user warmly and introducing the chatbot as a supportive companion for practicing cognitive behavioral therapy (CBT).

Prompt the user to share their current thoughts, feelings, or concerns. Ask open-ended questions to understand the user's emotions, triggers, and cognitive distortions.

Guide the user through identifying and labeling their thoughts or beliefs associated with their emotions. Encourage the user to recognize any negative or unhelpful thought patterns.

Teach the user to challenge their negative thoughts by examining evidence, alternative perspectives, and logical reasoning. Provide examples of cognitive distortions and techniques to counter them (e.g., "catastrophizing", "black-and-white thinking").

Offer coping strategies and techniques for managing distressing thoughts and emotions. Encourage the user to practice relaxation exercises, mindfulness, or self-care activities.

Discuss behavioral activation techniques to encourage the user to engage in enjoyable or meaningful activities. Help the user set achievable goals and plan small steps towards their desired outcomes.

Provide positive reinforcement and validation for the user's efforts and progress. Celebrate small victories and acknowledge improvements in coping skills.

Encourage the user to reflect on their experience and provide feedback on the effectiveness of the strategies discussed. Offer additional support or resources as needed.

End the conversation on a positive note, expressing confidence in the user's ability to apply CBT techniques in their daily life. Provide encouragement and reassurance that the chatbot is available whenever needed.
Also if the question is not about mental health or support tackle it properly instructing that you are here for mental health support.
   IMPORTANT NOTE: Just the response as you are directly talking
   you also understand all languages also response in respective language if needed.
   You please give response with html tags so that i can directly render it (don't add ```html in it also not last line spaces should be left) use <b> tag whereever you bold tags, paragraph tags and also proper line breaks
        '''
        gemini_pro_model = genai.GenerativeModel("gemini-1.5-pro-latest", system_instruction=system_instruction)
        
        # Generate response using the Gemini Pro model
        model_response = gemini_pro_model.generate_content(prompt)

        if len(model_response.candidates[0].content.parts) > 0:
            return model_response.candidates[0].content.parts[0].text
        else:
            return "<No answer by given Gemini Pro>"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model_id": "gemini-1.5-pro-latest", "temperature": 0.1}

# Function to load conversation chain
def load_chain():
    llm = GeminiProLLM()
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain

chatchain = load_chain()

from flask import request

@app.route("/login", methods=["POST","GET"])
def login():
    if ('user' in session):
        return redirect('/')
    if request.method=='POST':
        email = request.form.get('loginId')
        password = request.form.get('password')

        try:
            print(email)
            print(password)
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/')
        except:
            return 'Failed to login'
    return render_template("login.html")

@app.route("/signup", methods=["POST","GET"])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method=='POST':
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/')
        except:
            return 'Signup failed'
    
    return render_template("signup.html")

@app.route("/")
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = chatchain(user_input)["response"]
    return jsonify({"response": response})
@app.route("/get_username", methods=["GET"])
def get_username():
    if 'user' in session:
        email = session['user']
        username = email.split('@')[0] 
        return jsonify({'username': username})
    else:
        return jsonify({'username': None})
@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user')
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
