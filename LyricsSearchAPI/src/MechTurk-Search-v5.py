
# This is a working version Sep 28, 2020
# Normalizer is added to the program so that the tweet query can 
# match the database. 

import TextCleaner
import pymongo
import nltk
import blast
import sys
import concurrent.futures
import logging
import Normalizer
import re

from gensim.parsing.preprocessing import remove_stopwords
from datetime import datetime
# from spellchecker import SpellChecker

def printResult(result, songtitle, doc_id):

    logging.info('tweet: ' + result[0], extra={'_id': doc_id})
    logging.info('query: ' + result[1], extra={'_id': doc_id})
    logging.info('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + songtitle, extra={'_id': doc_id})
    logging.info(' first half score: ' + str(round(result[4], 2)), extra={'_id': doc_id})
    logging.info('second half score: ' + str(round(result[5], 2)), extra={'_id': doc_id})
    
    suggestions = 'tweet: ' + result[0] + '\n' + 'query: ' + result[1] + '\nScore: ' + \
                    str(round(result[2],2)) + '/1.0 \n(' + str(result[3]) + ' words matched)'
    
    return suggestions
 
def findDrugKeywords(str):
    
    terms = ['heroin', 'heroine', 'oxy', 'dopamine', 'norepinephrine',
             'weed','cocaine', 'lean', 'blunt', 'joint', 'dank',
             'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette',
             'smoking', 'smokin', 'pour', 'xan', 'crack in my crack']
    
    substract_terms = ['u', 'ex', 'help', 'th',
                       'dont', 'gon', 'na', 'hos', 'like', 
                       'before', 'im ', 'nigga', 'bieber', 'hand', 
                       'albany', 'people', 'diamonds', 'glow', 'aint', 
                       'run', 'bout', 'fun', 'comin']
    
    filtered_str = remove_stopwords(str)
    tokenized_str = nltk.word_tokenize(filtered_str)
    blaster = blast.blast()
    keywordList = []
    for tokenized_word in tokenized_str:
        for term in terms:      
            result = blaster.SMalignmentGlobal(tokenized_word.lower(), term.lower())
            if result[2] > 0.85:
                term = re.sub(r'ing$', 'in', term)
                keywordList.append(term.lower())   
    if keywordList:                       
        for word_token in tokenized_str: 
            if word_token.lower() not in substract_terms:  
#                 word_token = spell.correction(word_token)          
                word_token = re.sub(r'ing$', 'in', word_token)            
                keywordList.append(word_token.lower()) 
    keywordList = list(dict.fromkeys(keywordList))
#     print(keywordList)
    return keywordList

def findArtistName(tweet):
    artistList = ['young thug', 'coke boys']

    for artist in artistList:
        tweet = tweet.lower()               
        if (tweet.find(artist)!=-1):
            return artist
    return ''
    

def searchTweet(doc):
    tweet = doc['data']
    tweet = cleaner.clean(tweet)

    artistFound = findArtistName(tweet)
    if (artistFound != ''):
        now = datetime.now()
        updatequery = {'_id': doc['_id']}
        newvalue = { '$set': {'score': 1.00 , 'suggestions': 'artist found: ' + artistFound, 'song': '', 'found': "v3", 'x_add': now.strftime("%Y-%m-%d %H:%M:%S")}}
        logging.info('No keywords found in Tweet ', extra = {'_id': doc['_id']})
        testTbl.update_one(updatequery, newvalue)
        return 0
    # normalizer simplify the words 
    # that spelling checkers cannot handle.

    tweet = normalizer.normalize(tweet)
    query_list = findDrugKeywords(tweet)
    
    if not query_list:
        now = datetime.now()
        updatequery = {'_id': doc['_id']}
        newvalue = { '$set': {'score': 0.00 , 'suggestions': 'keywords not found', 'song': '', 'found': "v3", 'x_add': now.strftime("%Y-%m-%d %H:%M:%S")}}
        logging.info('No keywords found in Tweet ', extra = {'_id': doc['_id']})
        testTbl.update_one(updatequery, newvalue)
        return 0
    
    go_to_next_tweet = False
    titleMatched = False
    savedline = ''
    combined_lines = ''
    song = ''
    score = 0.00
    suggestions = ''
    
    keyword_list_title = []
    keyword_list_lyric = []
    
    for query_word in query_list:
        keyword_list_title.append({"title": {"$regex": query_word, "$options": "-i"}})
        keyword_list_lyric.append({"lyrics4": {"$regex": query_word, "$options": "-i"}})
    
    mytitlequery = {'$and': keyword_list_title}
    mytitle = lyricTbl.find(mytitlequery)
    
    if len(doc['data']) > 60:
        temp_str = doc['data'][0:60] + ' ... '
    else:
        temp_str = doc['data']
    
    logging.info(mytitlequery, extra = {'_id': doc['_id']})
    logging.info('searching for ' + temp_str + ' ' + str(mytitle.count()) + ' possible titles found.', extra = {'_id': doc['_id']})
    
    for eachtitle in mytitle: 
        title = cleaner.clean(eachtitle['title']) 
        
        result = blaster.SMWalignment(tweet.lower(), title.lower(), threshold)
            
        if round(result[2],2) > 0.70: 
            logging.info('title found', extra = {'_id': doc['_id']})
            titleMatched = True
            suggestions = suggestions + '\n' + printResult(result, eachtitle['title'], doc['_id'])   
            updatequery = {'_id': doc['_id']}
            newvalue = { '$set': {'score': round(result[2],2), \
                            'suggestions': suggestions, \
                                'song': eachtitle['title'], 'found': "v3"}}
            testTbl.update_one(updatequery, newvalue)
            break
    
    if titleMatched == True:
        return 0
      
    mylyricquery = {'$and': keyword_list_lyric} # query keyword
    mylyrics = lyricTbl.find(mylyricquery)  #find in lyrics database

    logging.info(mylyricquery, extra= {'_id': doc['_id']})
    logging.info(str(mylyrics.count()) + ' possible lyrics found.', extra= {'_id': doc['_id']})
        
    for eachlyrics in mylyrics: #loop through mylyrics list
        
        # initialize variables
        go_to_next_song = False  
        continue_test = False  
        followUp = False
        stepBack = False
        # read each line of lyrics  
        past_line_2 = ''
        past_line_1 = ''
        past_line_0 = ''
        combined_string = ''
        
        maxResult = 0
        maxMatch = 0
  
        for eachline in eachlyrics['lyrics4'].splitlines():
            
            eachline = cleaner.clean(eachline)
            
            past_line_2 = past_line_1
            past_line_1 = past_line_0
            past_line_0 = eachline
            
            combined_string = past_line_2 + ' ' + past_line_1 + ' ' + past_line_0
            for query_word in query_list:
                if query_word.lower() in combined_string.lower():
                    continue_test = True
                        
            if continue_test == True:
                followUp = False
                stepBack = False

                # perform blast Search                    
                result = blaster.SMWalignment(tweet, past_line_1.lower(), threshold)
                maxResult = result[2]
                maxMatch = result[3]
                    
                if result[6] == True:
                    followupLine = past_line_1 + ' ' + past_line_0
                    followUpResult = blaster.SMWalignment(tweet, followupLine.lower(), threshold)
                    maxResult = max(result[2], followUpResult[2], maxResult)
                    maxMatch = max(result[3], followUpResult[3], maxMatch)
                    
                if result[7] == True:
                    stepBackLine = past_line_2 + ' ' + past_line_1
                    stepBackResult = blaster.SMWalignment(tweet, stepBackLine.lower(), threshold)
                    maxResult = max(result[2], stepBackResult[2], maxResult)
                    maxMatch = max(result[3], stepBackResult[3], maxMatch)
                    
                if maxResult > mid_score and maxMatch > 3 or maxMatch > 5: 
                    suggestions = suggestions + '\n' + printResult(result, eachlyrics['title'], doc['_id'])
                    song = song + ' ' + eachlyrics['title']                   
                    score = maxResult
                    go_to_next_song = True # go to next song
                
                if maxResult > high_score:
                    suggestions = suggestions + '\n' + printResult(result, eachlyrics['title'], doc['_id'])
                    suggestions = suggestions + '\n' + 'found the song'
                    song = song + ' ' + eachlyrics['title']
                    score = maxResult
                    logging.info('found the song', extra= {'_id': doc['_id']})             
                    go_to_next_tweet = True
                    break
            
            if go_to_next_song == True: 
                break
             
        if go_to_next_tweet == True:
            break

    now = datetime.now()
    updatequery = {'_id': doc['_id']}
    newvalue = { '$set': {'score': round(score,2) , 'suggestions': suggestions, 'song': song, 'found': "v3", 'x_add': now.strftime("%Y-%m-%d %H:%M:%S")}}
    testTbl.update_one(updatequery, newvalue)
    

logFormatter = '%(asctime)s - %(_id)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='archived_tweets/myLogs.log',level=logging.DEBUG, format='%(asctime)s %(_id)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

cleaner = TextCleaner.TextCleaner()
# spell = SpellChecker()
normalizer = Normalizer.Normalizer()

blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']

threshold = 0.65
mid_score = 0.39
high_score = 0.64

mylyricquery = {}
  
myquery = {"found": {"$not" :{"$regex": { "$in": [ "0", "1" ] }}}}
myquery = {}

testTbl = mydb['MechTurk']
noofdoc = testTbl.find(myquery).count() #find() method returns a list of dictionary

x = 549
y = 20

while x < noofdoc:
    docs = testTbl.find(myquery).skip(x).limit(y)
#     serial code 
    for doc in docs: 
        searchTweet(doc)
    x = x + y
    
#     parallel code
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         executor.map(searchTweet, docs)
#     x = x + y

                                

