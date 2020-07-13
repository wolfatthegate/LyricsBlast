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

 
def findDrugKeywords(str):
    terms = ['weed','cocaine','lean', 'blunt', 'joint', 'dank', 'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette', 'champagne', 'gasoline']
    tokenized_str = nltk.word_tokenize(str)
    keywordList = []
    for tokenized_word in tokenized_str:
        for term in terms:
            if tokenized_word.lower() == term.lower():
                keywordList.append(tokenized_word.lower())   
    return keywordList

combined_lines = ''
saved_line = ''
cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['LyricsDB']
testTbl = mydb['Test']
lyricTbl = mydb['Lyrics']
threshold = 0.65
score = 0.40


  
myquery = {"found": {"$not" :{"$regex": "2"}}}
mylyricquery = {}

mydoc = testTbl.find(myquery) #find() method returns a list of dictionary

file = open('archived_tweets/lyricsearchresult.txt', 'w')

for x in mydoc:
    
    tweet = x['data']
    query_list = findDrugKeywords(tweet)
    found = False
    second_chance = False
    trial_counter = 0
    
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
            print('tweet: ' + result[0])
            file.write('tweet: ' + result[0] + '\n')
            print('query: ' + result[1])
            file.write('query: ' + result[1] + '\n')
            print('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachtitle['title'])
            file.write('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachtitle['title'] + '\n')
            print('')
            file.write('\n')
            found = True
            break
        
    mylyricquery = {"lyrics": {"$regex": keyword, "$options": "-i"}} # query keyword
    mylyrics = lyricTbl.find(mylyricquery)  #find in lyrics database
    counter = 0
        
    for eachlyrics in mylyrics: #loop through mylyrics list
                        
            # read each line of lyrics             
            
        for eachline in eachlyrics['lyrics'].splitlines():
                
            eachline = cleaner.clean(eachline)
                
                # is this line follow up ? 
                # if it is follow up reconstruct the sentence and 
                
            if second_chance == True: 
                trial_counter += 1
                combined_lines = saved_line + ' ' + eachline.lower()
                tweet = cleaner.clean(tweet)
                result = blaster.SMWalignment(tweet, combined_lines, threshold)
            
                if result[2] > 0.60: 
                    print('second chance')
                    print('tweet: ' + result[0])
                    file.write('tweet: ' + result[0] + '\n')
                    print('query: ' + result[1])
                    file.write('query: ' + result[1] + '\n')
                    print('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachlyrics['title'])
                    file.write('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachlyrics['title'] + '\n')
                    print('')
                    file.write('\n')
                    second_chance = False
                    saved_line = ''
                    found = True
                    break
            
                else: 
                    saved_line = eachline.lower()
                    
                if trial_counter > 3:
                    trial_counter = 0
                    second_chance = False
                    saved_line = ''
                    break
                
                # check if each line has keyword
            if keyword.lower() in eachline.lower():
                tweet = cleaner.clean(tweet)
                # perform blast Search                    
                result = blaster.SMWalignment(tweet, eachline.lower(), threshold)
                if result[2] < 0.60 and result[3] > 3:
                    second_chance = True
                    saved_line = eachline.lower()
                
                # follow up = True or False            
                if result[2] > 0.60 and result[3] > 3: 
                     
                    print('tweet: ' + result[0])
                    file.write('tweet: ' + result[0] + '\n')
                    print('query: ' + result[1])
                    file.write('query: ' + result[1] + '\n')
                    print('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachlyrics['title'])
                    file.write('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachlyrics['title'] + '\n')
                    print('')
                    file.write('\n')
                    found = True
                    break
                    
            if found == True:
                break
        if found == True:
            break
    
file.close()

                                

