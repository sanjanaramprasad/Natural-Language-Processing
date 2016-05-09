import nltk,string,re,codecs,gensim
from nltk.corpus import reuters
from gensim import models,corpora,similarities
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import wordpunct_tokenize
import numpy as np
fileids=[]
stemmer=PorterStemmer()
stopwords=stopwords.words("english")+list(string.punctuation)
def tokenize(doc):
        write_data=[]
        tokens=wordpunct_tokenize(doc.strip())
        for token in tokens:
                if not token.lower() in stopwords:
                        write_data.append(unicode(stemmer.stem(token.lower())))
        p=re.compile('[a-zA-Z]+')
        write_data_filtered=list(filter(lambda data: p.match(data),write_data))
        #fileids.append(each_doc)
        return write_data_filtered

def corpus_building(write_data_filtered,dictionary):
        for each in write_data_filtered:
                yield dictionary.doc2bow(each)


def test(dictionary, model, index, test_document):
        write_data_c=[]
        write_contents=[]
        write_contents_tokens=[]
        token=tokenize(test_documents.strip())
        a=' '.join(token)+"\n"
        print "ACTUAL SENTENCE: " +a
        test_model=model[dictionary.doc2bow(token)]
        similarities=index[test_model]
        similarities=sorted(enumerate(similarities), key=lambda item : -item[1])
        #print "SIMILARITIES"
        #print similarities     
        for i in range(0,5):
                (file_no,score)=similarities[i]
                fileid=fileids[file_no]
                matched=reuters.open(fileid).read()
                #tokens_contents=wordpunct_tokenize(matched.strip())            
                match_tokens=tokenize(matched)
                match_lsi=model[dictionary.doc2bow(match_tokens)]
                difference= np.absolute(np.array([e[1] for e in test_model]) - np.array([e[1] for e in match_lsi]))
                #deltas=np.absolute(deltas)
                #print deltas
                #print list1
                topics=sorted(enumerate(difference), key= lambda e: -e[1])
                topic=model.show_topic(topics[0][0])
                words=[e[0] for e in topic]
                #print token
                print "The popular stems were"
                for word in words:
                        print word
                print "The closest document to the query is : %s \n"%fileid
                print matched,"\n"



documents=reuters.fileids()
write_data_filtered=[]
for each_doc in documents:
                        fileids.append(each_doc)
                        doc=reuters.open(each_doc).read()
                        write_data=tokenize(doc)
                        write_data_filtered.append(write_data)
dictionary = corpora.Dictionary()
for w in write_data_filtered:
        dictionary.doc2bow(w, allow_update=True)

corpus=list(corpus_building(write_data_filtered,dictionary))
#print "CORPUS"
#print dictionary
model=models.TfidfModel(corpus)
corpus_tfidf=model[corpus]
#print corpus_tfidf
lsi=models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
corpus_lsi=lsi[corpus_tfidf]
similarityModel=similarities.MatrixSimilarity(corpus_lsi)
test_documents=raw_input("Enter a search query")
test(dictionary,lsi,similarityModel,test_documents)

                
