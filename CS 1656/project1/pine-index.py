# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:13:37 2019

@author: Sam
"""

import glob
import sys
import os
import string
import re
import nltk
from nltk.stem import PorterStemmer 
import json

documents = []
inverseIndex = {}

path = 'input/*.txt'            #Set the path for the keywords file
files = glob.glob(path)         
for file in files:              #iterate through files
    f=open(file, 'r')           #open the file
    text = f.read()             #read it into text
    f.close()                   #close file reader
    text = text.lower()         #convert the text to lower case
    


    #now we need to eliminate punctuation
    text = re.sub(r'[^\d\w\s]','',text)
    
    #now remove numbers
    text = re.sub(r' \d+','',text)
    
    #now preform stemming
    ps = PorterStemmer()
    
    #
    tempText= "";
    for word in text.split():
        tempText = tempText + ps.stem(word) + " "
    
    text = tempText
    
    documents.append(text)

###
#The text is now processed and can be put into the inverse index
###
doc_num = 0         
for document in documents:
    doc_num += 1 
    for word in document.split():
        
        #check if the word is already in dictionary
        if inverseIndex.get(word) == None:
            #add to inverseIndex
            inverseIndex[word] = (0, {}, 0)
        
        #increment the word count
        (count,doc_list, doc_total) = inverseIndex[word]
        count += 1
        
        #update the documents it appears and how man times
        if doc_list.get(doc_num) == None:
            #add the document to the list
            doc_list[doc_num] = 0
        
        #now increment the count in that document
        doc_count = doc_list[doc_num]
        doc_count += 1
        doc_list[doc_num] = doc_count
        
        #update the inverse index
        inverseIndex[word] = (count,doc_list,0)
        
#now add the number of documents to each dictionary entry
for key in inverseIndex:
    (count,doc_list, doc_total) = inverseIndex[key]
    doc_total = doc_num 
    inverseIndex[key] = (count,doc_list, doc_total)

#now store the invertedIndex as a JSON object in a file named inverted-index.json
with open('inverted-index.json', 'w') as outfile:
    json.dump(inverseIndex, outfile)
    
