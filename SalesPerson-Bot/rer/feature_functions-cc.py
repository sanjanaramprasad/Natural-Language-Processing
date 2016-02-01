'''
feature_functions.py
Implements the feature generation mechanism
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014

6th Dec: Org gazeteer added
7th Dec: 
'''
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
import datetime
import collections


all_tags=['price_query','feature_query','comparison','interest_intent','irrelevant','acknowledgement','disagreement','greeting','agreement']
brand_product_bigrams_dict = [] # use the web service from Ner_client to get this: ner.get_brand_product_bigrams() # gazeteer based 7th Dec 2014
product_names = []
for v in get_brand_product_bigrams_dict().values():
    for v1 in v:
        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token
for p in product_names:
    product_name_tokens.extend(p.split())


class FeatureFunctions(object):
    def __init__(self, tag_list = None):
        self.wmap = {}
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        self.fdict = {}
        for k, v in FeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    self.flist[k] = v # .append(v)
                    tag = k[1:].split("_")[0]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val

        #self.all_tags = self.fdict.keys()        
        return

    def set_wmap(self, sents): # given a list of words sets wmap
        for i in range(len(sents)):
            self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
        return

    def check_list(self, clist, w):
        #return 0
        w1 = w.lower()
        for cl in clist:
            if w1 in cl:
                return 1
        return 0

    #------------------------------- Phone tag ---------------------------------------------------------
    # The following is an example for you to code your own functions
    # returns True if wi is in phones tag = Phone
    # h is of the form {'ta':xx, 'tb':xx, 'wn':xx, 'i':xx}
    # self.wmap provides a list of sentences (tokens) where each element in the list is a dict {'words': word_token_list, 'pos_tags': pos_tags_list}
    # each pos_tag is a tuple returned by NLTK tagger: (word, tag)
    # h["wn"] refers to a sentence number
    
    def fPriceQuery_1(self, h, tag):
        if tag != "price_query":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if ("Price" in h[0][relatedTags]):
            return 1
        else:
            return 0


    #------------------------------- Functions for Feature_query tag ---------------------------------------------------------

    def fFeatureQuery_1(self, h, tag):
        if tag != "feature_query":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if ("Feature" in h[0][relatedTags])):
            return 1
        else:
            return 0

    
    #------------------------------- Functions for Comparison tag ---------------------------------------------------------  

    def fComparison_1(self, h, tag):
        if tag != "comparison":
            return 0
        #words = self.wmap[h["wn"]]['words']
        l=h[0]['relatedTags']
        counter=collections.Counter(l)  
        if (dict(counter.most_common(len(l)))['Org']):
            return 1
        else:
            return 0

    def fComparison_2(self,h,tag):
        if tag != "comparison":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if (dict(counter.most_common(len(l)))['Family'])):
            return 1
        else:
            return 0

    def fComparison_3(self, h, tag):
        if tag != "comparison":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if (dict(counter.most_common(len(l)))['OS']):
            return 1
        else:
            return 0

    #------------------------------- Functions for Intent_query tag ---------------------------------------------------------        

    def fIntentQuery_1(self, h, tag):
        if tag != "intent_query":
            return 0
        #words = self.wmap[h["wn"]]['words']        
	words = map(lambda x:x["word"],h[0]["sentence"])
        if (("buy" in words) or ("purchase" in words)):
            return 1
        else:
            return 0

    
    #------------------------------- Functions for Irrelevant tag ---------------------------------------------------------

    def fIrrelevant_1(self, h, tag):
        tags_copy=all_tags[:]
        tags_copy.remove('irrelevant')
        if tag != "irrelevant":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if (tag not in tags_copy)):
            return 1
        else:
            return 0

    def rule_Acknowledgement(self,h,tag):
        words = map(lambda x:x["word"],h[0]["sentence"])
        if (("thanks" in words) or ("thank" in words) or ('yes' in words)):
            return 1
        else:
            return 0
    
    def rule_Disagreement(self,h,tag):
        words = map(lambda x:x["word"],h[0]["sentence"])
        if (("not" in words) or ("no" in words) or ('else' in words) or ('alternative' in words)):
            return 1
        else:
            return 0
    
    def rule_Greeting(self,h,tag):
        words = map(lambda x:x["word"],h[0]["sentence"])
        if (("hi" in words) or ('hello' in words) or ('hey' in words)):
            return 1
        else:
            return 0

    def rule_Agreement(self,h,tag):
        words = map(lambda x:x["word"],h[0]["sentence"])
        if (("true" in words) or ("yes" in words) or ('indeed' in words)):
            return 1
        else:
            return 0
if __name__ == "__main__":
    pass
