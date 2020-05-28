'''
Created on Mar 18, 2020

@author: WaylonLuo

lyricsgenius package installed from https://github.com/johnwmillr/LyricsGenius
The problem with needleAndHay search is that it only gives the last match of the sequence. 

'''

import lyricsgenius
import genius_credentials
import TextCleaner
import needleAndHay

genius = lyricsgenius.Genius(genius_credentials.CLIENT_ACCESS_TOKEN)
cleaner = TextCleaner.TextCleaner()
my_lyrics = 'lose yourself in the music' + ' the moment you own it '
#my_lyrics = 'Under the moonlight fading away'
result = genius.search_genius(my_lyrics.lower())

for hit in result['hits']:
    
    print('Song Title ' + hit['result']['title'])
    song_title = hit['result']['title']
    song = genius.search_song(song_title)
    counter = 0
    
    # split the song by line and
    # check every line against my_lyrics

    for line in song.lyrics.split('\n\n'):
        # set flag to false
        found = False 
        # clean the text
        line = cleaner.clean(line)
        my_lyrics = cleaner.clean(my_lyrics)
         
        searcher = needleAndHay.needleAndHay()
        found = searcher.searchTheNeelde(my_lyrics, line, 0.70)
        
        if found:
            print('Lyrics found')
            break
        
    # We will only find the first hit in the search result. 
    if found:
        break
            
    if counter == 3:
        break
    counter = counter + 1
    
