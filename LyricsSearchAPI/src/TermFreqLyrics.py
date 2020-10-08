import TextCleaner
import pymongo
import nltk
import blast
import sys
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from gensim.parsing.preprocessing import remove_stopwords
from collections import Counter

terms = ['heroin', 'heroine', 'oxy', 'dopamine', 'norepinephrine',
             'weed','cocaine', 'lean', 'blunt', 'joint', 'dank',
             'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette',
             'smoking', 'smokin', 'pour', 'xan']
   
cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']

myquery = {}
totalTweet = lyricTbl.find(myquery).count()

current_line = ''
previous_line = ''
future_line = ''
found = False

stop_words = set(stopwords.words('english')) 

x = 0
count_all = Counter()


while x < 10983:
    for mydoc in lyricTbl.find(myquery).skip(x).limit(5): #find() method returns a list of dictionary
        try:
            song = mydoc['lyrics3']
            for line in song.splitlines(): 
                found = False 
                line = cleaner.clean(line)

#         word_tokens = word_tokenize(tweet)   
#         word_tokenized_ = [w for w in word_tokens if not w in stop_words] 
        
                filtered_sentence_ = remove_stopwords(line.lower())      
                word_tokens_gen = word_tokenize(filtered_sentence_)     
                 
                for token in word_tokens_gen: 
                    for term in terms: 
                        if term == token:
                            found = True
                 
                if found == True:
                    count_all.update(word_tokens_gen)
        except:
            print("An exception occurred at x: " + str(x) + " song name: " + mydoc['title'])

    x = x + 5  
    if(x==5665):
        x = 5675
print('search done')    
most_common_list = count_all.most_common(4000)
for el in most_common_list:
    print (el)
              
print('print done')