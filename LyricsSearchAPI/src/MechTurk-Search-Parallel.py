import TextCleaner
import pymongo
import nltk
import blast
import sys
import concurrent.futures
import logging
from datetime import datetime

def printResult(result, songtitle, doc_id):

    logging.info('tweet: ' + result[0], extra={'_id': doc_id})
    logging.info('query: ' + result[1], extra={'_id': doc_id})
    logging.info('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + songtitle, extra={'_id': doc_id})
    logging.info(' first half score: ' + str(round(result[4], 2)), extra={'_id': doc_id})
    logging.info('second half score: ' + str(round(result[5], 2)), extra={'_id': doc_id})
    
    suggestions = 'tweet: ' + result[0] + '\n' + 'query: ' + result[1] + 'Score: ' + \
                    str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)'
    
    return suggestions
 
def findDrugKeywords(str):
    
    terms = ['heroin', 'heroine', 'oxy', 'dopamine', 'norepinephrine',
             'weed','cocaine', 'lean', 'blunt', 'joint', 'dank',
             'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette',
             'smoking', 'smokin', 'pour', 'xan']

    related_terms = ['bitch', 'bitches', 'fuck', 'fucked', 'sniff', 'sniffed', 'sniffin', 'addict', 'addicted', 
                     'addictin', 'need', 'narcotics', 'sell', 'sells', 'sellin', 'sold',
                     'dick', 'girl', 'girls', 'snort', 'snorted', 'shit', 'sip', 'sippin', 'sipping',
                     'hookers', 'gas', 'gasoline',
                     'arrested', 'baby', 'babe', 'bowl', 'drug', 'life', 'like', 'bag', 'cook', 'cooked', 
                     'pound', 'pint', 'ass', 'pussy',
                     'line', 'lines', 'roll', 'dosage', 'gram', 'whore', 'whores', 'cure', 'poison', 'gun',
                     'guns', 'rock', 'kids', 'friend', 'friends', 'want', 'share', 'shared', 'do', 'kid', 
                     'hot', 'sex', 'try', 'tried' 'sick', 'love', 'did', 'doing', 'doin', 'shoot', 'shoots', 
                     'dream', 'dreaming', 'spill', 'jack', 'rum', 'bourbon', 
                     'suck', 'sucks', 'chill', 'pipe', 'pipes', 'hoe', 'hoes', 'white', 'smell', 'dip', 'real', 'taking', 'get']

    substracted_terms = ['mother', 'mothafucka', 'motha', 'fucka', 'coke-head', 'crack-head', 'cokehead', 'crackhead', 'head']
    
    tokenized_str = nltk.word_tokenize(str)
    blaster = blast.blast()
    keywordList = []
    for tokenized_word in tokenized_str:
        for term in terms:      
            result = blaster.SMalignmentGlobal(tokenized_word.lower(), term.lower())
            if result[2] > 0.85:
                term = term.replace('ing', 'in')
                keywordList.append(term.lower())   
    if keywordList:            
        for tokenized_word in tokenized_str:     
            for term in related_terms:
                result = blaster.SMalignmentGlobal(tokenized_word.lower(), term.lower())
                if result[2] > 0.90:
                    keywordList.append(term.lower())  
            
    return keywordList

def searchLyrics(doc):
    tweet = doc['data']
    tweet = cleaner.clean(tweet)
    
    query_list = findDrugKeywords(tweet)
    
    if not query_list:
        updatequery = {'_id': doc['_id']}
        newvalue = { '$set': {'score': 0.00 , 'suggestions': 'keywords not found', 'song': '', 'found': "6"}}
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
        keyword_list_lyric.append({"lyrics2": {"$regex": query_word, "$options": "-i"}})
    
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
            
        if round(result[2],2) > 0.85: 
            logging.info('title found', extra = {'_id': doc['_id']})
            titleMatched = True
            suggestions = suggestions + '\n' + printResult(result, eachtitle['title'], doc['_id'])   
            updatequery = {'_id': doc['_id']}
            newvalue = { '$set': {'score': round(result[2],2), \
                            'suggestions': suggestions, \
                                'song': eachtitle['title'], 'found': "6"}}
            testTbl.update_one(updatequery, newvalue)
            break
    
    if titleMatched == True:
        return 0
      
    mylyricquery = {'$and': keyword_list_lyric} # query keyword
    mylyrics = lyricTbl.find(mylyricquery)  #find in lyrics database

    logging.info(mylyricquery, extra= {'_id': doc['_id']})
    logging.info(str(mylyrics.count()) + ' possible lyrics found.', extra= {'_id': doc['_id']})
        
    for eachlyrics in mylyrics: #loop through mylyrics list
        
        go_to_next_song = False  
        continue_test = False  
        followUp = False
        stepBack = False
        # read each line of lyrics  
        for eachline in eachlyrics['lyrics2'].splitlines():
                
            eachline = cleaner.clean(eachline)
            
            for query_word in query_list:
                if query_word.lower() in eachline.lower():
                    continue_test = True
                    
            if followUp == True: 
                eachline = savedline + ' ' + eachline     
                # check if each line has keyword
            if stepBack == True: 
                eachline = previous_line + ' ' + savedline
                
            if continue_test == True or stepBack == True or followUp == True:
                followUp = False
                stepBack = False
                tweet = cleaner.clean(tweet)
                # perform blast Search                    
                result = blaster.SMWalignment(tweet, eachline.lower(), threshold)
                
                if result[6] == True:
                    followUp = True
                    savedline = eachline
                
                if result[7] == True:
                    stepBack = True
                    savedline = eachline
                if result[2] > 0.10:
                    printResult(result, eachlyrics['title'], doc['_id'])
                
                if result[2] > mid_score and result[3] > 3 or result[3] > 5:
                    suggestions = suggestions + '\n' + printResult(result, eachlyrics['title'], doc['_id'])
                    song = song + ' ' + eachlyrics['title']    
                    score = result[2]                                 
                    if followUp == False:
                        go_to_next_song = True # go to next song
                
                if result[2] > high_score or (result[4] > high_score and result[3] > 4):
                    uggestions = suggestions + '\n' + printResult(result, eachlyrics['title'], doc['_id'])
                    song = song + ' ' + eachlyrics['title'] 
                    score = max(result[2], result[4])
                    logging.info('found the song')                
                    go_to_next_tweet = True
                    break

            else: 
                previous_line = eachline
            
            if go_to_next_song == True: 
                break
                    
        if go_to_next_tweet == True:
            break

    updatequery = {'_id': doc['_id']}
    newvalue = { '$set': {'score': round(score,2) , 'suggestions': suggestions, 'song': song, 'found': "5"}}
    testTbl.update_one(updatequery, newvalue)
    

logFormatter = '%(asctime)s - %(_id)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='archived_tweets/myLogs.log',level=logging.DEBUG, format='%(asctime)s %(_id)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']

threshold = 0.65
mid_score = 0.39
high_score = 0.64

mylyricquery = {}
  
myquery = {"found": {"$not" :{"$regex": { "$in": [ "0", "1" ] }}}}
myquery = {"found": { "$in": [ "5" ] }}
myquery = {}

testTbl = mydb['MechTurk_Test']
noofdoc = testTbl.find(myquery).count() #find() method returns a list of dictionary

x = 0
y = 5

while x < noofdoc:
    docs = testTbl.find(myquery).skip(x).limit(y)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(searchLyrics, docs)

#     for doc in docs: 
#         searchLyrics(doc)
    x = x + y

                                

