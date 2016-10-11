"""" Library Imports"""
import nltk
import os
import timeit
from nltk.corpus import wordnet as wn
from collections import Counter
import linecache
import numpy as np
import math
from math import *
from operator import itemgetter


""" Global Variables """
docs=[]									# temporary list used in the getDocs() function
doc_frequencies=[] 						# temporary list used in the getDocs() function
union_docs = set()						# set containing the union of all relevant docs pertaining to the query
qVector = []							# query vector of the entered query
query_terms = []						# contains the stemmed words of the query
query_dict = Counter()					# dictionary containing the frequency of query terms
univ_dict={}							# dictionary with key/value pairs as terms and their posting lists 
docVectorList = []						# list of doc vectors containg their similarity w.r.t to the query vector
dict_Fi_ni = {}							# dictionary containing the Fi and ni values of terms

def wordnetpos(tbtag):	
    """
    Function which gets the corresponding Wordnet POS tag for a treebank POS tag

    Input:
    -tbtag: the treebank POS tag which needs to be converted to a Wordnet POS tag

    Return:
     Returns one of the following wordnet POS tags based on the treebank POS tag supplied
    -wn.ADJ: for adjective
    -wn.NOUN: for noun
    -wn.VERB: for verb
    -wn.ADV: for adverb
    """
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

def ENPY():  
	""" 
	Used to calculate the global weights for the query vector using the ENPY formula (see documentation).

	Returns:
	- ENPY_list: Returns the list of global weights w.r.t query terms.
	"""
	global univ_dict
	ENPY_list = []
	for term in univ_dict:
		Fi_term = 0						# refers to the collection frequency of the query term in the corpus
		for List in univ_dict[term]:
			Fi_term += int(List[1])		
		log_N = math.log(100000, 10)
		wtt = 0
		for List in univ_dict[term]:
			wtt = wtt + ((float(List[1]) / Fi_term) * math.log((float(List[1]) / Fi_term), 10) / log_N)
		ENPY_list.append(wtt+1)
	return ENPY_list

		


def LOGG(): 
	"""
	Used to calculate the local weights for the query vector using the LOGG formula (see documentation).

	Returns:
	- LOGG_list: Returns the list of local weights w.r.t query terms.
	"""
	global univ_dict
	LOGG_list=[]
	for term in univ_dict:
		wt = 0.2 + 0.8 * math.log((query_dict[term] + 1), 10)
		LOGG_list.append(wt)
	return LOGG_list
		
def IGFL(term):  
	"""
	Used to calculate the global weights for the document vector using the IGFL formula (see documentation).

	Input:
	-term: term for which we want to retrieve the IGFL value.

	Returns:
	-wt: IGFL value w.r.t to the input term.
	"""
	li = dict_Fi_ni[term]
	Fi = float(li[0])				# refers to the collection frequency of the term
	ni = float(li[1])				# refers to the document frequecy of the term
	wt = math.log((Fi/ni) + 1, 10)
	return wt 

def getNorm(doc):
	"""Get the normalised values""""""
	Used to calulate the normalization value for document.

	Input:
	-doc: document for which we want to retrieve the normalization value (root of (sum of squares))

	Returns:
	-norm: normalization value for the document.
	"""
	s=linecache.getline("norm_semantic.txt",int(doc)+1)
	s=(s.decode("ISO-8859-1")).split()
	norm = float(s[1])
	return norm 

def SQRT(doc):
	"""
	Used to calculate the local weights for document vectors using the SQRT formula (see documentation).
	Also calculate the similarity value of the document vector w.r.t the entered query.

	Input:
	-doc: document for which we want to calculate the SQRT value and corresponding similarity with entered query.

	Returns:
	-sim: similarity value of the document w.r.t entered query
	"""
	global univ_dict
	i = 0
	ls = []
	wt = 0
	norm = getNorm(doc)				# retrieves the normalization for the input doc
	for term in univ_dict:
		for List in univ_dict[term]:
			if List[0] == doc:
				wt += float(List[2]) * IGFL(term) * qVector[i]
				i +=1
				break
	return  wt / norm

def queryVector():
	"""
	Used to calculate the query vector of the entered query.
	"""
	global univ_dict, qVector
	local_wt = LOGG() # should return vector
	global_wt = ENPY() # should return vector
	qVector = np.array(local_wt) * np.array(global_wt)	# qVector stores the final query vector

def documentsVector():
	"""
	Used to compute the document vector and calculate its similarity w.r.t query.
	"""
	global univ_dict, docVectorList, union_docs
	union_docs_list = list(union_docs)
	for doc in union_docs_list:							# iterates over the set of relevant documents
		sim_wt = SQRT(doc)								# returns the similarity between the query vector and the doc
		docVectorList.append([doc,sim_wt])


def getDocs(term, linenum):
	"""
	Finds the postings list of the term. Also finds the union of relevant documents w.r.t query.

	Input:
	-term: the term for which we are finding the postings list.
	-linenum: linenumber from which the posting list is to be retrieved. 
	"""
	global univ_dict
	docs = []											# list of docs for a term to calculate union
	doc_freq=[] 										# temp list for docs and freqs in which term occurs
	s=linecache.getline("invindex_semantic.txt",(int)(linenum) )
	s=(s.decode("ISO-8859-1")).split()
	for i in xrange(1, len(s)):
		doc_freq.append(s[i])
		if i%3 == 0:
			if term not in univ_dict:
				univ_dict[term] = [doc_freq]
				doc_freq=[]
			else:
				univ_dict[term].append(doc_freq)
				doc_freq=[]
	for i in univ_dict[term]:
		docs.append(i[0])
	global union_docs
	union_docs = union_docs | (set(docs))  				# use this to calculate doc vectors
    
	
def retrieveRelevant(line_list): 
    """
	Prints the relevant documents.

	Input:
	-line_list: represents a list of starting line numbers for the top 'n' relevant documents.
	""" 
    for line_number in line_list:
    	for i in xrange(line_number, line_number + 8):
    		s = linecache.getline("foods.txt", i)
    		s = s[:-1]
    		print s
    	print '\n'
		


""" Main block of execution """
start = timeit.default_timer()
indexfile=open("invindex_semantic.txt",'rU');

print "		#############################################################"
print "		#  VMARK v1.0.1 Semantic VSM Information Retrieval System  #"
print "		#############################################################"
print "\n\n"
print "Please enter a query:"
query=raw_input()
print "\nPlease enter the number of results you want to retrieve:"
num_rel_docs=int(raw_input())

query_tokens=(query.decode("ISO-8859-1")).split()			# tokenizing the entered query
query_tokens=nltk.pos_tag(query_tokens)
for qt in query_tokens:    									
	synonyms = wn.synsets(qt[0],pos = wordnetpos(qt[1]))
	if len(synonyms) == 0:
		query_terms.append(qt[0])							# making a list of query terms and their synonyms
		query_dict[qt[0]] += 1
	for syn in synonyms:
		syn = syn.name()
		query_terms.append(syn)
		query_dict[syn] += 1
query_terms = set(query_terms) 								# used a set to have membership checking as O(1)

termsfile=open("terms_semantic.txt",'rU');
count = 0
count_limit = len(query_terms)

for line in termsfile:    # checking in the terms.txt whether the word of the current line matches any term of the query terms list
	pos=(line.decode("ISO-8859-1")).split()
	if (pos[0] in query_terms) and count < count_limit:
		term = pos[0]
		linenum=int(pos[1])
		count += 1
		dict_Fi_ni[pos[0]] = [pos[2],pos[3]]
		getDocs(term, linenum)
	elif count > count_limit:
		break

queryVector()
documentsVector()
docVectorList =sorted(docVectorList, key=itemgetter(1), reverse = True)
doc_lines=[]												# list to store the starting line number of the relevant documents
for i in docVectorList:
	docLine = open("docline_semantic.txt",'rU');
	for line in docLine:
		pos=(line.decode("ISO-8859-1")).split()
		if pos[0] == i[0]:
			doc_lines.append(int(pos[1]))
			break
if len(docVectorList) == 0:
	print "\nSorry, no relevant documents found :( "
else:
	print "\nRelevant docs related to your query are:" 
	if len(docVectorList) < num_rel_docs:
		retrieveRelevant(doc_lines)
		
	else:
		retrieveRelevant(doc_lines[:num_rel_docs])
		


stop = timeit.default_timer()
print "Time taken:"
print stop-start
termsfile.close()
indexfile.close()	
