import blast
# import nltk

seq1 = 'AAACGGTAATTGACAGTAATAGACCAAACCCTAGATAGACTACTAATTACCCAGTAACCAGAATGATTAGTTG'
seq2 = 'CGAATTACCACCAGGATACCAAACAACACCAAAAGTAAACACGGATACAGGACATAAACAACGGAACATTACC'

seq0 = 'Frankly My Dear I dont give a damn'
seq2 = 'frankly My Dear I give a damn' #tweet 

blaster = blast.blast()
result = blaster.SMWalignment(seq0, seq2, 0.65)

print('   db string: ' + result[0])
print('query string: ' + result[1])
print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
print('')
