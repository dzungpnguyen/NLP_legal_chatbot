from flask import Flask, render_template, request
import random
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained('../ml_based_chatbot/saved_model')
model = AutoModelForSeq2SeqLM.from_pretrained('../ml_based_chatbot/saved_model')

chatbot_welcome_messages = [
    "Welcome to LegalBot! I'm here to help answer your legal questions.",
    "Greetings! Ask me anything related to the law, and I'll do my best to assist you.",
    "Hello! I'm your virtual legal assistant. What legal questions do you have for me today?",
    "Welcome to LegalBot! How may I assist you with your legal concerns?",
]

reference_links = ['https://thelawdictionary.org/', 'https://answers.justia.com/']

def get_response(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_length=50, temperature=0.9, do_sample=True)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text

@app.route('/')
def index():
    welcome_message = random.choice(chatbot_welcome_messages)
    return render_template('index.html', welcome_message=welcome_message)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    chatbot_response = get_response(user_input)
    ref_link = random.choice(reference_links)
    return {'bot_response': chatbot_response, 'reference_link': ref_link}

if __name__ == '__main__':
    app.run(debug=True)
