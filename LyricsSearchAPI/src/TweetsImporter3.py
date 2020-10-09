import pymongo
import json
from datetime import datetime

print('This program is for remote server. Do not run it here locally. Terminating program...')
quit()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
myTbl = mydb['MechTurk']

# filepath = 'archived_tweets/nys_tweets_filtered_2014_Q2.json'
filepath = 'archived_tweets/MechTuck.json'

count = 0; 
with open(filepath, 'r') as f:
    data = json.load(f)
    for d in data: 

        try: 
            data = {'data': d['data']}           
        except:
            print('empty json') 
        try:
            myTbl.insert_one(data)
        except:
            print('insertion error')
    
# with open('archived_tweets/log.txt', 'w') as logfile:
#     logfile.write('finished importing file: {} at {}'.format(filepath, datetime.now().time())) 
        