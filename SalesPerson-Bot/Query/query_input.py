import ner_main
import part2
import qgen
import templateGenerate

def build(sent, st, tags):
	h = dict()
	h["reltags"] = []
	h["updates"] = []
	for i in range(len(st)):
		t = dict()
		t["word"] = st[i]
		t["tag"] = tags[i]
		h["updates"].append(t)
		if tags[i] not in h["reltags"]:
			h["reltags"].append(tags[i])		
	h["sentences"] = st
	return h

def getTags(st):
	ner_main.clf.load_classifier()
	
	st =[st,]

	result = ner_main.clf.tag(st)
	return result
	
def getRelation(hist):
	return part2.maxent.classify(hist)		

sent = raw_input("Enter\n")
sent = sent.strip(" ")
st = sent.split(" ")
wordTags = getTags(st)

#print(wordTags)

hist = build(sent,st,wordTags[0])
relation = getRelation(hist)
relation = "price_query"


#print wordTags
#print relation

qgen.q_dict = []
qgen.q_dict.append(st)
qgen.q_dict.append(wordTags[0])
qgen.q_dict.append(relation)

#print(qgen.q_dict)
response = qgen.execute_price_query() 

nlg = templateGenerate.TemplateGenerator(relation,response)

for i in nlg.decider()[relation]:
	print i
'''


rel = getRelation(hist)

print(wordTags)
print(rel)

#print "Model: ", ner_main.clf.model, " tagset = ", ner_main.clf.tag_set

'''
