q_dict = [["Show","me","all","the","Samsung","phones","costing","less","than","25000"],["Other","Other","Other","Other","Org","Other","Other","Other","Other","Price"],"price_query"]
	

				
import json
import ner_client
'''
class queryGen:
	def __init__(self,q_dict):
		self.q_dict = q_dict


st = raw_input("Enter a query")

q_dict = st.split(" ")
'''
def getEverythingTags(q_dict):
	everything = [i for i in q_dict[1]]
	return everything

def getQuery(q_dict):
	return q_dict[2]

def getSentence(q_dict):
	return q_dict[0]
def execute_interest_intent():
	query = getQuery(q_dict)#android will be mapped to Samsung
	everything = getEverythingTags(q_dict)
	sent = getSentence(q_dict)
	if query=="interest_intent":
				ind = everything.index("Org")
				
				
				
	
def execute_price_query():
	#price = "30000"
	#relate = "lesser"
	org_list =[]
	family = []
	model = []
	query = getQuery(q_dict)#android will be mapped to Samsung
	everything = getEverythingTags(q_dict)
	sent = getSentence(q_dict)
	#print sent
	if query == "price_query":
		nerC = ner_client.NerClient("55555","g100")
		for i in range(len(everything)):
			if everything[i] == "Org":
				org_list.append(sent[i])
			elif everything[i] == "Family":
				if sent[i] == "iPhone":
					org_list.append("Apple")
					family.append(sent[i])
				elif sent[i] == "Galaxy":
					org_list.append("Samsung")
					family.append(sent[i])
				else:
					family.append(sent[i])
					
				
			elif everything[i] == "Model":
				#print(sent)
				#print(i)
				family.append(sent[i])
				
				
		if len(family)!=0: 
			product = " ".join(family)
			#print product
			#print org_list[0]
			ret = nerC.get_products(org_list[0],product)
			response = []
			response1 = []
			for phones in ret:
				if phones["product"] == product:
					response.append(1)
					response1.append(phones)
					response2 = (response1,)
					
					
					response.append(response2)
					#print("HERE")
					return response
					break
			
		elif len(family)==0:
			response1 = []
			
			response = []
			if len(org_list)==0:
				return 0
			else:
				start = everything.index("Org")
				end = everything.index("Price")
				greater = ["higher","more","greater"]
				lesser = ["lesser","lower","less"]
				#print start
				#print end
				rec = nerC.get_products(org_list[0])
				#print rec
				rel_type = "equal"
				for i in range(start,end+1):
					if sent[i] in greater:
						rel_type = "high"
					elif sent[i] in lesser:
						rel_type = "low"
						
				money = sent[end]
				if "k" in money or "K" in money:
					money = money[0:len(money)-1]
					money = money + "000"
					money = int(money)
				else:
					money = int(money)

				if rel_type == "low":
					for phones in rec:
						if phones["dummy_price"]<=money:
							response1.append(phones)
							#print phones["product"],
							#print phones["dummy_price"]

				if rel_type == "high":
					for phones in rec:
						if phones["dummy_price"]>money:
							response1.append(phones)
							#print phones["product"],
							#print phones["dummy_price"]
				if rel_type == "equal":
					for phones in rec:
						if phones["dummy_price"]==money:
							response1.append(phones)
							#print phones["product"],
							#print phones["dummy_price"]
				
				response2 = (response1,)
				response.append(2)
				response.append(response2)
				#print "here"
				return response
				#for phones in rec:
					
			#print ret[0]
			#per = json.loads(ret)
			#print org_list
			#print per[org_list[0]]
	
		'''if query == "price_query"
		ret = nerC.get_products("Samsung")
		
		if relate == "lesser":
			for phones in ret:
				if phones["dummy_price"]<30000:
					print phones["product"],",",
					
		#ret = ner.get_products("Apple")
	#print ret'''

#execute_price_query()

