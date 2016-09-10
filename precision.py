# -*- coding: utf-8 -*-
from __future__ import division

from PCFG_cambios import PCFGChino as pcfg
import string
import io

import nltk
from nltk.corpus import sinica_treebank as sinica



def tree2set(tree):
    if '()' == tree:
        return []
    par= []
    size= len(str(tree))
    palabras= 0
    for c in range(size):  # Para cada caracter del árbol
        if ')' == tree[c] and tree[c-1] in string.hexdigits:
        	palabras += 1
        if '(' == tree[c]:
            ini= c+1
            tag= ''
            flag= False
            num_abiertos= 0
            num_palabras= 0
            for c1 in range(ini,size):
               ## Al final de cada paréntesis suelen estar las palabras
                if ')' == tree[c1] and tree[c1-1] in string.hexdigits:
                    num_palabras += 1
                ## Antes de un nuevo paréntesis o una palabra siempre hay un tag
                if ('(' == tree[c1] or '\\' == tree[c1]) and not flag:
                    tag= tree[ini:c1]
                    flag= True  # Así solo entra una vez por cada paréntesis
                ## En caso de llegar al final del parentesis
                if ')' == tree[c1] and num_abiertos == 0:
##                    print [tag, (palabras, num_palabras+palabras)]
                    par.append([tag,(palabras, num_palabras+palabras)])
                    break
                elif ')' == tree[c1]:
                    num_abiertos -= 1
                elif '(' == tree[c1]:
                    num_abiertos += 1
    return par


def parseval(corpus_set, own_set):
    size_own= len(own_set)
    num= 0
    for o in own_set:
        if o in corpus_set:
            num += 1
    if size_own == 0:
        return 0
    else:
        return num/size_own
            
def labeled_recall(corpus_set, own_set):
    size_corpus= len(corpus_set)
    num= 0
    for o in corpus_set:
        if o in own_set:
            num += 1
    return num/size_corpus

def lp_lr(corpus_set, own_set):
    size_corpus= len(corpus_set)
    size_own= len(own_set)
    num= 0
    for o in corpus_set:
        if o in own_set:
            num += 1
    num= num*2
    return num/(size_corpus+size_own)


def compare_trees(ttree, own_tree, fileStream):
    ## Procesa ambos árboles para que tengan el mismo formato
    ##      Calcula el % de acierto con los árboles generados
    ##      con valores [0:1]
    f= fileStream
    corpus_tree= []
    for j in ttree:
        corpus_tree.append( str(j) )
    corpus_tree= "".join(corpus_tree)
    own_tree= str(own_tree)
    pos= 0
    num= 0
    while (num < 2) & (pos < len(own_tree)):
        if '(' == list(own_tree)[pos]:
            num += 1
        pos += 1
    own_tree= own_tree[pos-1:]  # Se elimina la parte inicial que sobra
    pos= len(own_tree)
    num= 0
    while (num < 2) & (pos >= 0):
        if ')' == list(own_tree)[pos-1]:
            num += 1
        pos -= 1
    own_tree = own_tree[:pos]   # Se elimina la parte final que sobra
    a= "".join(str(own_tree).split())   # Se eliminan espacios y saltos de línea
    it= 0
    while it < len(a):
        if a[it] == 'u':
            if (a[it-1] != '\\') & (a[it+1] in string.hexdigits):
                a= a[:it] + '\\' + a[it:]
        it += 1
##    print "A",a
    f.write('Generado: '+str(a)+'\n')
    b= "".join(corpus_tree.split())     # Se eliminan espacios y saltos de línea
    s = list(b)
    while(u'[' in s):
        s.remove(u'[')
    while(u']' in s):
        s.remove(u']')
    while(u'+' in s):
        s.remove(u'+')
    while(u',' in s):
        s.remove(u',')
    while(u'}' in s):
        s.remove(u'}')
    b= "".join(s)
##    print "B",b
    f.write('Corpus: '+str(b)+'\n')
    r1= tree2set(str(a))
##    print "Tree A: "+str(r1)
    r2= tree2set(str(b))
##    print "Tree B: "+str(r2)
    return lp_lr(r2,r1)#parseval(r2,r1), labeled_recall(r2,r1),lp_lr(r2,r1)



##    ## TRAIN + TEST 1000
##   
size= 1000        
frases= sinica.sents()
arboles= sinica.parsed_sents()
train= pcfg(size)
train.carga_pesos()

with open('gramatica1000total.txt','r') as g:
    gramatica=g.readlines()
    
train.carga_gramatica(gramatica)

F1= 0
f= open('t1000.txt', 'w')
##f= open('Knownwords.txt', 'w')
for i in range(size):
##    print i
    f.write(str(i)+'\n')
##    print '\n\n'
    frase= frases[i]
    for j in range(len(frase)):
        frase[j]= unicode(repr(frase[j])[2:-1])
##    print frase
    ## f For
    ## Se intenta hacer el parsing de la frase
    try:
        resultado= train.parse2tree(frase)
    ## Si no puede hacer el parsing se compara con un árbol
    ## que evidentemente no es correcto
    except Exception as err:
       resultado= ['()']
       print "Fallo en el parsing"
       print err
    ## f Exception
    try:
        own_tree= resultado[0]
    except IndexError:
        resultado= ['()']
    ## f Exception
    t_F1= compare_trees(str(arboles[i]), str(list(resultado)[0]), f)
    f.write('F1 '+str(t_F1)+'\n\n')
    ## f If
    F1= F1 + t_F1
## f For
f.write("F1: "+str(F1/size))
f.close()
print "Fin 1000"


    ## TRAIN + TEST 2000
   
size2= 2000        
train= pcfg(size2)
train.carga_pesos()

with open('gramatica2000total.txt','r') as g:
    gramatica2=g.readlines()
    
train.carga_gramatica(gramatica2)

F1= 0
f= open('t2000.txt', 'w')
##f= open('Knownwords.txt', 'w')
for i in range(size2):
##    print i
    f.write(str(i)+'\n')
##    print '\n\n'
    frase= frases[i]
    for j in range(len(frase)):
        frase[j]= unicode(repr(frase[j])[2:-1])
##    print frase
    ## f For
    ## Se intenta hacer el parsing de la frase
    try:
        resultado= train.parse2tree(frase)
    ## Si no puede hacer el parsing se compara con un árbol
    ## que evidentemente no es correcto
    except Exception as err:
       resultado= ['()']
       print "Fallo en el parsing"
       print err
    ## f Exception
    try:
        own_tree= resultado[0]
    except IndexError:
        resultado= ['()']
    ## f Exception
    t_F1= compare_trees(str(arboles[i]), str(list(resultado)[0]), f)
##    print temp
    f.write('F1 '+str(t_F1)+'\n\n')
    ## f If
    F1= F1 + t_F1
## f For
f.write("F1: "+str(F1/size2))
f.close()
print "Fin 2000"


    ## TRAIN + TEST 5346
   
size3= 5346       
train= pcfg(size3)
train.carga_pesos()

with open('gramatica5346total.txt','r') as g:
    gramatica3=g.readlines()
    
train.carga_gramatica(gramatica3)

F1= 0
f= open('t5346.txt', 'w')
##f= open('Knownwords.txt', 'w')
for i in range(size3):
##    print i
    f.write(str(i)+'\n')
##    print '\n\n'
    frase= frases[i]
    for j in range(len(frase)):
        frase[j]= unicode(repr(frase[j])[2:-1])
##    print frase
    ## f For
    ## Se intenta hacer el parsing de la frase
    try:
        resultado= train.parse2tree(frase)
    ## Si no puede hacer el parsing se compara con un árbol
    ## que evidentemente no es correcto
    except Exception as err:
       resultado= ['()']
       print "Fallo en el parsing"
       print err
    ## f Exception
    try:
        own_tree= resultado[0]
    except IndexError:
        resultado= ['()']
    ## f Exception
    t_F1= compare_trees(str(arboles[i]), str(list(resultado)[0]), f)
##    print temp
    f.write('F1 '+str(t_F1)+'\n\n')
    ## f If
    F1= F1 + t_F1
## f For
f.write("F1: "+str(F1/size3))
f.close()
##print LP/size
##print LR/size
print "Fin 5346"
