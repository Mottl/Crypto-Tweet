import got3 as tweetory
import datetime
from calendar import monthrange
from dateutil.relativedelta import *
import mongoengine as mongo


class Tweet(mongo.Document):
    tweet_id = mongo.IntField()
    permalink = mongo.StringField()
    date = mongo.DateTimeField()
    username = mongo.StringField()
    author_id = mongo.IntField()
    tweet = mongo.StringField()
    retweets = mongo.IntField()
    likes = mongo.IntField()
    comments = mongo.IntField()
    mentions = mongo.ListField(mongo.StringField())
    hashtags = mongo.ListField(mongo.StringField())
    cashtags = mongo.ListField(mongo.StringField())
    urls = mongo.ListField(mongo.StringField())


def month_end(date):
    end_date = monthrange(date.year, date.month)[1]
    return datetime.date(date.year, date.month, end_date)


def store_data(tweet_list):
    for tweet in tweet_list:
        chirp = Tweet()
        chirp.tweet_id = tweet.id
        chirp.permalink = tweet.permalink
        chirp.date = tweet.date
        chirp.username = tweet.username
        chirp.author_id = tweet.author_id
        chirp.tweet = tweet.text
        chirp.retweets = tweet.retweets
        chirp.likes = tweet.favorites
        chirp.comments = tweet.comments
        chirp.mentions = tweet.mentions
        chirp.hashtags = tweet.hashtags
        chirp.cashtags = tweet.cashtags
        chirp.urls = tweet.urls
        chirp.save()


mongo.connect("twitter")
today = datetime.date.today()
start_date = datetime.date(2015, 1, 1)
date_delta = relativedelta(months=+1)

search = ["bitcoin", "altcoin", "cryptocurrency", "blockchain"]

for term in search:
    while ((start_date.year, start_date.month) != (today.year, today.month)):
        since = start_date.isoformat()
        until = month_end(start_date).isoformat()
        print(
            f"Retrieving tweets for keyword {term.upper()} between {since} and {until}")
        tweetCriteria = tweetory.manager.TweetCriteria(
        ).setQuerySearch(term).setSince(since).setUntil(until)
        tweet_list = tweetory.manager.TweetManager.getTweets(tweetCriteria)
        print("Tweets retrieved storing into database . . .")
        store_data(tweet_list)
        print("Tweets stored. \n Continuing...")
        start_date = start_date + date_delta
