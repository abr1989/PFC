__author__ = 'alber_000'
# -*- coding: utf-8 -*-
from Features import get_features
import nltk
from nltk.corpus import sinica_treebank as sinica

from time import gmtime, strftime, localtime
import time


from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.classify.decisiontree import DecisionTreeClassifier
from nltk.classify.util import accuracy, apply_features, log_likelihood
from nltk.classify.maxent import (MaxentClassifier, BinaryMaxentFeatureEncoding,
                                  TypedMaxentFeatureEncoding,
                                  ConditionalExponentialClassifier)

## Estudio de clasificación:
##  * NaiveBayesClassifier              
##  * DecisionTreeClassifier            
##  * MaxentClassifier                 

def load_featuresets():
    tagged_sents= sinica.tagged_sents()
    featuresets= []
    prev_tag= '<START>'
    prev2_tag= '<START>'

    for tagged_sent in tagged_sents:
        untagged_sent= nltk.tag.untag(tagged_sent)
        for i,(word, tag) in enumerate(tagged_sent):
            featuresets.append( (get_features(untagged_sent, i, prev_tag, prev2_tag), tag) )
            prev2_tag= prev_tag
            prev_tag= tag
    return featuresets

def naivebayes(featuresets):
    size= int(len(featuresets)) * 0.1
    train_set, test_set= featuresets[int(size):], featuresets[:int(size)]

    NB_classifier= nltk.NaiveBayesClassifier.train(train_set)
    return (NB_classifier, test_set)
    #return nltk.classify.accuracy(NB_classifier, test_set)
    
def decisiontree(featuresets):
    size= int(len(featuresets)) * 0.1
    train_set, test_set= featuresets[int(size):], featuresets[:int(size)]

    tree_classifier= nltk.classify.DecisionTreeClassifier.train(train_set, entropy_cutoff=0, support_cutoff=0)
    tree_classifier.pseudocode(depth=4)
    return (tree_classifier, test_set)
    #return nltk.classify.accuracy(Tree_classifier, test_set)
    
def maxent(featuresets, num):
    size= int(len(featuresets)) * 0.1
    train_set, test_set= featuresets[int(size):], featuresets[:int(size)]

    maxent_classifier= MaxentClassifier.train(train_set, trace= 3, max_iter= num)
    return (maxent_classifier, test_set)
    #return nltk.classify.accuracy(maxent_classifier, test_set)


#features= load_featuresets()
##ini1= time.time()
##(c, test_set)= naivebayes(features)
##num1= nltk.classify.accuracy(c, test_set)
##fin1= time.time()
##ini2= time.time()
##num2= eval_decisiontree(features)
##fin2= time.time()
##print "time stamp", time.time()
##for i in range(1,5):
##ini3= time.time()
##num3= eval_maxent(features, 0)
##fin3= time.time()
##print("Naive Bayes accuracy: ", num1," tiempo: ", (fin1-ini1))
##print("Decision Tree accuracy: ", num2," tiempo: ", (fin2-ini2))
##print("Maximum Entropy accuracy: ", num3," tiempo: ", (fin3-ini3))

