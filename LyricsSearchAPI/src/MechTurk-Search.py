# import sys
# from os import path
# 
# 
# sys.path.append(path.abspath('/Users/WaylonLuo/git/DrugAbusePrevention'))
# 
# from dbModels.MongoDbModel import MongoDbModel
# from dbModels.MongoDbService import MongoDbService
# 
# dBName = 'LyricsDB'
# tableName = 'Lyrics'
# query = {"name": "Kanye West"}
# results = {}
#       
# mongoDbService = MongoDbService('mongodb://localhost:27017/')
# mongoDbModel = MongoDbModel(mongoDbService.client, dBName)
# result = mongoDbModel.find(tableName, query)
#  
# mongoDbService.close()
# 
# for single in result: 
#     print(single)

import TextCleaner
import pymongo
import nltk
import blast
import sys
from datetime import datetime

def printSearchResult(result, songtitle):
    print('')
    print('tweet: ' + result[0])
    print('query: ' + result[1])
    print('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + songtitle)
    print(' first half score: ' + str(round(result[4], 2)))
    print('second half score: ' + str(round(result[5], 2)))
    
    with open('archived_tweets/log.txt', 'a') as file: 
        file.write('\n')
        file.write('tweet: ' + result[0] + '\n')
        file.write('query: ' + result[1] + '\n')
        file.write('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + songtitle + '\n')
        file.write(' first half score: ' + str(round(result[4], 2)) + '\n')
        file.write('second half score: ' + str(round(result[5], 2)) + '\n')
 
def findDrugKeywords(str):
    
    terms = ['heroin', 'heroine', 'oxy', 'dopamine', 'norepinephrine',
             'weed','cocaine', 'lean', 'blunt', 'joint', 'dank',
             'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette',
             'smoking', 'smokin', 'pour', 'xan']

    related_terms = ['bitch', 'bitches', 'fuck', 'fucked', 'sniff', 'sniffed', 'sniffin', 'addict', 'addicted', 
                     'addictin', 'need', 'narcotics', 'sell', 'sells', 'sellin', 'sold',
                     'dick', 'girl', 'girls', 'snort', 'snorted', 'shit', 'sip', 'sippin', 'sipping',
                     'coke-head', 'crack-head', 'cokehead', 'crackhead', 'head', 'hookers', 'gas', 'gasoline',
                     'arrested', 'baby', 'babe', 'bowl', 'drug', 'life', 'like', 'bag', 'cook', 'cooked', 
                     'mother', 'mothafucka', 'motha', 'fucka', 'pound', 'pint', 'ass', 'pussy',
                     'line', 'lines', 'roll', 'dosage', 'gram', 'whore', 'whores', 'cure', 'poison', 'gun',
                     'guns', 'rock', 'kids', 'friend', 'friends', 'want', 'share', 'shared', 'do', 'kid', 
                     'hot', 'sex', 'try', 'tried' 'sick', 'love', 'did', 'doing', 'doin', 'shoot', 'shoots', 
                     'dream', 'dreaming', 'spill', 'jack', 'rum', 'bourbon', 
                     'suck', 'sucks', 'chill', 'pipe', 'pipes', 'hoe', 'hoes', 'white', 'smell', 'dip', 'real', 'taking']

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

cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']

threshold = 0.65
mid_score = 0.50
high_score = 0.64

mylyricquery = {}
  
myquery = {"found": {"$not" :{"$regex": { "$in": [ "0", "1" ] }}}}
myquery = {"suggestions": {"$not" :{ "$in": ["-2"]  }}}

testTbl = mydb['MechTurk']
noofdoc = testTbl.find(myquery).count() #find() method returns a list of dictionary

x = 0
y = 5

while x < noofdoc:
    for doc in testTbl.find(myquery).skip(x).limit(y):
        
        tweet = doc['data']
        tweet = cleaner.clean(tweet)
        
        query_list = findDrugKeywords(tweet)
        
        if not query_list:
            updatequery = {'_id': doc['_id']}
            newvalue = { '$set': {'score': 0.00 , 'suggestions': 'keywords not found', 'song': '', 'found': "0"}}
            testTbl.update_one(updatequery, newvalue)
            continue
        
        go_to_next_tweet = False
        titleMatched = False
        savedline = ''
        combined_lines = ''
        song = ''
        score = 0.00
        suggestions = 0
        found = "0"
        
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
            
        print(mytitlequery)
        print('searching for ' + temp_str + ' ' + str(mytitle.count()) + ' titles found.')
        
        with open('archived_tweets/log.txt', 'a') as file: 
            file.write('searching for ' + temp_str + ' ' + str(mytitle.count()) + ' titles found.' + '\n')
        for eachtitle in mytitle: 
            title = cleaner.clean(eachtitle['title'])       
            result = blaster.SMWalignment(tweet.lower(), title.lower(), threshold)
                
            if round(result[2],2) > 0.85: 
                print('title matched:')
                with open('archived_tweets/log.txt', 'a') as file:
                    file.write('title matched:' + '\n')
                titleMatched = True
                printSearchResult(result, eachtitle['title'])
                song = eachtitle['title']
                suggestions += 1
                score = result[2]
                updatequery = {'_id': doc['_id']}
                newvalue = { '$set': {'score': round(score,2) , 'suggestions': str(suggestions), 'song': song, 'found': "1"}}
                testTbl.update_one(updatequery, newvalue)
                break
        
        if titleMatched == True:
            continue
          
        mylyricquery = {'$and': keyword_list_lyric} # query keyword
        mylyrics = lyricTbl.find(mylyricquery)  #find in lyrics database
    
        print(str(mylyrics.count()) + ' lyrics found.')
        with open('archived_tweets/log.txt', 'a') as file:
            file.write(str(mylyrics.count()) + ' lyrics found.' + '\n')
            
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
         
                    if result[2] > mid_score and result[3] > 3: 
                        printSearchResult(result, eachlyrics['title'])
                        song = song + ' ' + eachlyrics['title']
                        suggestions += 1
                        score = result[2]
                        if followUp == False:
                            go_to_next_song = True # go to next song
                    
                    if result[2] > high_score or (result[4] > high_score and result[3] > 4):
                        printSearchResult(result, eachlyrics['title'])
                        song = song + ' ' + eachlyrics['title']
                        score = max(result[2], result[4])
                        print('found the song')
                        found = "1"                
                        go_to_next_tweet = True
                        break
    
                else: 
                    previous_line = eachline
                
                if go_to_next_song == True: 
                    break
                        
            if suggestions > 4 or go_to_next_tweet == True:
                break
            
        print('No of suggestions: ' + str(suggestions) + ' for ' + doc['data'])
        now = datetime.now().time() # time object
    
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)   
        
        with open('archived_tweets/log.txt', 'a') as file:
            file.write('No of suggestions: ' + str(suggestions) + ' for ' + doc['data'] + '\n')
            file.write("Current Time =" + current_time + '\n')
        updatequery = {'_id': doc['_id']}
        newvalue = { '$set': {'score': round(score,2) , 'suggestions': str(suggestions), 'song': song, 'found': found}}
        testTbl.update_one(updatequery, newvalue)
    x = x + y

                                

