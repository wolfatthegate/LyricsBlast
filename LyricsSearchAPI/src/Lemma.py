from nltk.corpus import wordnet
import inflect

# synonyms = []
# antonyms = []
# 
# for syn in wordnet.synsets("heroins"):
#     for l in syn.lemmas():
#         synonyms.append(l.name())
#         if l.antonyms():
#             antonyms.append(l.antonyms()[0].name())
#  
# print(set(synonyms))
# print(set(antonyms))

engine = inflect.engine()
words = ["smell", "hate"]
Dict = {}

def lemmatize(word):
    forms = set() #We'll store the derivational forms in a set to eliminate duplicates
    for happy_lemma in wordnet.lemmas(word): #for each "happy" lemma in WordNet
        forms.add(happy_lemma.name()) #add the lemma itself
        for related_lemma in happy_lemma.derivationally_related_forms(): #for each related lemma
            forms.add(related_lemma.name()) #add the related lemma
            
    forms.add(engine.plural(word))
              
    if forms.__len__() > 0 :
        Dict[word] = forms

filepath = 'tweets/4000Terms.txt'
with open(filepath, 'r') as f:
    for line in f:
        line = line.strip()
        lemmatize(line)

print(Dict)