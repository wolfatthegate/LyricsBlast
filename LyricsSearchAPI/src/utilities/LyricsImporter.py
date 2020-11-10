import pymongo
import json
from datetime import datetime

print('This program is for remote server. Do not run it here locally. Terminating program...')
quit()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
myTbl = mydb['MechTurk_Test']

# filepath = 'archived_tweets/nys_tweets_filtered_2014_Q2.json'
filepath = 'archived_tweets/lyrics.json'

count = 0; 
with open(filepath, 'r') as f:
    data = json.load(f)
    for d in data: 
#         print(d)

        try:
            name = str(d['name'])
            title = d['title']
            year = d['year']
            genius_songID = d['genius_songID']
            x_add = d['x_add']
            lyrics4 = d['lyrics4'].replace('\n\n\n', '\n')
              
            data = {'name': name ,
                    'title': title ,
                    'year': year ,
                    'genius_songID': genius_songID,
                    'x_add': x_add, 
                    'lyrics4': lyrics4}
            print(data)
            
        except:
            print('empty json') 
        try:
            myTbl.insert_one(data)
        except:
            print('insertion error')
    
# with open('archived_tweets/log.txt', 'w') as logfile:
#     logfile.write('finished importing file: {} at {}'.format(filepath, datetime.now().time())) 
        