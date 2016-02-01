from nltk import *
def postagger(sent):
	text = word_tokenize(sent)
	posTagged = pos_tag(text)
	simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
	return simplifiedTags
class Rules:    
    def rule_Acknowledgement(self,h):
        words = map(lambda x : x.lower(),h[0]["sentences"])
        if (("thanks" in words) or ("thank" in words) or ('yes' in words)) or ( 'i' in words and 'do' in words) and '?' not in words:
            return 1
        else:
            return 0
    
    def rule_Disagreement(self,h):
        words = h[0]["sentences"]
        if (("not" in words) or ("no" in words) or ('else' in words) or ('alternative' in words)):
            return 1
        else:
            return 0
    
    def rule_Greeting(self,h):
        words = h[0]["sentences"]
        if (("hi" in words) or ('hello' in words) or ('hey' in words)):
            return 1
        else:
            return 0

    def rule_Agreement(self,h):
        words = h[0]["sentences"]
        if (("true" in words) or ("yes" in words) or ('indeed' in words)):
            return 1
        else:
            return 0

    def eval(self,h):
        if(self.rule_Acknowledgement(h)==1):
            return "acknowledgement"
        elif self.rule_Greeting(h)==1:
            return "greeting"
        elif self.rule_Disagreement(h)==1:
            return "disagreement"
        elif self.rule_Agreement(h) == 1:
            return "agreement"
        else:
            return ""
