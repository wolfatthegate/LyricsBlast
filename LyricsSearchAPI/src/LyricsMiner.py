# MongoDB Pagination example
#     db.students.find().limit(5)    # Page 1
#     db.students.find().skip(5).limit(5)    # Page 2
#     db.students.find().skip(5).limit(5)    # Page 3

import TextCleaner
import pymongo
import nltk
import blast
 
def findDrugKeywords(str):
    terms = ['weed','cocaine','lean', 'blunt', 'joint', 'dank', 'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette']
    try: 
        tokenized_str = nltk.word_tokenize(str)
    except:
        print(str + ' cannot be tokenized.')
    keywordList = []
    for tokenized_word in tokenized_str:
        for term in terms:
            if tokenized_word.lower() == term.lower():
                keywordList.append(tokenized_word.lower())   
    return keywordList
 
cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['TwitterData']
tweetTbl = mydb['NYtweets']

mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']
threshold = 0.65
found = False

file = open('archived_tweets/_searchresult.txt', 'w')

myquery = {}
totalTweet = tweetTbl.find(myquery).count()

x = 0
while x < totalTweet:
    for mydoc in tweetTbl.find(myquery).skip(x).limit(5): #find() method returns a list of dictionary
        if mydoc['description']:
            cleanTweet = cleaner.clean(mydoc['description'])
            query_list = findDrugKeywords(cleanTweet)
          
            for keyword in query_list:
                
                mylyricquery = {"lyrics": {"$regex": keyword}} # query keyword
                mylyrics = lyricTbl.find(mylyricquery)  #find in lyrics database
                
                for eachlyrics in mylyrics: #loop through mylyrics list
                                
                    # read each line of lyrics             
                    for eachline in eachlyrics['lyrics'].splitlines():
                        eachline = cleaner.clean(eachline)
                        # check if each line has keyword
                        if keyword.lower() in eachline.lower():
                            
                            # perform blast Search                    
                            result = blaster.SMWalignment(cleanTweet, eachline.lower(), threshold)
                            if result[2] > threshold and result[3] > 2:
                                
                                print('tweet: ' + result[0])
                                file.write('tweet: ' + result[0])
                                print('query: ' + result[1])
                                file.write('query: ' + result[1])
                                print('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachlyrics['title'])
                                file.write('Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)' + 'in song: ' + eachlyrics['title'])
                                print('')
                                file.write('\n')
                                found = True
                            if found == True: 
                                break
                        if found == True: 
                            break
            if found == False: 
                if len(mydoc['description']) > 25:
                    subTweet = mydoc['description'][0:25]
                else:
                    subTweet = mydoc['description']
                print('lyrics not detected. update the db. ' + subTweet.replace('\n', ''))
                
    x = x + 5 #incrementing the rows by 5
