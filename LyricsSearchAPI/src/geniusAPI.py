import lyricsgenius #https://github.com/johnwmillr/LyricsGenius
import genius_credentials
import json
import TextCleaner
import DBFactory
        
# all the method
def findSongInList(songlist, songID):
    for i in range(len(songlist)):
        if int(songlist[i]) == songID:
            return True
    return False

# initialize variables
genius = lyricsgenius.Genius(genius_credentials.CLIENT_ACCESS_TOKEN) 
genius.verbose = False # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title

downloaded_term = ['heroine', 'oxy', 'heroin', 'dopamine', 'norepinephrine', 'weed','cocaine','lean', 'blunt', 'joint', 'dank', 'crack', 'molly', 'coke', 'smoke', 'dope', 'cigarette']


terms = ['morphine']
nextPage = True
curPage = 1

saveInDB = True
saveInFile = False
 
found = False  
# define list of places
songlistLocal = []

# open file and read the content in a list
cleaner = TextCleaner.TextCleaner()
dbWorker = DBFactory.DBFactory()
for term in terms:
    with open('LyricsDatabase/_songlist.txt', 'r') as filehandle:
        filecontents = filehandle.readlines()
    
        for line in filecontents:
            # remove linebreak which is the last character of the string
            songlistLocal.append(line.strip())
     
    while nextPage is True:
        result = genius.search_all_term(term, per_page = 50, page = curPage)
    
        # convert JSON object into a JSON string 
        json_str = json.dumps(result)
         
        # parse JSON string into Python dictionary
        data = json.loads(json_str)
        data_section = data['sections'][0]['hits']
        
        if len(data['sections'][0]['hits']) == 0:
            # end of paige
            break
        
        print('CurrentPage: ' + str(curPage) + ' term: ' + term)
         
        for songlist in data_section:    
            
            # pull out the parameters
            name = songlist['result']['primary_artist']['name']
            title = songlist['result']['title']
            genius_songID = songlist['result']['id']
       
            found = findSongInList(songlistLocal, genius_songID)
            
            if found is True:
                continue
            
            song = genius.search_song(title, name)
            try:
                year = song.year
                lyrics = song.lyrics
            except:
                print("No Data in Song")
            
            data = {'name': name,
                'title': title,
                'year': year,
                'genius_songID': genius_songID,
                'lyrics': lyrics}
            
            if saveInDB is True:
                dbWorker.insert2MongoDB(genius_songID, 'Lyrics', 'LyricsDB', data)
            
            if saveInFile is True: 
                filename = cleaner.clean(title) + '-' + cleaner.clean(name) + '-' + str(genius_songID)
                with open( 'LyricsDatabase/' + filename + '.txt', 'w') as outfile:
                     json.dump(data, outfile)
            
            songlistLocal.append(genius_songID)
        
        # update the song list in the _songlist.txt file locally 
        with open('LyricsDatabase/_songlist.txt', 'w') as filehandle:
            for listitem in songlistLocal:
                filehandle.write('%s\n' % listitem)  
                
        # go to next search page
        curPage += 1