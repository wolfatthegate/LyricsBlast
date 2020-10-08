import json
import DBFactory
from datetime import datetime

dbworker = DBFactory.DBFactory()
# filepath = 'archived_tweets/nys_tweets_filtered_2014_Q2.json'
filepath = 'tweets/NY-Mech-Turk.txt'

with open(filepath, 'r') as f:
    for line in f:
        line = line.strip() # read only the first tweet line

        data = {'data': line}
 
        try:
            dbworker.insert2MongoDB(0, 'MechTurk', 'LyricsDB', data)
        except:
            print('insertion error')
    
print('done importing')
