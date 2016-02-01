
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
from ner_client import *
import datetime
import re
client = NerClient("1PI11CS004","g108")

phones = ["phone", "phones", "smartphone", "smartphones", "mobile", "tablet", "tablets", "phablet", "phablets"]
org_list = ['Samsung', 'Apple', 'Microsoft', 'Nokia', 'Sony', 'LG', 'HTC', 'Motorola', 'Huawei', 'Lenovo', 'Xiaomi', 'Acer', 'Asus', 'BlackBerry',
            'Alcatel', 'ZTE', 'Toshiba', 'Vodafone', 'T-Mobile', 'Gigabyte', 'Pantech', 'XOLO', 'Lava', 'Micromax', 'BLU', 'Spice', 'Prestigio',
            'verykool', 'Maxwest', 'Celkon', 'Gionee', 'vivo', 'NIU', 'Yezz', 'Parla', 'Plum']
org_list1 = [m.lower() for m in org_list]
os_list = ["iOS", "Android", "Windows", "Symbian", "Bada", "Unix", "Linux", "Ubuntu", "OS", "RIM", "Firefox"]
os_list1 = [m.lower() for m in os_list]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees"]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel" ]
all = []
all.extend(phones)
all.extend(org_list1)
all.extend(os_list)
all.extend(currency_symbols)
all.extend(size_list)

brand_product_bigrams_dict = [] # use the web service from Ner_client to get this: ner.get_brand_product_bigrams() # gazeteer based 7th Dec 2014
product_names = []
#for v in client.get_brand_product_bigrams_dict().values():
#    for v1 in v:
#        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token
family_set = set()
for p in product_names:
    product_name_tokens.extend(p.split())
    family_set.union({p.split()[0],})

class FeatureFunctions1(object):
    def __init__(self,sent, tag_list = None):
        self.wmap = {}
        self.sents = sent
        self.set_wmap(sent)
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        self.fdict = {}
        for k, v in FeatureFunctions1.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    self.flist[k] = v # .append(v)
                    tag = k[1:-1]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val
        self.supported_tags = self.fdict.keys() 
        #print self.supported_tags
        return
    def set_wmap(self, sents): # given a list of words sets wmap
        for i in range(len(sents)):
            self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
        return
		
    def evaluate(self, xi, tag):
        feats = []
        for t, f in self.fdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        #print str(feats)
        return feats
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
    
    def fprice_query1(self, h, rel):
        if u'?' in h["sentences"] and rel.lower() == "price_query":
            for i in h["updates"]:
                if i["tag"] == "Price":
                    return 1
            return 0	
        else:
            return 0
    '''def fprice_query2(self, h, rel):
        if u'?' in h["sentences"] and rel.lower() == "price_query":
            for i in h["updates"]:
                if str(i["word"]).lower() in currency_symbols:
                    return 1
            return 0
        else:
            return 0 '''
    #relation: feature_query
    def ffeature_query1(self, h, rel):
        if '?' in h["sentences"] and rel.lower() == "feature_query":
            for i in h["updates"]:
                if i["tag"] == "Feature":
                    return 1
            return 0					
        else:
            return 0
    #relation: interest_intent
    def finterest_intent1(self, h, rel):
        if 'interested' in h["sentences"] or 'interest' in h["sentences"] or 'interested' in h["sentences"] or rel.lower() == "interest_intent":
            return 1
        else:
            return 0
    #relation: comparison
	
	def finterest_intent2(self, h, rel):
		list_interest = ["Suggest","want","need","Show","buy","looking","available","like","get","exchange","suggest","show"]
		for i in list_interest:
			if i.lower() in h["sentences"] and (not self.ffeature_query_2(h,rel)) and (not self.ffeature_query_1(h, rel)):
				return 1
			else:
				return 0
			
    def fcomparison1(self, h, rel):
        if 'between' in h["sentences"] and 'and' in h["sentences"] and  rel.lower() == "comparison":
            return 1
        else:
            return 0
    '''def fcomparison2(self, h, rel):
        if 'better' in h["sentences"]:
            if rel.lower() == "comparison" or rel.lower() == "irrelevant":
                return 1
            else:
                return 0
        else:
            return 0
			
	def fcomparison3(self,h, rel):
		if 'or' in h["sentences"]:
			pos = h["sentences"].index('or')
			if h["sentences"][pos-1] in org_list:
				return 1
			else:
				return 0
		else:
			return 0
	'''		
    #relation: irrelevant
    def firrelevant1(self, h, rel):
        for i in h["sentences"]:
            if i in all:
                return 1
        return 0
    #------------------------------- Functions for Price tag ---------------------------------------------------------  
    #------------------------------- Functions for Size tag ---------------------------------------------------------  
    #------------------------------- Functions for Feature tag ---------------------------------------------------------  
if __name__ == "__main__":
    pass
