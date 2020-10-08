import blast
# import nltk

seq1 = 'AAACGGTAATTGACAGTAATAGACCAAACCCTAGATAGACTACTAATTACCCAGTAACCAGAATGATTAGTTG'
seq2 = 'CGAATTACCACCAGGATACCAAACAACACCAAAAGTAAACACGGATACAGGACATAAACAACGGAACATTACC'

seq0 = 'cocaine white like justin bieber bitch I might show the racks and tease her bitch'
seq2 = 'cocaine white like justin bieber bitch ' #tweet 

seq0 =  "@fuckyouricky I've been selling crack since like the 5th gradeeee"
seq2 =  "I been selling crack since like the fifth grade"
blaster = blast.blast()
result = blaster.SMWalignment(seq0, seq2, 0.65)

print('   db string: ' + result[0])
print('query string: ' + result[1])
print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
print(' first half score: ' + str(round(result[4], 2)))
print('second half score: ' + str(round(result[5], 2)))


# seq0 =  "Wtf u take me for, u smoking crack? Before I do that I beg my ex to take me back"
# seq2 =  "Fore I do that, I'd beg Mariah to take me back"
# blaster = blast.blast()
# result = blaster.SMWalignment(seq0, seq2, 0.65)
# 
# print('   db string: ' + result[0])
# print('query string: ' + result[1])
# print(' Align Score: ' + str(round(result[2],2)) + '/1.0 (' + str(result[3]) + ' words matched)')
# print(' first half score: ' + str(round(result[4], 2)))
# print('second half score: ' + str(round(result[5], 2)))

