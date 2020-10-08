import TextCleaner
import pymongo
import nltk
import blast
import sys
 
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

x = 0
limit = totalTweet
while x < totalTweet:
    for mydoc in lyricTbl.find(myquery).skip(x).limit(limit): #find() method returns a list of dictionary
        updatequery = {'_id': mydoc['_id']}
        newvalue = { '$set': {'suggestions': '', 'score': 0.0, 'song': '', 'matched': 0}}
        lyricTbl.update_one(updatequery, newvalue)
    x = x + 3  


            
                