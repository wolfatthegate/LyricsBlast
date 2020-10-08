import json
import re
import string
import vincent
import TextCleaner

from nltk.corpus import stopwords 
from collections import Counter


def remove_url(txt):
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

 
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')')
emoticon_re = re.compile(r'^'+emoticons_str+'$')

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(preprocess(tweet))

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

more_stop = ['’', '…', '1', '2', '“', '”', "i'm", '', '\u200d']
#\u200d - zero width joiner

final_stop = stop + more_stop

opioids = ['crack', 'doors & fours', 'loads', 'pancakes and syrup', 'captain cody', 'cody', 'lean', 'schoolboy', 'sizzurp', 'purple drank', 'apache', 'china girl', 'china white', 'dance fever', 'friend', 'good- fella', 'jackpot', 'murder 8', 'tango and cash', 'tnt''h', 'smack', 'dope', 'horse', 'skag', 'junk', 'black tar', 'big h', 'brown sugar', 'mud', 'dragon', 'boy', 'mexican brown', 'thunder', 'skunk''vike', 'watsons', 'watson-387', 'vics', 'vicos', 'hydros', 'lorris', 'fluff', 'scratch', 'norco', 'idiot pills', 'tabs', '357s','d', 'dillies', 'footballs', 'juice', 'herbal speedball', 'biak-biak', 'ketum kahuam', 'ithang', 'thom','demmies', 'm', 'miss emma', 'monkey', 'white stuff', 'o.c.', 'oxycet', 'oxycotton', 'oxy', 'hillbilly heroin', 'percs', 'o', 'ox', 'blue', '512s', 'kickers', 'killers', 'biscuits', 'blue heaven', 'blues', 'mrs. o', 'o bomb', 'octagone', 'stop signs'] 

excluded = ['h', 'd', 'o', 'm']

fname = 'tweets/nys_tweets_filtered_2017_Q3.json'

cleaner = TextCleaner.TextCleaner()

with open(fname, 'r') as f:
    count_all = Counter()

    for line in f:
        
        tweet = json.loads(line)
        # Create a list with all the terms
        # terms_stop = [term for term in preprocess(tweet['text'].lower()) if term[0] not in final_stop]
        # Update the counter
        # count_all.update(terms_stop)
         
        terms_count = [term for term in preprocess(tweet['text'].lower()) if term[0] in opioids and term[0] not in excluded]
        
        count_all.update(terms_count)
         
    # Print the first 5 most frequent words
    most_common_list = count_all.most_common(100)

    print(most_common_list)
    



