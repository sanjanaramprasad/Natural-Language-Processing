from jinja2 import Template


class TemplateGenerator(object):

		def __init__(self,relation,response):
			self.relation=relation
			self.data=response[1][0]
			self.error_code=response[0]
			self.templates=[]

		"""" Templates for different price_query"""
		def price_query_template(self):
			d={'price_query':[]}
			org=""
			family=""
			price=""
			count=len(self.data)
			print self.data
			for i in self.data:
				org=i['brand']
				family=i['product']
				price=i['dummy_price']
			if self.relation=="price_query":
				if self.error_code==1:
					template1=Template('{{Org}} {{Family}} costs Rs {{ price}}.')
					output1=template1.render(Org=org,Family=family,price=price)
					d['price_query'].append(output1)
				
				if self.error_code==2:
					template2=Template('There are {{count}} phones which costs less than Rs {{price}}')
					output2=template2.render(count=count,price=price)
					d['price_query'].append(output2)

				if self.error_code==3:
					template3=Template('There are {{count}} phones which costs greater than Rs {{price}}')
					output3=template3.render(count=count,price=price)
					d['price_query'].append(output3)
				
				if self.error_code==4:
					template4=Template('There are {{count}} phones available around Rs {{price}}')
					output4=template4.render(count=count,price=price)
					d['price_query'].append(output4)
		
				
				if count==0 and self.error_code==5:
					template5=Template('{{Org}} {{Family}} not Available')
					output5=template5.render(Org=org,Family=family)
					d['price_query'].append(output5)

			return d

		"""Templates for greetings"""
		def greeting_template(self):
			
			d={'greeting':[]}
			if self.error_code==1:
				template1=Template('{{response}},How may i assist you?')
				output1=template1.render(response="Good Morning")
				d['greeting'].append(output1)
				
			if self.error_code==2:
				template2=Template('{{response}},How may i assist you?')
				output2=template2.render(response="Good Afternoon")
				d['greeting'].append(output2)

			if self.error_code==3:
				template3=Template('{{response}},How may i assist you?')
				output3=template3.render(response="Good evening")
				d['greeting'].append(output3)
				
			if self.error_code==4:
				template4=Template('How are you?')
				output4=template4.render()
				d['greeting'].append(output4)
				
			if self.error_code==5:
				template5=Template('Hi,I am glad to have you here')
				output5=template5.render()
				d['greeting'].append(output5)
			
			return d

		"""Templates for ackowledgement"""
		def ackowledgement_template(self):
			
			d={'ackowledgement':[]}
			if self.error_code==1:
				template1=Template('Thank you so much')
				output1=template1.render()
				d['ackowledgement'].append(output1)

			if self.error_code==2:
				template2=Template('Yes')
				output2=template2.render()
				d['ackowledgement'].append(output2)

			if self.error_code==3:
				template3=Template('Alright')
				output3=template1.render()
				d['ackowledgement'].append(output3)

			if self.error_code==4:
				template4=Template('Fine')
				output4=template4.render()
				d['ackowledgement'].append(output4)

			if self.error_code==5:
				template5=Template('Okay')
				output5=template5.render()
				d['ackowledgement'].append(output5)
		
			return d

		"""Templates for agreement"""
		def agreement_template(self):
			
			d={'agreement':[]}
			if self.error_code==1:
				template1=Template('Yes,I am Sure')
				output1=template1.render()
				d['agreement'].append(output1)

			if self.error_code==2:
				template2=Template('You are absolutely right')
				output2=template2.render()
				d['agreement'].append(output2)

			if self.error_code==3:
				template3=Template('Yes,Definitely')
				output3=template3.render()
				d['agreement'].append(output3)


		
			return d

		"""Templates for disagreement"""
		def disagreement_template(self):
			
			d={'disagreement':[]}
			if self.error_code==1:
				template1=Template('I am not sure')
				output1=template1.render()
				d['disagreement'].append(output1)

			if self.error_code==2:
				template2=Template('No thats incorrect')
				output2=template2.render()
				d['disagreement'].append(output2)

			if self.error_code==3:
				template3=Template('Sorry')
				output3=template3.render()
				d['agreement'].append(output3)

			if self.error_code==4:
				template4=Template('No')
				output4=template4.render()
				d['agreement'].append(output4)

			return d



		def decider(self):
			if self.relation=="price_query":
				return self.price_query_template()
			if self.relation=="greeting":
				return self.greeting_template()
			if self.relation=="acknowledgement":
				return self.ackowledgement_template()
			if self.relation=="agreement":
				return self.agreement_template()
			if self.relation=="disagreement":
				return self.disagreement_template()

if __name__ == "__main__":

	print "Price query"
	response=[4,([{'dummy_price':14117,'brand':'Samsung','product':'U800 Soul b'},
	   {'dummy_price':30784,'brand':'Samsung','product':'T929 Memoir'},
	   {'dummy_price':14704,'brand':'Samsung','product':'U7220 Ultra b'}],)]
	#response=[5,([],)]
	
	nlg=TemplateGenerator('price_query',response)
	print nlg.decider()
	'''
	print "greeting"
	response=[3,([],)]
	nlg=TemplateGenerator('greeting',response)
	print nlg.decider()

	print "ackowledgement"
	response=[2,([],)]
	nlg=TemplateGenerator('ackowledgement',response)
	print nlg.decider()
	'''
