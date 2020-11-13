import random
import json

tweetsfile = open("tweets/2017-01-01-Weekly-fullbatch-with-tweets.json", "r")
sampletweets = open("tweets/2017-01-01-Weekly-500SampleTweets.json", "w+")

tweetslist = []
sample500 = []

data = json.load(tweetsfile)

for d in data:
    tweetslist.append('  ' + str(d['tweet']).replace('\n', ' '))
    
sample500 = random.sample(tweetslist, 500)

for line in sample500:
    sampletweets.write(str(line))
    sampletweets.write(',\n')

tweetsfile.close()
sampletweets.close()
    
