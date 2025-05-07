from flask import Flask, request, jsonify
import nltk
import ollama
from transformers import pipeline 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def healthcare_chatbot(user_input):
    if "symptoms" in user_input.lower():
        return "It seems like you're experiencing symptoms. Please consult a doctor."
    elif "appointment" in user_input.lower():
        return "Would you like me to schedule an appointment for you?"
    elif "medication" in user_input.lower():
        return "It's important to take your prescribed medication regularly."
    else:
        response = ollama.chat(model="medllama2", messages=[{"role": "user", "content": user_input}])
        return response["message"]["content"]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    response = healthcare_chatbot(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
