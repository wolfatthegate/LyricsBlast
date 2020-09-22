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
    
    suggestions = 'tweet: ' + result[0] + '\n' + 'query: ' + result[1] + '\nScore: ' + \
                    str(round(result[2],2)) + '/1.0 \n(' + str(result[3]) + ' words matched)'
    
    return suggestions
 
def findDrugKeywords(str):
    
    terms = ['heroin', 'heroine', 'oxy', 'dopamine', 'norepinephrine',
             'weed','cocaine', 'lean', 'blunt', 'joint', 'dank',
             'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette',
             'smoking', 'smokin', 'pour', 'xan']

    related_terms = ['bitch', 'bitches', 'fuck', 'fucked', 'sniff', 'sniffed', 'sniffin', 'addict', 'addicted', 
                     'addictin', 'need', 'narcotics', 'sell', 'sells', 'sellin', 'sold',
                     'dick', 'girl', 'girls', 'snort', 'snorted', 'shit', 'sip', 'sippin', 'sipping',
                     'hookers', 'gas', 'gasoline', 'arrested', 'baby', 'babe', 'bowl', 'drug', 'life', 'like', 'bag', 'cook', 'cooked', 
                     'pound', 'pint', 'ass', 'pussy', 
                     'line', 'lines', 'roll', 'dosage', 'gram', 'whore', 'whores', 'cure', 'poison', 'gun',
                     'guns', 'rock', 'kids', 'friend', 'friends', 'want', 'share', 'shared', 'kid', 
                     'hot', 'sex', 'try', 'tried' 'sick', 'love', 'do', 'does', 'did', 'doing', 'doin', 'shoot', 'shoots', 
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
            
    keywordList = list(dict.fromkeys(keywordList))
    return keywordList

def searchTweet(doc):
    tweet = doc['data']
    tweet = cleaner.clean(tweet)
    
    query_list = findDrugKeywords(tweet)
    
    if not query_list:
        now = datetime.now()
        updatequery = {'_id': doc['_id']}
        newvalue = { '$set': {'score': 0.00 , 'suggestions': 'keywords not found', 'song': '', 'found': found, 'x_add': now.strftime("%Y-%m-%d %H:%M:%S")}}
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
            now = datetime.now() 
            updatequery = {'_id': doc['_id']}
            newvalue = { '$set': {'score': round(result[2],2), \
                            'suggestions': suggestions, \
                                'found': "-1", \
                                    'song': eachtitle['title'], 'found': found, \
                                        'x_add': now.strftime("%Y-%m-%d %H:%M:%S")}}
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
        
        maxResult = 0
        maxMatch = 0
  
        for eachline in eachlyrics['lyrics3'].splitlines():
            
            eachline = cleaner.clean(eachline)
            
            past_line_2 = past_line_1
            past_line_1 = past_line_0
            past_line_0 = eachline
            
            for query_word in query_list:
                if query_word.lower() in past_line_1.lower():
                    continue_test = True
                        
            if continue_test == True:
                followUp = False
                stepBack = False

                # perform blast Search                    
                result = blaster.SMWalignment(tweet, past_line_1.lower(), threshold)
                maxResult = result[2]
                maxMatch = result[3]
                    
                if result[6] == True:
                    followupLine = past_line_1 + '\n' + past_line_0
                    followUpResult = blaster.SMWalignment(tweet, followupLine.lower(), threshold)
                    maxResult = max(result[2], followUpResult[2], maxResult)
                    maxMatch = max(result[3], followUpResult[3], maxMatch)
                    
                if result[7] == True:
                    stepBackLine = past_line_2 + '\n' + past_line_1
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
    newvalue = { '$set': {'score': round(score,2) , 'suggestions': suggestions, 'song': song, 'found': found, 'x_add': now.strftime("%Y-%m-%d %H:%M:%S")}}
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
found = 'v1'
mylyricquery = {}
  
myquery = {"found": {"$not" :{"$regex": { "$in": [ "0", "1" ] }}}}
myquery = {}

testTbl = mydb['MechTurk']
noofdoc = testTbl.find(myquery).count() #find() method returns a list of dictionary

x = 0
y = 20

while x < noofdoc:
    docs = testTbl.find(myquery).skip(x).limit(y)
#     serial code 
#     for doc in docs: 
#         searchTweet(doc)
#     x = x + y
    
#     parallel code
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(searchTweet, docs)
    x = x + y

                                

