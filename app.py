from flask import Flask,request, render_template,request,flash,redirect,url_for,session,Response
import json
import random
import enum
from os import access, sendfile
import random
from threading import active_count
from absl.logging import ERROR
from nltk import tag
from nltk.parse.nonprojectivedependencyparser import DemoScorer
from nltk.sem.relextract import descape_entity
import numpy as np
import json 
import pickle
import nltk


from nltk.stem import WordNetLemmatizer
from tensorflow.keras import models
from tensorflow.keras import optimizers

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.python.keras import activations
from tensorflow.python.keras.engine import training
from tensorflow.python.keras.feature_column.dense_features_v2 import DenseFeatures
from tensorflow.keras.models import load_model



app=Flask(__name__)

lemmatizer=WordNetLemmatizer()

intents= json.loads(open("intents.json").read())

words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))

model=load_model('chat_bot.model')


def clean_up_sentence(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words=clean_up_sentence(sentence)
    bag=[0]*len(words)

    for w in sentence_words:
        for i, word in enumerate(words):
            if word==w:
                bag[i]=1

    return np.array(bag)


def predict_class(sentence):
    bow=bag_of_words(sentence)
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.25

    results=[[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list=[]

    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})

    return return_list

def get_response(intents_list,intents_json):
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag']  == tag:
                result = random.choice(i['responses'])
                break
    except IndexError:
        result = "I don't understand!"

    return result





@app.route("/")
@app.route("/messaging",methods=['GET','POST'])
def message():
    data="Hi there, I\'m Dadson Derrick, what\'s on your mind today?"

    if request.method == 'POST':
        message = request.json["message"]
        print(message)

        # print(message)
        ints=predict_class(message)
        res=get_response(ints,intents)


        return {"message": res}

    return render_template("message.html",Koto=data)


if __name__=='__main__':
    app.run(debug=True)

    

 

