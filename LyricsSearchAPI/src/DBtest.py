import pymongo
import json
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['LyricsDB']
myTbl = mydb['Tweets_test']

myquery = {}
totalTweet = myTbl.find(myquery).count()


x = 0
limit = totalTweet
while x < totalTweet:
    for mydoc in myTbl.find(myquery).skip(x).limit(limit): #find() method returns a list of dictionary
        print(mydoc['description'])
    x = x + 3  