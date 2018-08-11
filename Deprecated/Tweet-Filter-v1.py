import os
import csv
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
class classifier:

    def __init__(self,directory_path:str):
        self.directory_path = directory_path
        self.total = 0
        self.is_spam = 0
        self.trainPositive = {}
        self.positiveTotal = 0
        self.trainNegative = {}
        self.negativeTotal = 0

    #runs once on training data
    def train(self):
        os.chdir(self.directory_path)
        training_files = os.listdir(".")
        for fl in training_files:
            with open(file=fl,mode='r',encoding='UTF-8',newline='') as csvfile:
                listing_reader = csv.reader(csvfile)
                for row in listing_reader:
                    if(row[2] == 'Listings'):
                        continue
                    elif row[2] == 'TRUE':
                        self.is_spam  += 1
                    self.total += 1
                    self.process_text(row[3],row[2])
            csvfile.close()
        self.pA = self.is_spam/float(self.total)
        self.pNotA = (self.total - self.is_spam)/ float(self.total)
    
    #counts the words in a specific email
    def process_text(self,body,label):
        text = [word for word in body.split(" ") if word not in stop and word.isalnum()]
        for word in text:
            if label == "TRUE":
                self.trainPositive[word] = self.trainPositive.get(word, 0) + 1
                self.positiveTotal += 1
            else:
                self.trainNegative[word] = self.trainNegative.get(word, 0) + 1
                self.negativeTotal += 1
    
    #gives the conditional probability p(B_i | A_x)   
    def conditional_word(self,word, boolean):
        if boolean:
            return (self.trainPositive.get(word,0)+1)/float(self.positiveTotal)
        else:
            return (self.trainNegative.get(word,0)+1)/float(self.negativeTotal)
   
    #gives the conditional probability p(B | A_x)
    def conditional_text(self,body, boolean):
        result = 1.0
        for word in body:
            result *= self.conditional_word(word,boolean)    
        return result

    #classifies a new email as spam or not spam
    def classify(self,text_body):
        text_body = [word for word in text_body.split(" ") if word not in stop and word.isalnum()]
        isClassifier = self.pA * self.conditional_text(text_body, True) # P (A | B)
        notClassifier = self.pNotA * self.conditional_text(text_body, False) # P(¬A | B)
        result = isClassifier > notClassifier
        return 
        

class nGramm(classifier):
    def __init__(self):
        print("New class made")
    def unique_to_nGramm (self):
        print ("Unique to NGRAM!!!")