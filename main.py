
import os #get the tweets from the twitter api
import tweepy #get the tweets from the twitter api
import dotenv #load the .env file
import pandas as pd #load the dataframe
import datetime as dt #get the date and time
import requests #get the date and time
import json #load the json file

dotenv.load_dotenv('credentials.env') #load the .env file
consumer_key = os.environ["API_KEY"] #load the consumer key
consumer_secret = os.environ["API_KEY_SECRET"] #load the consumer secret
access_token = os.environ["ACCESS_TOKEN"] #load the access token
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"] #load the access token secret

auth = tweepy.OAuth1UserHandler(
  consumer_key, 
  consumer_secret, 
  access_token, 
  access_token_secret
) #create an object for authentication

api = tweepy.API(auth) #create an object for the tweepy api



users = ['@elonmusk','@VitalikButerin','@adam3us', '@aantonop', '@CamiRusso',
'@AltcoinSara', '@cz_binance', '@TimDraper', '@saylor'] #list of users to be analyzed

columns = ['User', 'Tweet'] #column names for the dataframe
data = [] #create a dataframe with the user and tweet


for user in users: #for each user in the list of users
  tweets = tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode = "extended").items(10)  #get the tweets
  for tweet in tweets: #for each tweet in the user's timeline
    data.append([tweet.user.screen_name, tweet.full_text]) #create a dataframe with the user and tweet

df = pd.DataFrame(data, columns=columns) #create a dataframe with the user and tweet
print(df)

# put dataframe to a csv
df.to_csv('tweets.csv', index=False)

# do sentiment analysis on the tweets
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

#do sentiment analysis on the tweets
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))
    return score

# store the sentiment analysis scores in a list
scores = []
for i in range(len(df)):
    scores.append(sentiment_analyzer_scores(df['Tweet'][i]))

# add the scores to the dataframe
df['Sentiment'] = scores

# print the dataframe
print(df) # print the dataframe

# loop through the scores and print the ones that are positive
for i in range(len(df)):
    if df['Sentiment'][i]['compound'] > 0:
        print(df['Tweet'][i])
        print(df['Sentiment'][i])
        print("\n")
  
# loop through the scores and print the ones that are negative
for i in range(len(df)):
    if df['Sentiment'][i]['compound'] < 0:
        print(df['Tweet'][i])
        print(df['Sentiment'][i])
        print("\n")

# pull last 30 days btc price from coingecko


# get https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"
response = requests.get(url)
data = json.loads(response.text)

print ("Prices for the last 30 days: (in USD)")
for i in range(len(data['prices'])):
    print(data['prices'][i][0], data['prices'][i][1])