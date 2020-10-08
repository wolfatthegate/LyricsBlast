import TextCleaner
import pymongo
import nltk
import blast
import sys
import Normalizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from gensim.parsing.preprocessing import remove_stopwords
from collections import Counter
from datetime import datetime
   
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
cleaner = TextCleaner.TextCleaner()
normalizer = Normalizer.Normalizer()
 
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
 
mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']
 
myquery = {}
totalTweet = lyricTbl.find(myquery).count()
 
x = 0
count_all = Counter()

while x < 10983:
    for mydoc in lyricTbl.find(myquery).skip(x).limit(5): #find() method returns a list of dictionary
        saveLyrics = ''
        try:
            song = mydoc['lyrics3']
            for line in song.splitlines(): 
                found = False 
                line = line.lower().replace(',', ' ')
                line = line.lower().replace('.', ' ')
                normalizedLine = normalizer.normalize(line)
                saveLyrics = saveLyrics + '\n' + normalizedLine 
                 
        except:
            print("An exception occurred at x: " + str(x) + " song name: " + mydoc['title'])
         
        updatequery = {'_id': mydoc['_id']}
        newvalue = { '$set': {'lyrics4': saveLyrics}}
        lyricTbl.update_one(updatequery, newvalue)
         
    x = x + 5  
    if(x==5665):
        x = 5675

print(now.strftime("%Y-%m-%d %H:%M:%S"))