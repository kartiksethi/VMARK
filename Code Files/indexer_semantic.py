import nltk
import os
import timeit
import math
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

def wordnetpos(tbtag):	#function which gets the corresponding wordnet pos tag for a treebank pos tag
    if tbtag.startswith('J'):
        return wn.ADJ
    elif tbtag.startswith('N'):
        return wn.NOUN
    elif tbtag.startswith('V'):
        return wn.VERB
    elif tbtag.startswith('R'):
        return wn.ADV
    else:
        return ''

def sqrtweighting(termfrequency):	#computes the sqrt weighting for a term frequency in a document
	sqrt = termfrequency - 0.5
	sqrt = math.sqrt(sqrt)
	sqrt = sqrt + 1
	return sqrt

def processDocument():	#Processes each individual review. It adds the terms in the review to the inverted index and also updates the other files
				global docID,doclinenum,frequency,docline,tffile,lineterm
				fileinput = open("invindex_semantic.txt","r+")
				filebackup = open("invindex_semantic.txt.bak","w")
				filelinenum = 1
				tffile.write(str(docID) + ' ')
				for invline in fileinput: #loop to update the postings list				
					if frequency.has_key(lineterm[filelinenum]): #if the posting in the given line is present in the frequency dictionary, it has to be updated    					
						updterm = lineterm[filelinenum]				
						sqrt = sqrtweighting(frequency[updterm])
						#update term frequency file
						tffile.write(updterm.encode("ISO-8859-1") + ' ' + str(sqrt) + ' ')
						#update inverted index
						posting = invline[:-1] + str(docID) + ' ' + str(frequency[updterm]) + ' ' + str(sqrt) + ' ' + '\n'
						filebackup.write(posting)
					else:	#if line number is not equal to line number of the term then keep the old postings list
						filebackup.write(invline)
					filelinenum = filelinenum + 1
				tffile.write('\n')
				frequency.clear()	#refresh frequency dictionary
				os.rename("invindex_semantic.txt.bak","invindex_semantic.txt")			
				docline.write(str(docID) + ' ' + str(doclinenum) + ' ' + '\n')
				docID = docID + 1
				doclinenum += 9				
				fileinput.close()
				filebackup.close()

def processToken(tkpos):	#process each token
		global prevtoken, stemmer,termsFi,termsni,frequency,terms,linenum
		tk = tkpos[0]
		pos = tkpos[1]
		if wordnetpos(pos) == '':
			return	
		if(tk == 'product/productId'): #new doc if the 'product/productId' token is encountered	
			processDocument()

		if(len(tk) > 1 and tk != 'product/productId' and tk != 'review/userId' and tk!= 'review/profileName' and tk != 'review/helpfulness' and tk != 'review/score' and tk != 'review/time' and tk != 'review/summary' and tk != 'review/text'):	
			t = tk			
			wnpos = wordnetpos(pos)
			synonyms = wn.synsets(tk,pos = wnpos)	#get all the synonyms of the word corresponding to the pos
			if len(synonyms)==0:
				if not termsFi.has_key(t):
					termsFi[t] = 0
				if not termsni.has_key(t):
					termsni[t] = 0			
				if frequency.has_key(t):#update the frequency of the term in the current document if already present
					frequency[t] = frequency[t] + 1 
					termsFi[t] = termsFi[t] + 1
				else:	#add the term to the frequency dictionary 
					termsni[t] = termsni[t] + 1
					termsFi[t] = termsFi[t] + 1
					frequency[t] = 1
				if not terms.has_key(t):	#if dictionary of terms doesn't have the term, then add the token to it
						terms[t] = linenum
						lineterm[linenum] = t
						#create a new line in the inverted index for the new term
						g = open('invindex_semantic.txt','a')
						g.write(t.encode("ISO-8859-1"))
						g.write(' ')
						g.write('\n')
						g.close() 
						linenum = linenum + 1
			else:
				for syn in synonyms:
					t = syn.name()
					if not termsFi.has_key(t):
						termsFi[t] = 0
					if not termsni.has_key(t):
						termsni[t] = 0			
					if frequency.has_key(t):#update the frequency of the term in the current document if already present
						frequency[t] = frequency[t] + 1 
						termsFi[t] = termsFi[t] + 1
					else:	#add the term to the frequency dictionary 
						termsni[t] = termsni[t] + 1
						termsFi[t] = termsFi[t] + 1
						frequency[t] = 1
					if not terms.has_key(t):	#if dictionary of terms doesn't have the term, then add the token to it
							terms[t] = linenum
							lineterm[linenum] = t
							#create a new line in the inverted index for the new term
							g = open('invindex_semantic.txt','a')
							g.write(t.encode("ISO-8859-1"))
							g.write(' ')
							g.write('\n')
							g.close() 
							linenum = linenum + 1
		prevtoken = tk

f = open('foods.txt','r')
tffile = open("tf_semantic.txt","w")
docline = open("docline_semantic.txt","w")
docID = 0
linenum = 1
terms = {} #stores the list of all terms' line numbers in the inverted index
termsFi = {} #stores the list of all terms' corpus frequencies
termsni = {} #stores the list of all terms' corpus document frequencies
frequency = {} #stores the frequencies of terms for each document
lineterm = {} #stores the term corresponding to a given line
prevtoken = '' #stores the previous token
doclinenum = -8
start = timeit.default_timer()
for line in f:	#getting line by line input
	if docID == 5001:
		break
	tokens = nltk.pos_tag(word_tokenize(line.decode("ISO-8859-1")))	
	for tk in tokens:
		processToken(tk)
		
processDocument() #flushing out the last document's data

#writing dictionary, inverted index line numbers, corpus frequency, document frequency
h = open('terms_semantic.txt','w')
for term in terms:
	op = term + ' ' + str(terms[term]) + ' ' + str(termsFi[term]) + ' ' + str(termsni[term]) + '\n'
	h.write(op.encode("ISO-8859-1"))
stop = timeit.default_timer()
print stop-start

f.close()
tffile.close()
docline.close()
h.close()
    
