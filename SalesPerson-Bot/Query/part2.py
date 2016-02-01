from feature_functions1 import *
from mymaxent1 import *
from build_history1 import *
import json
from rules import *
from ner_metrics_1 import *
file = open("rer.txt","w")
p_file ="rer.p"
r = Rules()
def test(clf, history_list):
	result = []
	prev = []
	vit = []
	tagged = []
	for history in history_list:
		mymap = clf.func.wmap[history[0]["wn"]]
		words = mymap['words']
		tags = mymap['pos_tags']    
		index = history[0]["i"]
		val = clf.classify(history[0])
		#li = clf.viterb(words,history[0])
		#li = li[0]
		#vit.append(li)
		if str(val) == "irrelevant":
			val = r.eval(history)
			if val=="":
				val = "irrelevant"
		tagged.append(val)
		file.write("words : " + str(history[0]['sentences']) + " , tags: " + val+"\n")
		#prev = words
	met = NerMetrics(tagged,expected)
	#print "Accuracy:" + str(metrics(tagged,expected)*100)
	#print met.compute()['overall']
	return result
f = open("all_data1.json","r")
root = json.loads(f.read())['root']
h_tup,sent,expected = build_history(root,['irrelevant', 'price_query', 'feature_query', 'interest_intent', 'comparison'])#, 'disagreement', 'greeting','agreement', 'acknowledgement'])
def metrics(tagged,expected):
	tot = 0
	cor = 0
	for i in range(len(tagged)):
		tot+=1
		if(tagged[i]==expected[i]):
			cor+=1
	acc = float(cor)/tot
	return acc
def parse(x):
	try:
		return x[0].keys(0)
	except:
		return "irrelevant"
expected = map(parse,expected)
maxent = MyMaxEnt1(h_tup,FeatureFunctions1(sent),pic_file=p_file)
maxent.train()
#print(maxent.model)

#r = test(maxent,h_tup)


file.close()
