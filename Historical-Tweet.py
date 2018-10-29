import got3 as tweetory
import datetime
import csv


# This small program makes use of got3 library to retrieve historical twitter data for specific tags or handle which we can then save to a csv. The data can then later be used for training models to
# identify new exchange listings, spam tweets and important news using different classifiers.
def toCSV(t, fl):
    with open(fl, "w+", encoding="utf-8", newline="") as file:
        write = csv.writer(file)
        write.writerow(["Date", "ID", "Tweet", "Retweets",
                        "Favorites", "Mentions", "Hashtags"])
        for item in t:
            row = [item.date.strftime("%Y-%m-%d %H:%M"), item.id, item.text,
                   item.retweets, item.favorites, item.mentions, item.hashtags]
            write.writerow(row)
        print("Complete")
        file.close()


#query = input("What username do you want to use? ")
#fl = input("What filename do you want to use? ")

twitter_handles = ["coinbase", "binance", "OKEx_", "BithumbOfficial", "GeminiDotCom", "cryptopia_NZ", "KuCoincom",
                   "BittrexExchange", "Bitfinex", "UPBitExchange", "huobicom", "Huobi_Pro", "hitbtc", "BitZExchange", "gate_io", "LBank_Exchange"]

search = ["altcoin"]
for handle in twitter_handles:
    tweetCriteria = tweetory.manager.TweetCriteria(
    ).setQuerySearch(handle).setSince("2018-10-27")
    tweet = tweetory.manager.TweetManager.getTweets(tweetCriteria)
    fl = handle + "_historical.csv"
    toCSV(tweet, fl)
