import glob
filepathList = glob.glob("week2_json/*.json")

import pymongo
import json
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['TwitterData']
myTbl = mydb['2017-07-16-WeeklyTweets']

def TweetImporter(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip() # read only the first tweet line
            tweet = json.loads(line) # load it as Python dictionary
    #         print(json.dumps(tweet, indent = 4)) # pretty-print
            try:
                tweetID = str(tweet['id'])
                description = tweet['user']['description']
                text = tweet['text'] # actual tweet
                createdAt = tweet['created_at']
                location = tweet['place']['full_name']
                 
                data = {'tweetID': tweetID,
                        'description': description, 
                        'tweet': text,
                        'createdAt': createdAt,
                        'location': location}
            except:
                print('duplicate')
            try:
                myTbl.insert_one(data)
            except:
                print('insertion error. TweetID: ' + tweetID)
                #logfile.write('duplicate data. TweetID: {}. Tweet {}. Filepath {}\n'.format(tweetID, description, filepath)) 
    
        logfile.write('finished importing file: {} at {}\n'.format(filepath, datetime.now().time())) 

for filepath in filepathList: 
    with open('logs/week2_json_log.txt', 'a') as logfile:
        TweetImporter(filepath)
    
