#  https://basicdashflask.herokuapp.com/
from flask import *
import requests     
import tweepy
from textblob import TextBlob
from tweepy import user

server = Flask(__name__, template_folder='static')

@server.route('/dash',methods=['GET'])
def hello():
    return redirect('sentiment')

@server.route('/',methods=['GET'])
def hello_html():
    return render_template('mapmyindia.html')

@server.route('/total_cases',methods=['GET'])
def new_page_option1():
    return render_template('total_cases.html')

@server.route('/new_cases',methods=['GET'])
def new_page_option2():
    return render_template('new_cases.html')

@server.route('/new_deaths',methods=['GET'])
def new_page_option3():
    return render_template('new_deaths.html')

@server.route('/total_deaths',methods=['GET'])
def new_page_option4():
    return render_template('total_death.html')

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
    return render_template('news_page.html',arr=res,senti=senti)

@server.route('/tweets',methods=['POST'])
def tweets_searchbar():
    query_text = request.form['search_tweets']
    query = query_text
    client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAI4MXgEAAAAAF6mhobDFen97C4OvxCuGGDqc9c8%3DH60ut0wyJvExe8XYJ3yeqMpLSJJ9UgXhCaePBGa3RfMMURvtL7")
    tweets = []
    names = []
    usernames = []
    response = client.search_recent_tweets(query=query,max_results=100,tweet_fields=['created_at','lang'],expansions='author_id')
    for i in range(len(response.data)):
        if response.data[i].lang == 'en':
            text = response.data[i].text
            if(text[0:2]=='RT'):
                idx = text.find(':')
                text = text[idx+1:]
            tweets.append(text)
            # names.append(response.includes['users'][i].name)
            # usernames.append(response.includes['users'][i].username)
    return render_template('tweet_result.html',tweets=tweets)


if __name__ == '__main__':
    # server.debug = True
    server.run()
