from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model
import gensim
from konlpy.tag import Okt

app=Flask(__name__)
MIN_NOUN_VECTOR_VALUE = -10.0
MAX_NOUN_VECTOR_VALUE = 10.0
NOUN_VECTOR_SIZE = 100
TITLE_LENGTH = 37

def generate_random_noun_vector():
    return np.random.uniform(low=MIN_NOUN_VECTOR_VALUE,
                             high=MAX_NOUN_VECTOR_VALUE,
                             size=(NOUN_VECTOR_SIZE,))

def generate_zero_noun_vector():
    return np.random.uniform(low=0.0, high=0.0,size=(NOUN_VECTOR_SIZE,))

@app.route('/')
def home():
    return render_template('text/index.html')

@app.route('/text_result', methods=['POST'])
def result():
    model=load_model('c:/data/text')
    text=request.form['text']
    twitter_nlp=Okt()
    title_noun_arr=[]
    title_noun_arr.append(twitter_nlp.nouns(text))

    w2v_model=gensim.models.Word2Vec.load('c:/data/text/text_100.model')
    title_noun_vector_arr=[]
    for index, title_noun in enumerate(title_noun_arr):
        noun_vector_arr=[]
        for noun in title_noun:
            try:
                noun_vector=w2v_model[noun]
            except:
                noun_vector=generate_random_noun_vector()
            noun_vector_arr.append(noun_vector)
        title_noun_vector_arr.append(noun_vector_arr)
    for index, title_noun_vector in enumerate(title_noun_vector_arr):
        while len(title_noun_vector) < TITLE_LENGTH:
            title_noun_vector.append(generate_zero_noun_vector())
        title_noun_vector=title_noun_vector[:TITLE_LENGTH]
    noun_vector_arr=np.array(title_noun_vector_arr).reshape(1,37,100,1)
    pred=model.predict(noun_vector_arr)
    a=pred[0][0]
    result=''
    if a>=0.5:
        result='긍정'
    else:
        result='부정'
    return render_template('text/result.html', result=result,rate='{:.2f}%'.format(a*100),review=text)

if __name__=='__main__':
    app.run(port=8000,threaded=False)