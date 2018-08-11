import pandas as pd

from nltk.corpus import stopwords as sw
from nltk import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split as tts
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate

class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.lower = True
        self.strip = True
        self.stopwords = set(sw.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def fit(self, X, y=None):
        return self
    
    def inverse_transform(self,X):
        return self
    
    def transform(self,X):
        return [self.tokenize(tweet) for tweet in X]
    
    def tokenize(self, tweet):
        tweet = tweet.lower()
        token = [self.lemmatizer.lemmatize(word) for word in tweet.split(" ") if word not in self.stopwords and word.isalnum()]
        return token
def identity(arg):
    #passthrough function
    return arg
def build_and_evaluate(body,tag,outpath=None):
    def build(body,tag):
        model = Pipeline([
            ('preprocessor', Preprocessor()),
            ('vectorizer', TfidfVectorizer(sublinear_tf=True,min_df=5,norm='l2',tokenizer=identity, preprocessor=None, lowercase=False)),
            ('classifier', MultinomialNB()),
        ])
        model.fit(body,tag)
        return model


    print("Encoding labels. . .")
    labels = LabelEncoder()
    tags = labels.fit_transform(tag)

    print("Spitting training and testing data set . . .")
    body_train, body_test, tag_train, tag_test = tts(body,tags)
    print("Building model . . .")
    model = build(body_train, tag_train)

    print("Classification report:\n")
    y_prediction = model.predict(body_test)
    results = clsr(tag_test,y_prediction,target_names=labels.classes_)
    print (results)

    #Let's use Cross Validation and the GridSearch to see if we can improve upon our accuracy.
    #Define the paramaters to be fine tuned
    paramaters = {
        'vectorizer__sublinear_tf': (True, False),
        'vectorizer__min_df': (4,5,7,10),
        'classifier__alpha':(0.5,0.2,0.1,0.01,0.001)
    }

    #Create the GridSearchCV from our existing model
    grid_search = GridSearchCV(model,paramaters,cv=5, n_jobs=-1)
    grid_search.fit(body_train,tag_train)
    #GridSearch returns a cv_results paramater but also has several best_ attributes that aren't included in the cv_result dictionary. Lets make our own dic.
    data = {
        "best_estimator":grid_search.best_estimator_,
        "best_score":grid_search.best_score_,
        "best_index":grid_search.best_index_,
        "best_params":grid_search.best_params_,
    }

    # #lets print out the results and take a look at how we're doing
    # print("The best params:")
    # print(data)
    # print("The Cross validation Result:")
    # print(grid_search.cv_results_)

    # #Double check performance with the testing porition of our data set.
    # tag_real, body_predict = tag_test, grid_search.predict(body_test)
    
    # result = clsr(tag_real,body_predict)
    # print (result)

    #We have the optimal paramaters so lets grab the best estimator and refit it to the full data set and retest accuracy.
    model = grid_search.best_estimator_
    tag_real, body_predict = tag_test, grid_search.predict(body_test)
    
    result = clsr(tag_real,body_predict)
    print (result)

    return model




if __name__ == "__main__":
    PATH = "model.pickle"
    data_file = pd.read_csv("./aggregateddata.csv")
    body = data_file["Tweet"].tolist()
    tag = data_file["Category"].tolist()
    
    model = build_and_evaluate(body,tag,outpath=PATH)