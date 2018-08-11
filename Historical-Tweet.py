import got3 as tweetory
import datetime
import csv

def toCSV(t,fl):
	with open(fl, "w+",encoding="utf-8",newline="") as file:
		write = csv.writer(file)
		write.writerow(["Date","ID","Tweet","Retweets","Favorites","Mentions","Hashtags"])
		for item in t:
			row = [item.date.strftime("%Y-%m-%d %H:%M"),item.id,item.text,item.retweets,item.favorites,item.mentions,item.hashtags]
			write.writerow(row)
		print("Complete")
		file.close()


#query = input("What username do you want to use? ")
#fl = input("What filename do you want to use? ")

twitter_handles = ["coinbase", "binance", "OKEx_", "BithumbOfficial", "GeminiDotCom", "cryptopia_NZ", "KuCoincom", "BittrexExchange", "Bitfinex", "UPBitExchange", "huobicom", "Huobi_Pro", "hitbtc", "BitZExchange", "gate_io", "LBank_Exchange"]
print (twitter_handles)
for handle in twitter_handles:
   tweetCriteria = tweetory.manager.TweetCriteria().setUsername(handle).setSince("2018-02-01")
   tweet = tweetory.manager.TweetManager.getTweets(tweetCriteria)
   fl = handle + "_historical.csv"
   toCSV(tweet,fl)
