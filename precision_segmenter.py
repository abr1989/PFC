from __future__ import division
import nltk
from nltk.corpus import sinica_treebank as s
import Segmenter
from Segmenter import sent_segment


frases= s.sents()

def haz_uno(sentence):
    ## 'sentence' es una lista de caracteres sin codificar en utf8
    devolver= ""
    for i in sentence:
        devolver = devolver+ str(i).decode('utf-8')
    return devolver

def compare_both(a,b):
    ## 'a' siempre será la frase del corpus
    ## 'b' será la frase segmentada por mi tokenizer
    count= 0
    total= 0
    if len(a) <= len(b):
        for i in range(len(a)):
            if a[i] == b[i]:
                count = count + 1
    else:
        for i in range(len(b)):
            if a[i] == b[i]:
                count = count + 1
    return count/int(len(a))

##si= len(frases)/9
##for i in range(9):
##    tamano = si*(i+1) 
##    print "Para un total de ", tamano," frases"
##    media= 0
##    total= 0
##    for s in frases[:tamano]:
##        x= haz_uno(s)
##        x= sent_segment(x)
##        num= compare_both(s,x)
##        if num == 1:
##            total = total + 1
##        media = media + num
##    print "La media es: ", (media/tamano)
##    print "El % de acierto es: ", (total/tamano)
##
##
