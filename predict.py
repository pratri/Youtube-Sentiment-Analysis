import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

VOCAB_SIZE = 10000
MAX_LEN = 250
MODEL_PATH = 'sentiment_analysis_model.h5'

# Load the saved model
model = load_model(MODEL_PATH)

# Load the tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
    


def encode_texts(text_list):
    encoded_texts = []
    for text in text_list:
        tokens = tf.keras.preprocessing.text.text_to_word_sequence(text)
        
        
        tokens = [tokenizer.word_index[word] if word in tokenizer.word_index and tokenizer.word_index[word]<9999  else 0 for word in tokens]
        
        encoded_texts.append(tokens) 
    return pad_sequences(encoded_texts, maxlen=MAX_LEN, padding='post', value=VOCAB_SIZE-1)


def predict_sentiments(text_list):
    print("EHRE AT LEAST? predic.t.py")
    
    encoded_inputs = encode_texts(text_list)
    # print("ENCODED: ", encoded_inputs)
    # for val in encoded_inputs:
    #     for small_val in val:
    #         if small_val > 10000:
    #             print("OH NO!, ", small_val, " actual : ", val)
    predictions = np.argmax(model.predict(encoded_inputs), axis=-1)
    
    sentiments = []
    for prediction in predictions:
        if prediction == 0:
            sentiments.append("Negative")
        elif prediction == 1:
            sentiments.append("Neutral")
        else:
            sentiments.append("Positive")
    return sentiments

        
# print(tokenizer.word_index)
l = ['raise', 'your', 'hand', 'if', 'you’ve', 'been', 'watching', 'ksi', 'for', 'a', 'long', 'time', '🖐️']
# print(predict_sentiments(l))