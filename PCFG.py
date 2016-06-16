from __future__ import division
import nltk
from nltk.corpus import sinica_treebank as sinica
from nltk import Tree
from nltk.grammar import Nonterminal



class PCFGChino():
    " Lee los árboles del corpus y lo transforma en una gramática y un lexicon "
    sent_test= sinica.parsed_sents()#[24]
    __trees__= []               ##Lista de todos los árboles
    __productions__= []         ## Lista de todas las producciones encontradas
    __dictionary__= dict()      ## [Producción: probabilidad]
    __grammar__= []             ## Gramática
    __roots__= dict()           ## Términos iniciales
    
    def __init__(self, num):
        self.carga_pesos()
        for s in self.sent_test[:num]:
            self.__trees__.append(s)
            for i in s.productions():
                self.__productions__.append(i)
        ## Cojo la raiz del árbol
        for t in self.sent_test[:num]:
            p= t.productions()[0].lhs()
            if not self.__roots__.has_key(p):
		contador= 0
		for t2 in self.sent_test[:num]:
			if t2.productions()[0].lhs() == p:
				contador = contador + 1
                self.__roots__[p]= (contador/num)

    
    def carga_pesos(self):
        for p in self.__productions__:                   ## En cada producción
            if not self.__dictionary__.has_key(p):
                contador_label= 0
                contador_prod= 0
                for o in self.__productions__:
                    if p.lhs() == o.lhs():
                        contador_label += 1
                    if o == p:
                        contador_prod += 1
                self.__dictionary__[p]= (contador_prod/contador_label)


    def grammar2string(self):
        grammar= ""
        for r in self.__roots__.items():
            grammar= grammar+'ROOT -> '+str(r[0])+' ['+str(r[1])+']\n'
        for i in self.__dictionary__.items():
            ## Hay que tener cuidado con algunos caracteres que pueden complicar
            ## el parsing
            j= str(i[0]).decode('utf-8')
            s= list(j)
            if '\\' in s:
                flag= 1
                for c in s:
                    if flag:                ## Cuando flag= 1 podemos sustituir las '\\'
                        if c == '\\':
                            s[s.index(c)]= '-'
                        elif c == '\'':
                            flag= 0         ## En terminales no podemos sustituir su '\\'
                    else:
                        if c == '\'':
                            flag= 1
                j= "".join(s)
            grammar = grammar+j+' ['+str(i[1])+']\n'
        return grammar.decode('utf-8')

    def carga_gramatica(self, grammar):
        self.__grammar__= nltk.PCFG.fromstring(grammar)

    def parse2tree(self, sentence):
        viterbi_parser= nltk.ViterbiParser(self.__grammar__)
        parses= []
        for tree in viterbi_parser.parse(sentence):
            parses.append(tree)
        return parses

    def parse2tree2(self, sentence):
        parser= nltk.ChartParser(self.__grammar__)
        parses= []
        for tree in parser.parse(sentence):
            parses.append(tree)
        return parses
