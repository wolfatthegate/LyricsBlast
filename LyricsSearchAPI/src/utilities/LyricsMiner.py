# MongoDB Pagination example
#     db.students.find().limit(5)    # Page 1
#     db.students.find().skip(5).limit(5)    # Page 2
#     db.students.find().skip(5).limit(5)    # Page 3

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
    terms = ['weed','cocaine','lean', 'blunt', 'joint', 'dank', 'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette', 'champagne', 'gasoline']
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

mydb = myclient['TwitterData']
tweetTbl = mydb['NYtweets']

mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']

threshold = 0.65
mid_score = 0.39
high_score = 0.80

file = open('archived_tweets/_searchresult.txt', 'w')

myquery = {}
totalTweet = tweetTbl.find(myquery).count()

x = 0
while x < totalTweet:
    for mydoc in tweetTbl.find(myquery).skip(x).limit(5): #find() method returns a list of dictionary
        
        go_to_next_tweet = False
        followUp = False
        stepBack = False
        titleFound = False
        savedline = ''
        combined_lines = ''
        keyword = ''
        suggestions = 0
        
        if mydoc['description']:
            
            score = 0.0
            song = ''
            tweet = cleaner.clean(mydoc['description'])
            query_list = findDrugKeywords(tweet)
          
            if not query_list:
#                 print('empty query list. ID:' + mydoc['tweetID']) 
                continue
            for query_word in query_list:
                keyword = query_word
                break
            
            # Check the title of the song before mining the lyrics
            
            mytitlequery = {"title": {"$regex": keyword, "$options": "-i"}} # query keyword
            mytitle = lyricTbl.find(mytitlequery)
    
            for eachtitle in mytitle: 
                title = cleaner.clean(eachtitle['title'])       
                result = blaster.SMWalignment(tweet.lower(), title.lower(), threshold)
            
                if round(result[2],2) > 0.85: 
                    print('title matched:')
                    suggestions += 1
                    printSearchResult(result)
                    song = eachlyrics['title']
                    score = result[2]
                    titleFound = True
                    updatequery = {'_id': mydoc['_id']}
                    newvalue = { '$set': {'score': round(score,2), 'song': song}}
                    testTbl.update_one(updatequery, newvalue)  
                    break
            
            if titleFound ==True:
                continue
            # Start mining the lyrics 
            
            mylyricquery = {"lyrics": {"$regex": keyword}} # query keyword
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
                            song = eachlyrics['title']
                            score = result[2]
                            if followUp == False:
                                go_to_next_song = True # go to next song
                    
                        if result[2] > high_score or (result[4] > high_score and result[3] > 4):
                            printSearchResult(result)
                            song = eachlyrics['title']
                            score = result[2]
                            print('found the song')
                            go_to_next_tweet = True
                            break
    
                    else: 
                        previous_line = eachline
                
                    if go_to_next_song == True: 
                        break
                if suggestions > 4 or go_to_next_tweet == True:
                    break
        
            if len(mydoc['description']) > 35:
                subTweet = mydoc['description'][0:35]
            else:
                subTweet = mydoc['description']        
            print('Score: ' + str(round(score,2)) + '  for Tweet: ' + subTweet)
            updatequery = {'_id': mydoc['_id']}
            newvalue = { '$set': {'score': round(score,2), 'song': song}}
            testTbl.update_one(updatequery, newvalue)
         
        else:
            updatequery = {'_id': mydoc['_id']}
            newvalue = { '$set': {'score': 0.00, 'song': ''}}
            testTbl.update_one(updatequery, newvalue)  
    x = x + 5 #incrementing the rows by 5
