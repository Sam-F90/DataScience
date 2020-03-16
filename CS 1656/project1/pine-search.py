# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 15:03:25 2019

@author: Sam
"""

import json 
import re
import nltk
from nltk.stem import PorterStemmer 
import math

#read the inverted index from the json file 
with open('inverted-index.json') as json_file:
    invertedIndex = json.load(json_file)

#read the keywords
file = 'keywords.txt' 
f=open(file, 'r')           #open the file
keywords = f.read()             #read it into text
f.close()                   #close file reader


#copy the original keywords and keep track of the line for later use
words_and_line_numbers = {}
line_num = 1
for words in keywords.splitlines():
    words_and_line_numbers[line_num] = words
    line_num += 1 


#convert the text to lower case
keywords = keywords.lower()

#now we need to eliminate punctuation
keywords = re.sub(r'[^\d\w\s]','',keywords)

#now remove numbers
keywords = re.sub(r' \d+','',keywords)

#now preform stemming
ps = PorterStemmer()
tempText= "";
for line in keywords.splitlines():
    for word in line.split():
        tempText = tempText + ps.stem(word) +" "
    
    tempText = tempText + "\n"

keywords = tempText

weights = {}
#iterate over the keywords
for line in keywords.splitlines():
    #now go through each word in the line
    
    for keyword in line.split():
        if weights.get(keyword) == None:
            (word_count, doc_list, N) = invertedIndex[keyword]
            #calculate IDF
            n = len(doc_list)
            IDF = math.log((N/n),2)
            print 
            
            #now go through each document and calculate TF
            word_weights = []
            for doc_num in range(1,N +1):
               freq = doc_list.get(str(doc_num)) 
               TF = 0.0
               if freq != None:
                   TF = 1 + math.log(freq,2) 
               
               word_weights.append(TF * IDF)
            
            #now append this keywords weights to the weights variable
            weights[keyword] = word_weights
        

#now there is a dictionary of the keyword and the list of weights associated wih it


line_num = 0
total_docs = doc_num

#iterate over each line of keywords
for line in keywords.splitlines():
    line_num += 1
    print("------------------------------------------------------------")
    print("keywords =" ,words_and_line_numbers[line_num], " \n")
    
    keywordweights = []
    scores = [0] * total_docs
    
    #go through each keyword of the line to add their scores
    for keyword in line.split():
        word_weights = weights[keyword]
        doc_num = 0
        for elements in word_weights:
            scores[doc_num] = scores[doc_num] + word_weights[doc_num]
            doc_num += 1 
    
    #at an index to the scores so we know the doc number
    doc_num = 0
    for elements in scores:
            doc_num += 1
            keywordweights.append([scores[doc_num-1],doc_num])
            
    
    #sort the scores from highest to lowest
    keywordweights.sort(reverse = True)
    
    element_num = 0
    rank = 0
    previous_score = -1
    #iterate through the scores and display which files have the highest rank
    for elements in keywordweights:
        
        
        score,file = keywordweights[element_num]
        
        if(score == 0):
            break
        
        if(previous_score != score):
            rank += 1
            
        print("[",rank,"] file=doc" ,file ,".txt score=%.6f" % score, sep = "")
        previous_score = score
        
        element_num += 1
        #find the score of the individual words in the line
        for keyword in line.split():
            curr_weights = weights[keyword]
            print("    weight(",keyword,")=%.6f"  % curr_weights[file-1] , sep = "")
        
        
        print("\n")
    
    