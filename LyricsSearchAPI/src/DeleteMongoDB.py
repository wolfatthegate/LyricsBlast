import TextCleaner
import pymongo
import nltk
import blast
import sys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['LyricsDB']
lyricTbl = mydb['Lyrics']
  
myquery = { "lyrics": { "$exists": "true" }, "$expr": { "$gt": [ { "$strLenCP": "$lyrics" }, 35000 ]}}
myquery = {'$or':[{'name': "George Eliot"}, {'name': "Gustave Flaubert"}, {'name': "Mr. Robot"}, {'name': 'URLtv'}, {'name': 'Willa Cather'}]}
myquery = {'$or':[{'name': '101Barz'}, {'name': 'Ralph Ellison'}, {'name': 'King of the Dot'}, {'name': 'Albert Camus'}, {'name':'Roger Williams'}]}
myquery = {'$or':[{'name': 'FilmOn.TV'}, {'name': 'Aldous Huxley'}, {'name': 'Genius Deutschland'}, {'name': 'Genius Users'}, {'name':'American Red Cross'}]}
myquery = {'$or':[{'name': 'Kollegah'}, {'name': 'William Faulkner'}, {'name': 'Samuel Taylor Coleridge'}, {'name': 'Emoji Genius'}, {'name':'BTS'}]}
myquery = {'$or':[{'name': 'David Sedaris'}, {'name': 'Rock Genius'}, {'name': 'Phantoms'}, {'name': '​jeffersuhn'}, {'name':'Oscar Wilde'}]}

["ich bin", "wird", "wied", "connais", "L'argent", "sauver", "la merde", "m'appelle", "ouais", "blessures", "seulement", "J'fous", "recette","j'rêve", "feuille", "J'ai", "Contractée", "m'dis"]
["t'aimes", "lèvres", "culotte", "après", "l'herbe", "cette"]
myquery = {'$or':[{'lyrics': {"$regex": "д"}}, {'lyrics': {"$regex": "siamo"}}, {'lyrics': {"$regex": "farai"}}]}
myquery = {'$text': {'$search': "cocaine"}}
myquery = {'lyrics3': {'$search': "cocaine"}}
print(str(lyricTbl.find(myquery).count()))
