#  https://basicdashflask.herokuapp.com/
from flask import *
import torch
from transformers import BertTokenizer, BertModel
import matplotlib.pyplot as plt
# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
import pandas as pd
import numpy as np
import re
import string
import requests     
import json
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('brown')
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from dashboard.sentiment import create_sentiment_application

server = Flask(__name__, template_folder='static')

create_sentiment_application(server)

df=pd.read_csv('covid19_tweets.csv')
df=df.rename(columns={'text':'tweet'})
documents=pd.DataFrame(df['tweet'][0:100])
def pre_process(tweet):
    tweet = re.sub(r'\$\w*', '', tweet)
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    tweet = re.sub(r'#', '', tweet )
    tweet = re.sub(r'\n', ' ', tweet )
    #tweet = re.sub(r'@', '', tweet )
    tweet=' '.join(word for word in tweet.split(' ') if not word.startswith('@'))        
    return tweet

processed_docs = documents['tweet'].map(pre_process)
documents['processed_tweets']=processed_docs

def isNotBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return True
        #myString is None OR myString is empty or blank
    return False
    
model = BertModel.from_pretrained('bert-base-uncased',
                                 output_hidden_states = True, # Whether the model returns all hidden-states.
                                 )

    #Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()

data=pd.DataFrame()
def get_embeddings(text):
    marked_text = "[CLS] " + text + " [SEP]"
    tokenized_text = tokenizer.tokenize(marked_text) 
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = [1] * len(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2]
    token_embeddings = torch.stack(hidden_states, dim=0)
    token_embeddings.size()
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings.size()
    token_embeddings = token_embeddings.permute(1,0,2)
    token_embeddings.size()
    token_vecs_sum = []
    a=np.zeros(shape=(len(token_embeddings),768))
    for i in range(0,len(token_embeddings)):
        sum_vec = torch.sum(token_embeddings[i][-4:], dim=0)
        token_vecs_sum.append(sum_vec)
        a[i]=sum_vec
    a=np.average(a,axis=0)
    return a

documents['embeddings']=documents['processed_tweets'].apply(lambda x: get_embeddings(x))
# from scipy.spatial.distance import cosine
def cosine_similarity(x,y):
    similarity = cosine(x,y)
    return similarity
    
# query='covid active cases'
# embedding=get_embeddings(query)
# documents['similarity']=documents['embeddings'].apply(lambda x: cosine_similarity(x,embedding))
# documents=documents.sort_values(by=['similarity'],ascending=False).reset_index()
# module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
# model = hub.load(module_url)
# sentences=processed_docs
# sentence_embeddings = model(sentences)
# query = "myanmar"
# query_vec = model([query])[0]
# for sent in sentences[0:5]:
#     sim = cosine(query_vec, model([sent])[0])
# sentence_embeddings = model(sentences)
# query = "covid latest update"
# query_vec = model([query])[0]
# data=pd.DataFrame()
# for sent in sentences[0:5]:
#     sim = cosine(query_vec, model([sent])[0])
#     data=data.append({'text':sent,'similarity':sim},ignore_index=True)
# data=data.sort_values(by=['similarity'],ascending=False).reset_index()
# sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
# sentence_embeddings = sbert_model.encode(sentences)

# from dashboard.dash1 import create_dash1_application
# create_dash1_application(server)

@server.route('/dash',methods=['GET'])
def hello():
    return redirect('sentiment')


@server.route('/',methods=['GET'])
def hello_html():
    return render_template('mapmyindia.html')

# @server.route('/new',methods=['POST'])
# def new_page():
#     return render_template('total_cases.html')

@server.route('/total_cases',methods=['GET'])
def new_page_option1():
    return render_template('total_cases.html')

# @server.route('/India',methods=['GET'])
# def India_details():
#     return render_template('mapmyindia.html')

@server.route('/new_cases',methods=['GET'])
def new_page_option2():
    return render_template('new_cases.html')

@server.route('/new_deaths',methods=['GET'])
def new_page_option3():
    return render_template('new_death.html')

@server.route('/total_deaths',methods=['GET'])
def new_page_option4():
    return render_template('total_deaths.html')

@server.route('/news',methods=['POST'])
def newssearch():
    query_text = request.form['search_news']
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': query_text, # query phrase
        'pageSize': 95,  # maximum is 100
        'apiKey': '59730df608f440e58b7a56471582216e' # your own API key
    }
    senti = []
    response = requests.get(url, params=parameters)
    response_json = response.json()
    res = response_json['articles']
    for i in range(len(res)):
        blob = TextBlob(str(res[i]['description']))
        if(blob.sentiment.polarity >0):
            senti.append("positive")
        elif(blob.sentiment.polarity <0):
            senti.append("negative")
        else:
            senti.append("neutral")
    return render_template('news_page.html',arr=res,senti=senti)

@server.route('/covid_news',methods=['POST'])
def covidnewssearch():
    query_text = request.form['search_covid_news']
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': query_text, # query phrase
        'pageSize': 95,  # maximum is 100
        'apiKey': '59730df608f440e58b7a56471582216e' # your own API key
    }
    response = requests.get(url, params=parameters)
    response_json = response.json()
    res = []
    senti = []

    for i in range(len(response_json['articles'])):
        case1 = response_json['articles'][i]['title'].find('covid')
        case2 = response_json['articles'][i]['title'].find('Covid')
        case3 = response_json['articles'][i]['title'].find('corona')
        case4 = response_json['articles'][i]['title'].find('Corona')
        case5 = response_json['articles'][i]['title'].find('COVID')
        blob = TextBlob(str(response_json['articles'][i]['description']))

        if(case1!=-1):
            res.append(response_json['articles'][i]) 
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case2!=-1):
            res.append(response_json['articles'][i]) 
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case3!=-1):
            res.append(response_json['articles'][i]) 
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case4!=-1):
            res.append(response_json['articles'][i])
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case5!=-1):
            res.append(response_json['articles'][i])  
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
    # print(res)
    # res = json.dumps(res)
    if len(res)<10:
        left = 10-len(res)
        for i in range(left):
            res.append(response_json['articles'][i])
            blob = TextBlob(response_json['articles'][i]['description'])
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
    # return render_template('latest_news_page.html',arr=res)
    return render_template('news_page.html',arr=res,senti=senti)
    # return res

# Convert the response to JSON format and pretty print it
# response_json = response.json()

@server.route('/tweets',methods=['POST'])
def searchbar():
    query_text = request.form['search_tweets']
    query = query_text
    # query_vec = sbert_model.encode([query])[0]
    # data=pd.DataFrame()
    # for sent in sentences:
    #     sim = cosine(query_vec, sbert_model.encode([sent])[0])
    #     data=data.append({'text':sent,'similarity':sim},ignore_index=True)
    
    # data=data.sort_values(by=['similarity'],ascending=False).reset_index()
    return render_template('tweet_result.html',tweet1 = data['text'][0],tweet2 = data['text'][1],tweet3 = data['text'][2],tweet4 = data['text'][3],tweet5 = data['text'][4])


if __name__ == '__main__':
    # server.debug = True
    server.run()
