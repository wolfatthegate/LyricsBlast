from difflib import SequenceMatcher as SM
from nltk.util import ngrams

class needleAndHay:

    def searchTheNeedle(self, needle, hay, threshold):
        
        needle_length  = len(needle.split())
        max_sim_val    = 0
        max_sim_string = u""
        
        for ngram in ngrams(hay.split(), needle_length + int(.2*needle_length)):
            hay_ngram = u" ".join(ngram)
            similarity = SM(None, hay_ngram, needle).ratio() 
            if similarity > max_sim_val:
                max_sim_val = similarity
                max_sim_string = hay_ngram
        
        if (max_sim_val > threshold):
            print (str(round(max_sim_val,2)) + ' ' + max_sim_string)
            return True