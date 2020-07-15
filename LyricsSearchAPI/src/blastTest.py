import blast
# import nltk

seq1 = 'AAACGGTAATTGACAGTAATAGACCAAACCCTAGATAGACTACTAATTACCCAGTAACCAGAATGATTAGTTG'
seq2 = 'CGAATTACCACCAGGATACCAAACAACACCAAAAGTAAACACGGATACAGGACATAAACAACGGAACATTACC'

seq0 = 'cocaine white like justin bieber bitch I might show the racks and tease her bitch'
seq2 = 'cocaine white like justin bieber bitch ' #tweet 


seq0 =  "Provider of the back drop music for the crack rock user"
seq2 =  "For the crack rock user and the mascot Earl"
blaster = blast.blast()
result = blaster.SMWalignment(seq0, seq2, 0.65)

print('   db string: ' + result[0])
print('query string: ' + result[1])
print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
print(' first half score: ' + str(round(result[4], 2)))
print('second half score: ' + str(round(result[5], 2)))

