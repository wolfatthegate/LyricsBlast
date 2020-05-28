import glob 
import TextCleaner
import blast

list_of_lyrics = glob.glob("LyricsDatabase/*.*")

cleaner = TextCleaner.TextCleaner()
lyricFinder = blast.blast() 
threshold = 0.70


for file in list_of_lyrics:
    with open(file, "r") as f:
        for dBline in f: 
            dBline = cleaner.clean(dBline)
            print(dBline)
                
with open("tweets/_Lyrics_References.txt", "r") as tweets:
    for tweet in tweets:
        tweet = cleaner.clean(tweet.lower())
        print(tweet)