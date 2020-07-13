import blast
# import nltk

seq1 = 'AAACGGTAATTGACAGTAATAGACCAAACCCTAGATAGACTACTAATTACCCAGTAACCAGAATGATTAGTTG'
seq2 = 'CGAATTACCACCAGGATACCAAACAACACCAAAAGTAAACACGGATACAGGACATAAACAACGGAACATTACC'

seq0 = 'provider of the back drop music for the crack rock user'
seq2 = 'Provider of the backdrop music' #tweet 

blaster = blast.blast()
result = blaster.SMWalignment(seq0, seq2, 0.65)

print('   db string: ' + result[0])
print('query string: ' + result[1])
print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
print('')


seq0 = 'provider of the back drop music for the crack rock user'
seq2 = 'For the crack rock user and the mascot Earl' #tweet 

blaster = blast.blast()
result = blaster.SMWalignment(seq0, seq2, 0.65)

print('   db string: ' + result[0])
print('query string: ' + result[1])
print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
print('')