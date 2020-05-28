import blast
# import nltk

seq1 = 'AAACGGTAATTGACAGTAATAGACCAAACCCTAGATAGACTACTAATTACCCAGTAACCAGAATGATTAGTTG'
seq2 = 'CGAATTACCACCAGGATACCAAACAACACCAAAAGTAAACACGGATACAGGACATAAACAACGGAACATTACC'

seq0 = '(I smoke crack mutha fucka i dont sell it)' #lyric dB line 1
seq2 = 'I dont smoke crack motha fucka I sell it!!!' #tweet 

blaster = blast.blast()
result = blaster.SMWalignment(seq0, seq2, 0.65)
print('      str1:   ' + seq0)
print('      str2:   ' + seq2)
print('   db string: ' + result[0])
print('query string: ' + result[1])
print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
print('')
