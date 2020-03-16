#allowed libraries
import argparse
import collections
import csv
import glob
from itertools import combinations
from itertools import permutations
import math 
import os
import re
import string
import sys

#read command line arguments
input_file = sys.argv[1]
output_file_name = sys.argv[2]
min_supp_percent = sys.argv[3]
min_confidence = sys.argv[4]

#read the input file
with open(input_file) as inp:
	data = inp.readlines()

#convert to one string
data = ''.join(i for i in data if not i.isdigit())

#remove punction(mainly commas)
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
raw_data = ""
for char in data:
    if char not in punctuations:
        raw_data = raw_data + char

#remove the digits from the data
raw_data = ''.join([i for i in raw_data if not i.isdigit()])

#put the data in an array for easier use later
data_array = []
for line in raw_data.splitlines():
	data_array.append(line)


#create an array for each specific item
#this will be useful for permutations later
items = []
for item_set in data_array:
	for item in item_set:
		if item not in items:
			items.append(item)


#now create a list of all the permutations of the itemset
item_permutations = []
for i in range(len(items)):
	if i is not 0:
		for p in combinations(items,i):
			p = ''.join(sorted(p))
			p = tuple(p)
			item_permutations.insert(len(item_permutations),p)

#now calculate the support count for each permutation
#store it in dictionary CFI
CFI = {}
for subset in item_permutations:
	freq = 0;
	for line in data_array:
		char_count = 0
		for c in subset:
			if c in line:
				char_count+=1
		if char_count == len(subset):
			freq+= 1
	CFI[subset] = freq	

#create the VFI with only the itemsets which exceed the support % threshold
VFI = {}
for i in CFI:
	#calculate support_percentage
	supp_percent = CFI[i]/len(data_array)
	
	#convert to float
	supp_percentage = float(supp_percent)

	#if the threshhold is met, add to VFI
	if supp_percent >= float(min_supp_percent):
		VFI[i] = supp_percent


#create a list of the associative relations
AR = []
#create a list of relations already checked as to not repeat
repeat_check = []
for i in VFI:
	#find the frequent sets that are more than 1 item
	if len(i) > 1:
		#join the tuple into a string and append '>'
		new_i = "".join(i) + ">"
		#go through all the permutations of the subset
		for p in permutations(new_i):
			#do not include permutations that begin or end in '>'
			if p[0] != '>' and p[len(p)-1] != '>':
				#variables used later to split the permutations between the 
				#subset before the '>', and the subset after the '>'
				before_arrow = ''
				after_arrow = ''
				arrow_hit = False
				#go through chars in the permutatioj
				for char in p:
					if char == '>':
						arrow_hit = True
					else:
						if not arrow_hit:
							#add this char to the subset before the '>'
							before_arrow += char
						elif arrow_hit:
							#add this char to the subset after the '>'
							after_arrow += char

				add_item = True
				#now check if the permutation has been checked already
				for items in repeat_check:
					#if the left subset already exits...
					if items[0] == ''.join(sorted(before_arrow)):
						#and the right subset already exists with this left item...
						if items[1] == ''.join(sorted(after_arrow)):
							add_item = False
							#dont add this pair to repeat_check

				#if the item did not exist...
				if add_item:
					#add this permutation to the list of already checked ones
					repeat_check.append([''.join(sorted(before_arrow)),''.join(sorted(after_arrow))])

					#calculate the confidence
					#sup (i U j) / sup(i)
					I = ''.join(sorted(before_arrow))
					j = ''.join(sorted(after_arrow))
					IUj = ''.join(sorted(I + j))

					confidence = CFI[tuple(IUj)]/CFI[tuple(I)]

					#if the confidence is greater than the threshold, at it to the list of
					#associative relations to be written to the output
					if confidence > float(min_confidence):
						AR.append([VFI[(i)],confidence,tuple(before_arrow),tuple(after_arrow)])




#write the reults to the output file

#open the file and store in variable output_file
output_file = open(output_file_name, mode = 'w', newline = '')
#create a file_writer 
file_writer = csv.writer(output_file,delimiter=" ")

#write all the verified itemsets
for i in VFI:
	file_writer.writerow(["S,{0:.4f},".format(VFI[i]) +','.join(i)])

#write all the associative rule sets
for ar in AR:
	file_writer.writerow(["R,%.4f,%.4f,%s,%s,%s" %(float(ar[0]),float(ar[1]),','.join(ar[2]),'=>',','.join(ar[3]))])