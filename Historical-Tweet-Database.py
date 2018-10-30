# Script to scrape,download and store twitter data into a MongoDB database. The data will be used to feed ML algoirthms and analyze sentiment, spamd and other analysis.

import got3 as tweetory
import datetime
from calendar import monthrange
from dateutil.relativedelta import *
import mongoengine as mongo
from textblob import TextBlob

# Schema class for Tweet data to be used with MongoDB


class Random(mongo.Document):
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
    polarity = mongo.FloatField()
    subjectivity = mongo.FloatField()


# Gives us the date of the last day in the month to be used with providing a date range to GetOldTweets library


def month_end(date):
    end_date = monthrange(date.year, date.month)[1]
    return datetime.date(date.year, date.month, end_date)

# stores data into a Schema and saves it into MongoDB. The data is the typical tweet data that can be gathered from scraping like username, likes, retweets etc... Additionally we use Textblob to store the sentiment on the tweet.
# We're storing sentiment now because even when we do the spam classification we still want the sentiment as extra information. Spam is still data!


def store_data(tweet_list, term):
    for tweet in tweet_list:
        chirp = Random()
        # not best practice but we're going to direclty change the collection name so we're storing to unique collections based off of the search term.
        chirp.switch_collection(term)
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

        sentiment = TextBlob(chirp.tweet)

        chirp.polarity = sentiment.sentiment.polarity
        chirp.subjectivity = sentiment.sentiment.subjectivity

        chirp.save()


mongo.connect("twitter")
today = datetime.date.today()
start_date = datetime.date(2015, 1, 1)
date_delta = relativedelta(months=+1)

search = ["bitcoin", "altcoin", "cryptocurrency", "blockchain", "DAO", "dApp", "decentralized app", "digital asset", "cryptotokens", "cryptoassets", "consensus", "masternode", "mooning",
          "proof of stake", "proof of work", "pump and dump", "satoshi", "satoshi nakamoto", "shilling", "solidity", "the dao", "tokenized", "digital economy", "crypto whale", "white paper", "airdrop"]

# For each term loop through each month and pull the historical data by scraping twitter data using GetOldTweets library.
for term in search:
    while ((start_date.year, start_date.month) != (today.year, today.month)):
        since = start_date.isoformat()
        until = month_end(start_date).isoformat()
        print(
            f"Retrieving tweets for keyword {term.upper()} between {since} and {until}")
        tweetCriteria = tweetory.manager.TweetCriteria(
        ).setQuerySearch(term).setSince(since).setUntil(until).setMaxTweets(1).setLang("en")
        tweet_list = tweetory.manager.TweetManager.getTweets(tweetCriteria)
        print("Tweets retrieved storing into database . . .")
        store_data(tweet_list, term)
        start_date = start_date + date_delta

    print(f"All tweets stored for {term.upper()}...\nContinuing...")
    # reset start_date back to original value if not the while loop will not initiate on the next for loop.
    start_date = datetime.date(2015, 1, 1)

print("All search terms saved...\nExiting...\nGoodbye.")
