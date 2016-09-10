from __future__ import division
import nltk
from nltk.corpus import sinica_treebank as sinica
from nltk import Tree
from nltk.grammar import Nonterminal
import string



class PCFGChino():
    #7 Lee los árboles del corpus y lo transforma en una gramática y un lexicon "
    sent_test= sinica.parsed_sents()
    __trees__= []               ## Lista de todos los árboles
    __productions__= []         ## Lista de todas las producciones
    __dictionary__= dict()      ## [Producción: probabilidad]
    __grammar__= []             ## Gramática
    __roots__= dict()           ## Términos iniciales
    __preterminals__= []
    __words__= []
    __unknowns__= dict()

    ## Tagging
    train_set= sinica.tagged_sents()[:int(len(sinica.tagged_sents())*0.9)]
    t0= nltk.DefaultTagger('Nab') 
    t1= nltk.UnigramTagger(train_set, backoff= t0)
    t2= nltk.BigramTagger(train_set, backoff= t1)
    t3= nltk.TrigramTagger(train_set, backoff= t2)
    
    def __init__(self, num):
        ## De cada frase se extraen todos los
        ## árboles y todas las producciones
        for s in self.sent_test[:num]:
            self.__trees__.append(s)    
            for i in s.productions():
                self.__productions__.append(i)
                ## Si encuentro un terminal guardo su tag y el token
                ## en la lista correspondiente
                if '\'' in str(i):
                    self.__words__.append(str(i)[str(i).index('\'')+1:-1])
                    self.__preterminals__.append(str(i.lhs()))
        # f for
        ## Se añade a cada posible preterminal una producción a unknown
        for p in self.__preterminals__:
##            QUIZA EDITAR AQUI LOS TAGS
            self.__unknowns__[str(p)]= str(p)+' -> \''+str(p)+'_unknown\''

        ## En cada árbol se extrae la raíz y se calcula
        ## la probabilidad que tiene dicha raíz
        for t in self.sent_test[:num]:
            p= t.productions()[0].lhs()
            if not self.__roots__.has_key(p):
                contador= 0
                for t2 in self.sent_test[:num]:
                    if t2.productions()[0].lhs() == p:
                        contador = contador + 1
                self.__roots__[p]= (contador/num)   ## Cálulo de probabilidad

    
    def carga_pesos(self):
        ## Se recorre la lista de producciones
        ## calculando y almacenando sus pesos
        for p in self.__productions__:
            ## Si la producción no está en el diccionario...
            if not self.__dictionary__.has_key(p):
                contador_label= 0
                contador_prod= 0
                ## ... se calcula su probabilidad
                for o in self.__productions__:
                    ## si la parte izquierda es la misma
                    if p.lhs() == o.lhs():
                        contador_label += 1
                    ## si la producción se repite
                    if o == p:
                        contador_prod += 1
                ## Añadir aquí la producción a unknown con su probabilidad
                if self.__unknowns__.has_key(str(p.lhs())):
                    contador_label += 1
                    if not self.__dictionary__.has_key(self.__unknowns__[str(p.lhs())]):          ## Si aun no se ha añadido el unknown del tag...
                        self.__dictionary__[self.__unknowns__[str(p.lhs())]]= (1/contador_label)  ## ... se añade ahora con su probabilidad
                self.__dictionary__[p]= (contador_prod/contador_label)  ## Cálculo de probabilidad


    def grammar2string(self):
        ## Las producciones de la gramática se procesan formando
        ## un string que representa todas las reglas de la gramática
        grammar= ""
        ## Se añade el símbolo inicial, común a todos los árboles
        for r in self.__roots__.items():
            grammar= grammar+'ROOT -> '+str(r[0])+' ['+str(r[1])+']\n'
        ## Se añade para cada tag una producción Tag -> unknown
##        for t in self.sent_test[:num]
        
        ## Se procesa cada regla de la gramática dándole el formato adecuado
        for i in self.__dictionary__.items():
            ## Hay que tener cuidado con algunos caracteres
            ## que viterbi no puede procesar, y han de eliminarse
            j= str(i[0]).decode('utf-8')
            s= list(j)
            f = 0
            while(u'[' in s):
                s.remove(u'[')
            while(u']' in s):
                s.remove(u']')
            while(u'+' in s):
                s.remove(u'+')
            while(u',' in s):
                s.remove(u',')
            while(u'}' in s):
                s[s.index(u'}')] = '_'
            ## El caracter '\' ha de eliminarse de forma especial, porque los
            ## símbolos terminales lo usan, y en ellos no se debe eliminar
            if '\\' in s:
                flag= 1
                for c in s:
                    if flag:                ## Cuando flag= 1 podemos sustituir las '\'
                        if c == '\\':
                            s.remove(c)
                        elif c == '\'':
                            flag= 0         ## En terminales no podemos sustituir su '\\'
                    else:
                        if c == '\'':
                            flag= 1         ## Se termina el terminal que se estaba leyendo
            j= "".join(s)
            grammar = grammar+j+' ['+str(i[1])+']\n'
        ## f for
        return grammar.decode('utf-8')

    def carga_gramatica(self, grammar):
        self.__grammar__= nltk.PCFG.fromstring(grammar)

    def parse2tree(self, sentence):
        s= sentence
        viterbi_parser= nltk.ViterbiParser(self.__grammar__)
        parses= []
        flag= False
        ## Ahora falta añadir la sustitución
        for it in range(len(s)):
            if s[it] not in self.__words__: ## Si falta alguna palabra
                flag= True
        if flag:                            ## Se sustituye por el unknown de su tag
            tsent= self.t3.tag(s)
            for i in range(len(s)):
                if str(s[i]) not in self.__words__:
                    s[i]= str(tsent[i][1])+'_unknown'
        for tree in viterbi_parser.parse(sentence):
            parses.append(tree)
        return parses

## 1. Crear la gramática con los preterminales derivando a 'unknown'
## 1. Si la palabra es desconocida, intentar calcular su tag
## 2. Con su tag, sustituir la palabra por el 'unknown' correspondiente
## 3. Obtener el árbol con la frase


