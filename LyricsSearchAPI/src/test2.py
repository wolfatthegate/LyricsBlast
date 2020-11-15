import random
import json

tweetsfile = open("tweets/2017-01-01-Weekly-500Samples.json", "r")
tweetslist = []

data = json.load(tweetsfile)

for d in data:
    print(d)
    
tweetsfile.close()

    