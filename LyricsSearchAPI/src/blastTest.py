import blast
# import nltk

seq1 = 'AAACGGTAATTGACAGTAATAGACCAAACCCTAGATAGACTACTAATTACCCAGTAACCAGAATGATTAGTTG'
seq2 = 'CGAATTACCACCAGGATACCAAACAACACCAAAAGTAAACACGGATACAGGACATAAACAACGGAACATTACC'

seq0 = 'And he grabs me he has me by my heart' #lyric dB line 1
seq2 = 'he loves me with every beat of his cocaine heart' #tweet 

blaster = blast.blast()
result = blaster.SMWalignment(seq0, seq2, 0.70)
print('      str1:   ' + seq0)
print('      str2:   ' + seq2)
print('   db string: ' + result[0])
print('query string: ' + result[1])
print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
print('')
