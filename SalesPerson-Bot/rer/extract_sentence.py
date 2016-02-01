import json
f = open("all_data1.json","r")
root = json.loads(f.read())['root']
sents = []
out = open("sents.txt","w")
for data in root:
	for i in data['data']:
		#print i['rels']
		out.write( i["sentence"]+ ":" + str(i.get('rels',"None")) + "\n")
out.close()		
