import TextCleaner
import pymongo
import nltk
import blast
import sys
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from gensim.parsing.preprocessing import remove_stopwords
from collections import Counter

cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
lyricTbl = mydb['MechTurk_Test']

myquery = {}
totalTweet = lyricTbl.find(myquery).count()

current_line = ''
previous_line = ''
future_line = ''
found = False

stop_words = set(stopwords.words('english')) 

x = 0
count_all = Counter()

while x < 653:
    for mydoc in lyricTbl.find(myquery).skip(x).limit(5): #find() method returns a list of dictionary
        tweet = mydoc['data']
        tweet = cleaner.clean(tweet)
#         word_tokens = word_tokenize(tweet)   
#         word_tokenized_ = [w for w in word_tokens if not w in stop_words] 

        filtered_sentence_ = remove_stopwords(tweet.lower())      
        word_tokens_gen = word_tokenize(filtered_sentence_)     
        
        
        count_all.update(word_tokens_gen)

    x = x + 5  
    
most_common_list = count_all.most_common(1000)
for el in most_common_list:
    print (el)
              
                