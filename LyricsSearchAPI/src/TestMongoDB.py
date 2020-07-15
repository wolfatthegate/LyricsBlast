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

def printSearchResult(result):
    print('')
    print('tweet: ' + result[0])
    print('query: ' + result[1])
    print('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachlyrics['title'])
    print(' first half score: ' + str(round(result[4], 2)))
    print('second half score: ' + str(round(result[5], 2)))
 
def findDrugKeywords(str):
    
    terms = ['weed','cocaine','lean', 'blunt', 'joint', 'dank', 'crack', 
             'molly', 'coke', 'smoke', 'dope', 'cigarette', 'champagne', 'gasoline']
     
    tokenized_str = nltk.word_tokenize(str)
    keywordList = []
    for tokenized_word in tokenized_str:
        for term in terms:
            if tokenized_word.lower() == term.lower():
                keywordList.append(tokenized_word.lower())   
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

myquery = {"found": {"$not" :{ "$in": [ "0", "1" ] }}}

testTbl = mydb['MechTurk']
mydoc = testTbl.find(myquery) #find() method returns a list of dictionary

for x in mydoc:
    
    tweet = x['data']
    query_list = findDrugKeywords(tweet)
    go_to_next_tweet = False
    followUp = False
    stepBack = False
    titleMatched = False
    savedline = ''
    combined_lines = ''
    song = ''
    score = 0.00
    suggestions = 0
    found = "0"
    
    print('searching for ' + x['data'])
    for query_word in query_list:
        keyword = query_word
        break

    mytitlequery = {"title": {"$regex": keyword, "$options": "-i"}} # query keyword
    mytitle = lyricTbl.find(mytitlequery)
    
    for eachtitle in mytitle: 
        title = cleaner.clean(eachtitle['title'])       
        result = blaster.SMWalignment(tweet.lower(), title.lower(), threshold)
            
        if round(result[2],2) > 0.85: 
            print('title matched:')
            titleMatched = True
            printSearchResult(result)
            song = song + ' ' + eachlyrics['title']
            suggestions += 1
            score = result[2]
            updatequery = {'_id': x['_id']}
            newvalue = { '$set': {'score': round(score,2) , 'suggestions': str(suggestions), 'song': song, 'found': 1}}
            testTbl.update_one(updatequery, newvalue)
            break
    
    if titleMatched == True:
        continue
      
    mylyricquery = {"lyrics": {"$regex": keyword, "$options": "-i"}} # query keyword
    mylyrics = lyricTbl.find(mylyricquery)  #find in lyrics database
        
    for eachlyrics in mylyrics: #loop through mylyrics list
        
        go_to_next_song = False    
        # read each line of lyrics  
        for eachline in eachlyrics['lyrics'].splitlines():
                
            eachline = cleaner.clean(eachline)
            if followUp == True: 
                eachline = savedline + ' ' + eachline
                followUp = False
                # check if each line has keyword
            if stepBack == True: 
                eachline = previous_line + ' ' + savedline
                stepBack = False
                
            if keyword.lower() in eachline.lower():
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
                    printSearchResult(result)
                    song = song + ' ' + eachlyrics['title']
                    suggestions += 1
                    score = result[2]
                    if followUp == False:
                        go_to_next_song = True # go to next song
                
                if result[2] > high_score or (result[4] > high_score and result[3] > 4):
                    printSearchResult(result)
                    song = song + ' ' + eachlyrics['title']
                    score = result[2]
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
        
    print('No of suggestions: ' + str(suggestions) + ' for ' + x['data'])
    updatequery = {'_id': x['_id']}
    newvalue = { '$set': {'score': round(score,2) , 'suggestions': str(suggestions), 'song': song, 'found': found}}
    testTbl.update_one(updatequery, newvalue)


                                

