# import logging
import random
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# logging.basicConfig(filename='warnings.log', level=logging.WARNING)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('../ml_based_chatbot/saved_model')
model = AutoModelForSeq2SeqLM.from_pretrained('../ml_based_chatbot/saved_model')

# Choices for welcome messages
chatbot_welcome_messages = [
    "Welcome to LegalBot! I'm here to help answer your legal questions.",
    "Greetings! Ask me anything related to the law, and I'll do my best to assist you.",
    "Hello! I'm your virtual legal assistant. What legal questions do you have for me today?",
    "Welcome to LegalBot! How may I assist you with your legal concerns?",
]

# Reference links
reference_links = ['https://thelawdictionary.org/', 'https://answers.justia.com/']

# Function to generate answer from input question
def get_response(input_text):
    # Tokenize input
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    # Get output
    output_ids = model.generate(input_ids, max_length=50, temperature=0.9, do_sample=True)
    # Decode the output
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text

# Build chatbot
def chatbot():
    # Welcome
    welcome_message = random.choice(chatbot_welcome_messages)
    print('Bot:', welcome_message)
    
    # Start conversation loop
    while True:
        # Get user's input
        user_input = input('User: ')
        
        # End the conversation if user types 'exit'
        if user_input == 'exit':
            print('Bot: Bye.')
            break

        chatbot_response = get_response(user_input)
        ref_link = random.choice(reference_links)
        print(f'Bot: {chatbot_response}. Refer to {ref_link} for more information.')

# Run
chatbot()