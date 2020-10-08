import TextCleaner
import pymongo
import nltk
import blast
import sys
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from gensim.parsing.preprocessing import remove_stopwords

cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
lyricTbl = mydb['MechTurk']

myquery = {}
totalTweet = lyricTbl.find(myquery).count()

current_line = ''
previous_line = ''
future_line = ''
found = False

stop_words = set(stopwords.words('english')) 

x = 0
while x < 653:
    for mydoc in lyricTbl.find(myquery).skip(x).limit(5): #find() method returns a list of dictionary
        tweet = mydoc['data']
        tweet = cleaner.clean(tweet)
        word_tokens = word_tokenize(tweet) 
        
        word_tokenized_ = [w for w in word_tokens if not w in stop_words] 

        filtered_sentence_ = remove_stopwords(tweet.lower())      
        word_tokens_gen = word_tokenize(filtered_sentence_)      
        with open('archived_tweets/tokens_test.txt', 'a') as f: 
            f.write(tweet + '\n') 
            f.write(str(word_tokenized_) + '\n')
            f.write(str(word_tokens_gen) + '\n')
            f.write('\n')
    x = x + 5  
            
                