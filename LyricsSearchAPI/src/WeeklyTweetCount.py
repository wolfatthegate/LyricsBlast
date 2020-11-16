import pymongo

tablename = '2017-01-01-WeeklyTweets'
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

myquery = {"found": {"$not" :{"$regex": { "$in": [ "0", "1" ] }}}}
myquery = {}

twitterDataTbl = myclient['TwitterData']
tweetTbl = twitterDataTbl[tablename]
noofdoc = tweetTbl.find(myquery).count()

print(noofdoc)