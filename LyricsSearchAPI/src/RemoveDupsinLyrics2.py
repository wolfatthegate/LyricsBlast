# This program takes strings from Lyrics2 column
# remove duplicate lines and insert into Lyrics3
# This program should run only once. 

import TextCleaner
import pymongo
import nltk
import blast
import sys
import json
import re
import string
import vincent
import TextCleaner

from datetime import datetime



myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']

myquery = {}
totalSongs = lyricTbl.find(myquery).count()
limit = 50
x=5674

while x < 5680:
    for mydoc in lyricTbl.find(myquery).skip(x).limit(limit): #find() method returns a list of dictionary       
        try: 
            temp_lines = []
            lyrics3 = ''
            for line in mydoc['lyrics2'].splitlines():
                temp_lines.append(line)
            temp_lines = list(dict.fromkeys(temp_lines))   
            for line in temp_lines:
                lyrics3 = lyrics3 + '\n' + line
            now = datetime.now()
            updatequery = {'_id': mydoc['_id']}
            newvalue = { '$set': {'lyrics3': lyrics3, 'x_add': now.strftime("%Y-%m-%d %H:%M:%S")}}
            lyricTbl.update_one(updatequery, newvalue)
        except Exception as exc:
            print('{} exception while updating at x = {}. {} '.format(mydoc['title'], x, exc)) 
        
    x = x + 5 
    print(x)



