import os
import csv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sklearn.feature_extraction.text as features

class classifier():
    def __init__(self,is_file=False,path='.'):
        #Load default variables and validate the passed path for either path or directory and then initialize the data loader.
        self.original_dir = os.getcwd()
        self.stop = set(stopwords.words('english'))
        self.lemm = WordNetLemmatizer()
        self.documents = []
        self.tokenized_document = []
        if(is_file and os.path.isfile(path) or not is_file and os.path.isfile(path)):
            print("Loading data from file: %s" % path)
            self.load_and_toke(path,True)
        elif(is_file and os.path.isdir(path)):
            q = input("Expected a file but received a directory. Would you like to continue y/n")
            if( q == 'y'):
                print("Loading text from files in directory: %s" % path)
                self.load_and_toke(path,False)
            else:
                print ("Failed to load data. Reload class with (is_file:bool,path:str)")
                self.data_is_loaded = False
        else:
            print("Loading text from files in directory: %s" % path)
            self.load_and_toke(path,False)

    def load_and_toke(self,path, is_file):
        #local function to read the  files
        def file_reader(name):
            with open(file=name,mode='r',encoding='UTF-8',newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if(row[2] == 'Listings'):
                        continue
                    else:
                        #For reach row of text create list of words that aren't stop words and lemmatize each word.
                        words = [(self.lemm.lemmatize(word.lower())) for word in row[3].split(" ") if self.lemm.lemmatize(word.lower()) not in self.stop and word.isalnum()]
                        self.tokenized_document += words
                        self.documents.append(row[3])
        #if its a file no need to change directories just call the file_reader and then store the results to the class object variables.
        if(is_file == True):
            file_reader(path)
            self.data_is_loaded = True
        else:
        #We're a directory so change to the directory and then loop through each document and call file-reader each time.
            print("Changing working directory to: %s" % path)
            os.chdir(path)
            print("Files in directory to be loaded:")
            file_list = os.listdir()
            print(file_list)
            for file in file_list:
                file_reader(file)
            self.data_is_loaded = True
    
    def count_vectorizer(self):
        vectorizer = features.CountVectorizer()
    
    def tf_idf_vectorizer(self):
        vectorizer = features.TfidfVectorizer()
