#  https://basicdashflask.herokuapp.com/
from flask import *
import requests     
import tweepy
from textblob import TextBlob
from tweepy import user

server = Flask(__name__, template_folder='static')

# Landing page/Home page
@server.route('/',methods=['GET'])
def landing_page():
    return render_template('index.html')

# IndiaCovidDetails
@server.route('/India_details',methods=['GET'])
def hello_html():
    return render_template('mapmyindia.html')

# GlobalData->Total Cases
@server.route('/total_cases',methods=['GET'])
def new_page_option1():
    return render_template('total_cases.html')

# GlobalData->New Cases
@server.route('/new_cases',methods=['GET'])
def new_page_option2():
    return render_template('new_cases.html')

# GlobalData->New Deaths
@server.route('/new_deaths',methods=['GET'])
def new_page_option3():
    return render_template('new_deaths.html')

# GlobalData->Total Deaths
@server.route('/total_deaths',methods=['GET'])
def new_page_option4():
    return render_template('total_death.html')

# Search for news
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


# Search for covid news
@server.route('/covid_news',methods=['POST'])
def covidnewssearch():
    # Fetching news from the api and passing parameters
    query_text = request.form['search_covid_news'] # getting the keyword entered
    url = 'https://newsapi.org/v2/everything?'  # api
    parameters = {                               # parameters needed to be passed with the api 
        'q': query_text, # query phrase
        'pageSize': 95,  # maximum is 100
        'apiKey': '59730df608f440e58b7a56471582216e' # your own API key
    }
    response = requests.get(url, params=parameters)     # reponse from the api
    response_json = response.json()                     # converting the data into json
    res = []                                            # list to store data about each news article
    senti = []                                          # list to store setiments of each news articles

    # Running a loop over the fetched news to find the covid keywords in the news 
    for i in range(len(response_json['articles'])):
        # Searching in each news for covid/Covid/Corona/COVID/Corona keywords
        case1 = response_json['articles'][i]['title'].find('covid')
        case2 = response_json['articles'][i]['title'].find('Covid')
        case3 = response_json['articles'][i]['title'].find('corona')
        case4 = response_json['articles'][i]['title'].find('Corona')
        case5 = response_json['articles'][i]['title'].find('COVID')
        blob = TextBlob(str(response_json['articles'][i]['description'])) #passing the text to textblob for sentiment analysis

        if(case1!=-1):                            # If news contains keyword covid do the sentiment analysis and append to senti array
            res.append(response_json['articles'][i]) 
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case2!=-1):                            # If news contains keyword Covid do the sentiment analysis and append to senti array
            res.append(response_json['articles'][i]) 
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case3!=-1):                            # If news contains keyword corona do the sentiment analysis and append to senti array
            res.append(response_json['articles'][i]) 
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case4!=-1):                            # If news contains keyword Corona do the sentiment analysis and append to senti array
            res.append(response_json['articles'][i])
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
        if(case5!=-1):                            # If news contains keyword COVID do the sentiment analysis and append to senti array
            res.append(response_json['articles'][i])  
            if(blob.sentiment.polarity >0):
                senti.append("positive")
            elif(blob.sentiment.polarity <0):
                senti.append("negative")
            else:
                senti.append("neutral")
    
    # If number of news with the covid related keywords < 10 then appending with random news related to the keyword entered to make the total number of new to 10 
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
    return render_template('news_page.html',arr=res,senti=senti)       # Passing the lists res and senti to frontend i.e news_page.html


# Search for tweets
@server.route('/tweets',methods=['POST'])
def tweets_searchbar():
    query_text = request.form['search_tweets'] # Fetch the keywords entered
    query = query_text                          # Keyword
    client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAI4MXgEAAAAAF6mhobDFen97C4OvxCuGGDqc9c8%3DH60ut0wyJvExe8XYJ3yeqMpLSJJ9UgXhCaePBGa3RfMMURvtL7") # Authentication
    tweets = []                                 #List to store the tweet text
    names = []                                  #List to store the name of the person
    usernames = []                              #List to store the username
    urls = []                                   #List to store the url of the tweet
    response = client.search_recent_tweets(query=query,max_results=100,tweet_fields=['created_at','lang'],expansions='author_id')
    for i in range(min(len(response.includes['users']),len(response.data))):
        if response.data[i].lang == 'en':
            text = response.data[i].text         # Tweet text
            tweets.append(text)                  # Appending the tweet text to list
            names.append(response.includes['users'][i].name)     # Appending the name of the user to list
            usernames.append(response.includes['users'][i].username)       # Appending the username of the user text to list
            urls.append("https://twitter.com/twitter/statuses/"+str(response.data[i].id))           #Creating a link to the tweet using tweet id
    return render_template('tweet_result.html',tweets=tweets,names=names,usernames=usernames,urls=urls)    # Passing the lists to frontend i.e tweet_result.html  


if __name__ == '__main__':
    # server.debug = True
    server.run()
