# Crypto-Tweet

Annoyed by the constant spam of bots in Crypto Twitter I created this project. The aim is to use the same Spam Filtering techniques (text classification) to sort out the bot tweets and get a clean stream of authentic tweets. I approached this project from multiple angles the first being a raw implementation of Naive Bayes classicization as seen in the Deprecated folder. Each version thereafter was a refactoring with additional elements added to improve classification i.e. better tokenizing, vectorizing, and lemmatization of words.
The most current version v4 was the best with a typical accuracy around 85% and took the knowledge from the previous versions and implemented the [SciKit-Learn]( http://scikit-learn.org/stable/) library in order to create a pipeline for handling the cleaning of the data strings, lemmatizing, vectorizing, splitting up the data into k-folds and then outputting the appropriate stats for measuring accuracy.
Data for the project was pulled using Jefferson-Henrique’s [GetOldTweets-python]( https://github.com/Jefferson-Henrique/GetOldTweets-python) library. I created my own wrapper to output the data as needed into a csv. The tweet data then had to be manually classified into spam and not spam so it could be used appropriately by the text classification algorithm.

## Improvements
There is still a lot of room to improve accuracy. The tokenizing, lemmatizing and vectorizing could be improved with a better dataset. Better features can be added into the algorithm that could account for likes, comments, account age, and or account followers all of which can be used to identify spam. Also other classifications beyond Naïve Bayes could be used for potentially better results.
The next iteration would definitely take the above into account.

# Built With

* [Python](https://www.python.org/)
* [SciKit-Learn]( http://scikit-learn.org/stable/)
* [GetOldTweets-python]( https://github.com/Jefferson-Henrique/GetOldTweets-python)
* [Natural Language toolkit](https://www.nltk.org/)
