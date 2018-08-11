import nltk
import os
import csv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
stop = set(stopwords.words('english'))
lemm = WordNetLemmatizer()

class classifier ():

    def __init__(self,testing_path:str,training_path:str):
        self.testing_path = os.path.abspath(testing_path)
        self.training_path = os.path.abspath(training_path)
        self.training_data_words = []
        self.training_data_texts = []
        self.create_data(self.training_path)


    def create_data(self,path):
        os.chdir(path)
        if(os.getcwd() == path):
            training_files = os.listdir(".")
            for fl in training_files:
                with open(file=fl,mode='r',encoding='UTF-8',newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if(row[2] == 'Listings'):
                            continue
                        else:
                            words = [lemm.lemmatize(word) for word in row[3].split(" ") if lemm.lemmatize(word) not in stop and word.isalnum()]
                            tweet = [words,row[2]]
                            self.training_data_words += words
                            self.training_data_texts.append(tweet)
                csvfile.close()
            self.training_data_words = nltk.FreqDist(self.training_data_words)
            self.word_features = list(self.training_data_words.keys())[:300]
            self.featuresets = [(self.find_features(words), tag) for (words, tag) in self.training_data_texts]
        else:
            print("Error with directory. Data not loaded.")
    
    def find_features(self,text):
        words = set(text)
        features = {}
        for word in self.word_features:
            features[word] = (word in words)
        return features

    def naive_bayes(self):
        training_set = self.featuresets
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print (classifier)
        accuracy =(nltk.classify.accuracy(classifier, training_set))*100
        return accuracy
