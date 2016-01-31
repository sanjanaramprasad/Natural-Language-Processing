import re
import sys
import os
import csv
import nltk
from nltk.corpus import stopwords
from collections import Counter;
import math
def normalize():
	stop=stopwords.words('english')
	#x=input("Enter name of file")
	input_filename="CRICKET CORPUS.txt"
	input_file=open(input_filename)
	list=[]
	l1=[]
	for row in input_file:
		row1=row.split('"')
		for each1 in row1:
			if(re.match(',',each1)):
				row1.remove(each1)
			
			if(re.match('\[',each1)):
				row1.remove(each1)
			if(re.match('\]',each1)):
				row1.remove(each1)
	row1=[each2 for each2 in row1 if each2]
	#print(row1)
	#stop words
	for a in row1:
		sentence=a.split()
		final=""
		for i in sentence:
			if i not in stop:
				final+="".join(i)+" "
			
		list.append(final)
	#print(list)
	f=open("finally.txt","w")
	count=0
	for each in list:
		count=count+1
		f=open("finally.txt","a")
		f.write("%s\n"%each)
	return count
	
def idf(query1):
	query=query1
	query=query.lower();
	input_filename="finally.txt"
	input_file=open(input_filename)
	document=[]
	for each in input_file:
		document.append(each)
	
	n=len(document)
	#print("N:",n)
	qlist=query.split();

	data={};

	#print(qlist)

	count=0;
	
	for j in qlist:
		count=0
		if re.match('boundary',j):
			#count=count+1
			for i in range(0,n):
				if j in document[i].lower() or 'four' in document[i].lower() or 'six' in document[i].lower() or 'SIX' in document[i].lower() or 'FOUR' in document[i].lower() or '4' in document[i].lower() or '6' in document[i].lower():
					count=count+1
					
				
		else:
			for i in range(0,n):
				#print("NJJJ",j)
				#print("gg",document[i])
				if j in document[i].lower():
					#print("J",j)
					#print("ss",document[i])
					count=count+1
		#print("count:",count)
		if (count==0):
				data[j]=-1
		else:
				data[j]=math.log10(n/count);
	return data
	#print(data)
def term_frequency(doc,que):
	query=que
	query=query.lower();
	document=doc
	document=document.lower();
	document=document.replace(",", " ")
	#print(document)

	def count_many(needles, haystack):
		haystack=haystack.strip()
		count = Counter(haystack.split(" "))
		#print("COUNT:",count)
		if re.match('boundary',needles):
			bound=0
			for each in count:
				if re.match('boundary',each):
					bound=bound+count['boundary']
				if re.match('four',each):
					bound=bound+count[each]
				if re.match('FOUR',each):
					bound=bound+count[each]
				if re.match('six',each):
					bound=bound+count[each]
				if re.match('SIX',each):
					bound=bound+count[each]
				if re.match('4',each):
					bound=bound+count[each]
				if re.match('6',each):
					bound=bound+count[each]
					#print("BOUND:",bound)
			count['boundary']=bound
				
			
		return {key: count[key] for key in count if key in needles}
		
	count=count_many(query,document);
	return count
	#print(count)
	
	
def list():
	stop=stopwords.words('english')
	input_filename="CRICKET CORPUS.txt"
	input_file=open(input_filename)
	list=[]
	l1=[]
	for row in input_file:
		row1=row.split('"')
		for each1 in row1:
			if(re.match(',',each1)):
				row1.remove(each1)
			
			if(re.match('\[',each1)):
				row1.remove(each1)
			if(re.match('\]',each1)):
				row1.remove(each1)
	row1=[each2 for each2 in row1 if each2]
	#print(row1)
	#stop words
	for a in row1:
		sentence=a.split()
		final=""
		for i in sentence:
				final+="".join(i)+" "
			
		list.append(final)
	return list

	

query=input("Please enter the query: ")
print("\n")
result={}
counter=normalize()
result=idf(query)
#print("RESULT_IDF:",result)

input_filename="finally.txt"
input_file=open(input_filename)
tf_idf={}
count=-1
list_of_dic=[]
list_of_doc=list()
for document in input_file:
	count=count+1
	tf_dic=term_frequency(document,query)
	#print("TF_DIC",tf_dic)
	for key in tf_dic:
		if re.match('[A-Za-z]+',key):
			try:
				a=result[key]
				b=tf_dic[key]
				#print("TF_IDF",a*b)
				tf_idf[count]=a*b
			except KeyError:
				pass
#print("FINAL DIC",tf_idf)
i=0
rank_list=[]
rank_list=sorted(tf_idf,key=tf_idf.__getitem__,reverse=True)
#print("RANK LIST:",rank_list)
'''for i in range(0,2):
	if(i):
		print(list_of_doc[rank_list[i]])'''
while i<10:
	try:
		print("RANK: ",i+1)
		#print("\n")
		print(list_of_doc[rank_list[i]])
		i=i+1
		print("\n")
	except IndexError:
		print("null")
		break
#print(list_of_doc)

		
			
			
	
