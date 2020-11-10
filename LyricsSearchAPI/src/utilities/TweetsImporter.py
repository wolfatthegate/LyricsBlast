import pymongo
import json
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
myTbl = mydb['Tweets_test']

# filepath = 'archived_tweets/nys_tweets_filtered_2014_Q2.json'
filepath = 'archived_tweets/nys_tweets_filtered_2014_Q1.json'

with open(filepath, 'r') as f:
    for line in f:
        line = line.strip() # read only the first tweet line
        tweet = json.loads(line) # load it as Python dictionary
#         print(json.dumps(tweet, indent = 4)) # pretty-print
        try:
            tweetID = str(tweet['id'])
            description = tweet['user']['description']
            createdAt = tweet['created_at']
            location = tweet['place']['full_name']
             
            data = {'tweetID': tweetID ,
                    'description': description ,
                    'createdAt': createdAt ,
                    'location': location}
        except:
            print('empty json') 
        try:
            myTbl.insert_one(data)
        except:
            print('insertion error')
    
with open('archived_tweets/log.txt', 'w') as logfile:
    logfile.write('finished importing file: {} at {}'.format(filepath, datetime.now().time())) 
        