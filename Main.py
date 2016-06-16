import nltk
from nltk.corpus import sinica_treebank as sinica

import Segmenter
from Segmenter import sent_segment
import PCFG
from PCFG import PCFGChino
import time

####################################
## ESTA PARTE NO ES IMPORTANTE PARA TESTEAR EL PARSER
tagged_sents= sinica.tagged_sents()
sents= sinica.sents()

size= int(len(tagged_sents) * 0.9)
train_set= tagged_sents[:size]
test_set= tagged_sents[size:]
##trigram_tagger= nltk.TrigramTagger(train_set)
##score= trigram_tagger.evaluate(test_set)
print "Entrenando"
ini= time.time()
t0= nltk.DefaultTagger('Nab')
t1= nltk.UnigramTagger(train_set, backoff=t0)
t2= nltk.BigramTagger(train_set, backoff=t1)
t3= nltk.TrigramTagger(train_set, backoff=t2)
fin= time.time()
score= t3.evaluate(test_set)
print("Entrenamiento terminado ", str(fin-ini))
print "Evaluation Tagger= ",score
####################################
## Se crea el parser
testing= PCFGChino(15)
testing.carga_pesos()
reglas= testing.grammar2string().decode('utf-8')
##print "Tree Grammar completed:"
##print reglas
testing.carga_gramatica(reglas)
##
##print "###########################"
##print "## Testing on a sentence ##"
##                ###################################
##sent= '按了門鈴'
##print sent.decode()
##done= sent_segment(sent)
##print "Segmented looks like:"
##for o in done: print o
##print "We try to tag each word"
##ts= tag_sent(t3, done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
##for i in range(len(done)):
##    done[i]= unicode(repr(done[i])[2:-1])
##    print done[i]
##print "Time to parse:"
##resul= testing.parse2tree(done)
##resul2= testing.parse2tree2(done)
##for t in resul:
##    print t
##print "otro parser"
##for t2 in resul2:
##    print t2
##                ###################################
sent= '卻沒有任何動靜'
print sent
done= sent_segment(sent)
##print "Segmented looks like:"
##for o in done: print o
##print "We try to tag each word"
ts= t3.tag(done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
for i in range(len(done)):
    done[i]= unicode(repr(done[i])[2:-1])
##    print done[i]

print "Time to parse:"
resul= testing.parse2tree(done)
##resul2= testing.parse2tree2(done)
for t in resul:
    print t
##print "otro parser"
##for t2 in resul2:
##    print t2
                ###################################
##sent= '我的哥哥就去工作'
##print sent
##done= sent_segment(sent)
##print "Segmented looks like:"
##for o in done: print o
##print "We try to tag each word"
##ts= tag_sent(t3, done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
##for i in range(len(done)):
##    done[i]= unicode(repr(done[i])[2:-1])
##    print done[i]
##
##print "Time to parse:"
##resul= testing.parse2tree(done)
##for t in resul:
##    print t
##print "###########################"
##print "## Testing on a sentence ##"
##sent= '\u537b\u6c92\u6709\u4efb\u4f55\u52d5\u975c'
##done= sent_segment(sent)
##print "Segmented looks like:"
##for o in done: print o#.decode('utf-8'), o
##print "We try to tag each word"
##ts= tag_sent(t3, done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
##done= ['\u537b', '\u6c92\u6709', '\u4efb\u4f55', '\u52d5\u975c']
##print "Time to parse:"
##resul= testing.parse2tree(done)
##for t in resul:
##    print t

    
##sent= '我的哥哥就去工作'
##done= sent_segment(sent)
##print "Segmented looks like:"
##for o in done: print o.decode('utf-8')
##print "#################"
##print "We try to tag each word"
##ts= tag_sent(t3, done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
##print "Time to parse:"
##resul= testing.parse2tree(done)
##for t in resul:
##    print t
##print "#################"
##print "We try to tag each word"
##ts= tag_sent(t3, done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
##print "#################"
##print "#################"
##sent= '我朋友的奶奶真可爱'
##done= sent_segment(sent)
##print "Segmented looks like:"
##for o in done: print o.decode('utf-8')
##print "#################"
##print "We try to tag each word"
##ts= tag_sent(t3, done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
##print "#################"
##print "#################"
##sent= '他的perro很漂亮'
##done= sent_segment(sent)
##print "Segmented looks like:"
##for o in done: print o.decode('utf-8')
##print "#################"
##print "We try to tag each word"
##ts= tag_sent(t3, done)
##for t in ts: print ''+t[0].decode('utf-8')+': '+t[1]
##print "#################"
##print "#################"
