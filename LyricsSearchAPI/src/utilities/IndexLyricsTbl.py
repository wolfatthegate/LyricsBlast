import TextCleaner
import pymongo
import nltk
import blast
import sys

cleaner = TextCleaner.TextCleaner()
blaster = blast.blast()

def checkKeywords(str):
    old_terms = ['heroine', 'oxy', 'heroin', 'dopamine', 'norepinephrine', 
             'weed','cocaine', 'lean', 'blunt', 'joint', 'dank', 
             'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette', 
             'smoking', 'smokin', 'xan', 'pour', 'fuck', 'bitch', 'bitches']
    
    terms = ['weeds','weeded','weedhey','crystal','crackpipe','crackhead',
             'crack-head','crackin','crackers','cracker', 'morphine']
    
    tokenized_str = nltk.word_tokenize(str)
    blaster = blast.blast()
    keywordList = []
    for tokenized_word in tokenized_str:
        for term in terms:      
            result = blaster.SMalignmentGlobal(tokenized_word.lower(), term.lower())
            if result[2] > 0.85:
                return True

    return False
 

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']

myquery = {}
totalTweet = lyricTbl.find(myquery).count()

past_line_2 = ''
past_line_1 = ''
past_line_0 = ''
found = False



x = 7010
while x < totalTweet:
    for mydoc in lyricTbl.find(myquery).skip(x).limit(5): #find() method returns a list of dictionary
        if mydoc['lyrics']:
            
            newStr = ''
            past_line_2 = ''
            past_line_1 = ''
            past_line_0 = ''
            
            for eachline in mydoc['lyrics'].splitlines():
                   
                past_line_2 = past_line_1
                past_line_1 = past_line_0
                past_line_0 = eachline
                
                found = checkKeywords(past_line_1)
                
                if found == True:     
                    newStr = newStr + '\n' +past_line_2 + '\n' + past_line_1 + '\n' + past_line_0 + '\n'                       
                        
                updatequery = {'_id': mydoc['_id']}
                newvalue = { '$set': {'lyrics2': mydoc['lyrics2'] + '\n' + newStr}}
                lyricTbl.update_one(updatequery, newvalue)               
    x = x + 5 #incrementing the rows by 5
    if x % 50 == 0 : 
        print(x)
