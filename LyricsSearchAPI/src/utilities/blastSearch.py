import glob 
import TextCleaner
import blast

list_of_lyrics = glob.glob("LyricsDatabaseTest/*.*")

cleaner = TextCleaner.TextCleaner()
lyricFinder = blast.blast() 
threshold = 0.60
score = 0.30

def searchLyricsLocal(queryStr):
    for file in list_of_lyrics:
        with open(file, "r") as f:
            for dBline in f: 
                dBline = cleaner.clean(dBline)
                blaster = blast.blast()
                result = blaster.SMWalignment(dBline, queryStr, threshold)
                if result[2] > score or result[3] > 3:
                    print(' orig db str: ' + dBline)
                    print(' orig qy str: ' + queryStr)
                    print('   db string: ' + result[0])
                    print('query string: ' + result[1])
                    print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
                    print(' ')
                    break
                
with open("tweets/_Lyrics_References_Test.txt", "r") as tweets:
    for tweet in tweets:
        tweet = cleaner.clean(tweet.lower())
        searchLyricsLocal(tweet)