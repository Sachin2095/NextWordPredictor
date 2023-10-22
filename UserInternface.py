from flask import Flask , render_template,request
from keras.models import load_model
import pickle
model=load_model('next_word_predictor.h5')
app=Flask('__main__')
def preprocess(input_text):
    import numpy as np 
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    import tensorflow as tf
    import pickle
    from tensorflow.keras.preprocessing.text import  Tokenizer
    #import list for word indexes
    with open("test","rb") as rp:
        tok_word=pickle.load(rp)
    with open("tokenizer.pkl","rb") as rp:
        tok=pickle.load(rp)
    # tokenize 
    text=input_text
    token_text=tok.texts_to_sequences([text])[0]
    # padding 
    padded_token_text=pad_sequences([token_text],maxlen=101,padding='pre')
    # predict 
    top_indices = np.argsort(model.predict(padded_token_text)[0])[-3:][::-1]

    top_indices.sort()
    i=0
    predict_words=[]
    for word,index in tok_word.items():
        
        if index==top_indices[i] :
            predict_words.append(word)
            i+=1
            if(i==3):
                break
    return predict_words

@app.route('/home',methods=['GET','POST'])
def  home():
    if request.method=="GET":
       return  render_template('Home.html')
    else:
        input_text=request.form['inputs']
        words=preprocess(input_text)
        return  render_template('Home.html',first_word=input_text+" "+words[0],second_word=input_text+" "+words[1],third_word=input_text+" "+words[2])

if __name__=="__main__":
    app.run(debug=True)
