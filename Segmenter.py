## -*- coding: utf-8 -*-
import nltk
from nltk.corpus import sinica_treebank as sinica
import string
import time

non_hanzi= list(string.printable)
non_hanzi.append("。")
non_hanzi.append("！")
non_hanzi.append("？")
non_hanzi.append("，")
corpus_bank = set(sinica.words())

def sent_segment(sentence):
    palabras=[]
    sentence= sentence.decode('utf-8')
    # print sentence
    num_characters= len(sentence)
    if num_characters==0:
        return []
    ##
    ## Checking if what we got to analyze is not a hanzi to skip it
    ini_non_hanzi= 0
    fin_non_hanzi= 0
    not_a_hanzi= False
    # Go through the non-hanzi text until i find something different
    while((fin_non_hanzi < num_characters) and (sentence[fin_non_hanzi] in non_hanzi)):
        not_a_hanzi= True
        fin_non_hanzi+=1
    if not_a_hanzi:
        palabras.append(sentence[ini_non_hanzi:fin_non_hanzi])  # Añade el conjunto con caracteres latinos y puntuación como una palabra entera
        if(fin_non_hanzi >= num_characters):
            return palabras
        sentence= sentence[fin_non_hanzi:num_characters]        
    ## end if
    for i in range(num_characters):
##        print sentence[:num_characters-i].decode('utf-8')
        temp= sentence[:num_characters-i].decode('utf-8')
        # print temp in corpus_bank
        # print temp
        if(temp in corpus_bank):
            palabras.append(temp)
            # If there are characters left to be checked after 'num_characters-i'...
                # ...the function segmenter is called with what remains unchecked
            lista= sent_segment(sentence[num_characters-i: num_characters])
            palabras+=lista
            break;
        else:
            if (i == num_characters-1):
                palabras.append(sentence[:num_characters])
                return palabras
            ## end if
        ## end if
    ## end for    
    return palabras
## end def
