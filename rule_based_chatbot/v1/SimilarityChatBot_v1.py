import re
import random
import joblib
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logging.basicConfig(filename='running_logs.txt', level=logging.WARNING)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

df = pd.read_csv("../data/legal_qa_summarized_full.csv", encoding='unicode_escape')
questions_list = df['question'].tolist()
answers_list = df['answer'].tolist()

vectorizer = joblib.load('tfidf_vectorizer.joblib')
X = joblib.load('tfidf_matrix.joblib')

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return ' '.join(stemmed_tokens)

def preprocess_with_stopwords(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters
    tokens = nltk.word_tokenize(text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return ' '.join(stemmed_tokens)

def get_response(text):
    processed_text = preprocess_with_stopwords(text)
    print("processed_text:", processed_text)
    vectorized_text = vectorizer.transform([processed_text])
    similarities = cosine_similarity(vectorized_text, X)
    print("similarities:", similarities)
    max_similarity = np.max(similarities)
    print("max_similarity:", max_similarity)
    if max_similarity >= 0.3:
        high_similarity_questions = [q for q, s in zip(questions_list, similarities[0]) if s >= 0.3]
        print("high_similarity_questions:", high_similarity_questions)

        target_answers = []
        for q in high_similarity_questions:
            q_index = questions_list.index(q)
            target_answers.append(answers_list[q_index])
        print(target_answers)

        Z = vectorizer.fit_transform([preprocess_with_stopwords(q) for q in high_similarity_questions])
        processed_text_with_stopwords = preprocess_with_stopwords(text)
        print("processed_text_with_stopwords:", processed_text_with_stopwords)
        vectorized_text_with_stopwords = vectorizer.transform([processed_text_with_stopwords])
        final_similarities = cosine_similarity(vectorized_text_with_stopwords, Z)
        closest = np.argmax(final_similarities)
        return target_answers[closest]
    else:
        return "I can't answer this question."
    

def chatbot():
    print('Chatbot:', 'Ask me any questions about legal concerns.')
    while True:
        user_input = input("User: ")
        
        if user_input.lower() == 'exit':
            print('Chatbot: Bye.')
            break

        response = get_response(user_input)
        if response == "I can't answer this question.":
            reference_links = ['https://thelawdictionary.org/', 'https://answers.justia.com/']
            reference_link = random.choice(reference_links)
            response = f"{response} Please refer to {reference_link} for more information."
        
        print("Chatbot:", response)

# Start the chatbot
chatbot()