import pickle
import json
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from tensorflow.keras.models import load_model
import os
from django.conf import settings

lemmatizer= WordNetLemmatizer()
with open(os.path.join(settings.BASE_DIR, 'chatbotapp', 'intent.json')) as f:
    intents = json.load(f)
current_dir = os.path.dirname(os.path.abspath(__file__))
words = pickle.load(open(os.path.join(current_dir, 'words.pkl'), 'rb'))
classes = pickle.load(open(os.path.join(current_dir, 'classes.pkl'), 'rb'))
model = load_model(os.path.join(current_dir, 'chatbotmodel.h5'))

def clean_up_sentence(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def correct_spelling(sentence_words):
    spell = SpellChecker()
    corrected_words = []
    for word in sentence_words:
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)
    return corrected_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    corrected_sentence_words = correct_spelling(sentence_words)
    bag = [0] * len(words)
    for w in corrected_sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow=bag_of_words(sentence)
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results=[[i,r] for i, r in enumerate(res) if r> ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list=[]

    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})
    predicted_class_index = results[0][0]
    return predicted_class_index


def get_response(intents_list,intents_json):
    tag=classes[intents_list]
    list_of_intents=intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result=random.choice(i['responses'])
            break
    return result

print("Bot running")

def chatbot_response(message):    
    sentence_words = clean_up_sentence(message)
    corrected_sentence_words = correct_spelling(sentence_words)
    corrected_message = " ".join(corrected_sentence_words)
    print(f"Corrected message: {corrected_message}")
    ints = predict_class(message)
    res = get_response(ints, intents)
    return res
