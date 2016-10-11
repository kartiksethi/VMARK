import nltk
import os
import timeit
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
import linecache
import numpy as np
import math
from math import *

file1=open("tf.txt","r+")
output=open("norm.txt","w")
sum=0.0
num=0.0
for line in file1:
	pos=(line.decode("ISO-8859-1")).split()
	for i in xrange(1,len(pos)): # break into a module (for returning the union of docs) later
		if i%2==1:
			term=pos[i]
			file2=open("terms.txt","r+")
			for each in file2:
				pos2=(each.decode("ISO-8859-1")).split()
				if pos2[0]==term:
					num=((float)(pos2[2])/(float)(pos2[3]))+1
					num=math.log(num,10)
					num=num*((float)(pos[i+1]))
					sum+=num*num
					
					break
			file2.close()
	x=pos[0] + ' ' + str(math.sqrt(sum)) + '\n'
	print x
	output.write(x)
	sum = 0.0
file1.close()
output.close()
