from nltk.stem import WordNetLemmatizer, PorterStemmer
import re
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import pandas as pd
import joblib
import random
import spacy

df = pd.read_csv('../data/legal_qa_summarized_full.csv')

# Generate random choices for welcome message
chatbot_welcome_messages = [
    "Welcome to LegalBot! I'm here to help answer your legal questions.",
    "Greetings! Ask me anything related to the law, and I'll do my best to assist you.",
    "Hello! I'm your virtual legal assistant. What legal questions do you have for me today?",
    "Welcome to LegalBot! How may I assist you with your legal concerns?",
]

cannot_answer_messages = [
    "I'm sorry, I don't have information on that topic. You may refer to {link} for more information.",
    "Unfortunately, I'm unable to answer that question at the moment. Please find relevant topics at {link}.",
    "I don't have the data needed to give a response to that. Consider checking {link} for detailed informaiton",
    "Sorry, I'm not able to offer information on that subject. Refer to {link} for further exploration.",
]

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return ' '.join(stemmed_tokens)

# Load the model and vectorizer
vectorizer = joblib.load('tfidf_vectorizer_cb1.joblib')
tfidf_matrix = joblib.load('tfidf_matrix_cb1.joblib')

# Load spaCy English tokenizer
nlp = spacy.load("en_core_web_sm")

def get_answer_of_the_most_similar_question(user_input):
    # user_input = ' '.join([token.text for token in nlp(user_input.lower())])
    user_input = preprocess(user_input)
    user_vector = vectorizer.transform([user_input])

    # Calculate cosine similarity
    similarities = cosine_similarity(user_vector, tfidf_matrix)

    # Get the index and score of the most similar question
    most_similar_index = similarities.argmax()
    highest_similarity_score = similarities[0, most_similar_index]

    # Check if the similarity score is greater than 0.5
    if highest_similarity_score >= 0.3:
        return df['answer'].iloc[most_similar_index]
    else:
        return ''

def chatbot():
    welcome_message = random.choice(chatbot_welcome_messages)
    print('Chatbot:', welcome_message)
    while True:
        user_input = input("User: ")
        
        if user_input.lower() == 'exit':
            print('Chatbot: Bye.')
            break

        response = get_answer_of_the_most_similar_question(user_input)
        if response == '':
            reference_links = ['https://thelawdictionary.org/', 'https://answers.justia.com/']
            cannot_answer_message = random.choice(cannot_answer_messages)
            reference_link = random.choice(reference_links)
            response = cannot_answer_message.format(link=reference_link)
        
        print("Chatbot:", response)

# Start the chatbot
chatbot()

# import random
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import nltk
# from nltk.stem import WordNetLemmatizer, PorterStemmer
# from nltk.corpus import stopwords
# import re
# import spacy
# import joblib

# # Load spaCy English tokenizer
# nlp = spacy.load("en_core_web_sm")

# # Load dataset
# df = pd.read_csv('../data/legal_qa_summarized_full.csv')

# # Preprocess text
# df['question'] = df['question'].str.lower()
# df['question'] = df['question'].apply(lambda x: ' '.join([token.text for token in nlp(x)]))

# # Create a TF-IDF vectorizer
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform(df['questions'])

# joblib.dump(vectorizer, 'rule_based_params/tfidf_vectorizer.joblib')
# joblib.dump(tfidf_matrix, 'rule_based_params/tfidf_matrix.joblib')

# # Generate random choices for welcome message
# chatbot_welcome_messages = [
#     "Welcome to LegalBot! I'm here to help answer your legal questions.",
#     "Greetings! Ask me anything related to the law, and I'll do my best to assist you.",
#     "Hello! I'm your virtual legal assistant. What legal questions do you have for me today?",
#     "Welcome to LegalBot! How may I assist you with your legal concerns?",
# ]

# cannot_answer_messages = [
#     "I'm sorry, I don't have information on that topic. You may refer to {link} for more information.",
#     "Unfortunately, I'm unable to answer that question at the moment. Please find relevant topics at {link}.",
#     "I'm afraid I cannot provide an answer for that specific question. Explore more at {link}",
#     "Sadly, that's beyond the scope of my capabilities. You might find useful information at {link}.",
#     "I don't have the data needed to give a response to that. Consider checking {link} for detailed informaiton",
#     "Sorry, I'm not able to offer information on that subject. Refer to {link} for further exploration.",
#     "I'm sorry, that's not within my current knowledge base. Consult {link} and you may have your answer.",
# ]

# def preprocess(text):
#     lemmatizer = WordNetLemmatizer()
#     stemmer = PorterStemmer()
#     text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters
#     tokens = nltk.word_tokenize(text.lower())
#     tokens = [token for token in tokens if token not in stopwords.words('english')]
#     lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
#     stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
#     return ' '.join(stemmed_tokens)

# def get_answer_of_the_most_similar_question(user_input, tfidf_matrix, vectorizer, nlp):
#     # user_input = ' '.join([token.text for token in nlp(user_input.lower())])
#     user_input = preprocess(user_input)
#     user_vector = vectorizer.transform([user_input])

#     # Calculate cosine similarity
#     similarities = cosine_similarity(user_vector, tfidf_matrix)

#     # Get the index and score of the most similar question
#     most_similar_index = similarities.argmax()
#     highest_similarity_score = similarities[0, most_similar_index]

#     # Check if the similarity score is greater than 0.5
#     if highest_similarity_score >= 0.3:
#         return df['answer'].iloc[most_similar_index]
#     else:
#         return ''

# def chatbot(nlp):
#     # Load the model and vectorizer
#     vectorizer = joblib.load('tfidf_vectorizer.joblib')
#     tfidf_matrix = joblib.load('tfidf_matrix.joblib')

#     welcome_message = random.choice(chatbot_welcome_messages)
#     print('Chatbot:', welcome_message)
#     while True:
#         user_input = input("User: ")
        
#         if user_input.lower() == 'exit':
#             print('Chatbot: N')
#             break

#         response = get_answer_of_the_most_similar_question(user_input, tfidf_matrix, vectorizer, nlp)
#         if response == '':
#             reference_links = ['https://thelawdictionary.org/', 'https://answers.justia.com/']
#             cannot_answer_message = random.choice(cannot_answer_messages)
#             reference_link = random.choice(reference_links)
#             response = cannot_answer_message.format(link=reference_link)
        
#         print("Chatbot:", response)

# # Start the chatbot
# chatbot(nlp)
