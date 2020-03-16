#dec_tree.ppy
import sys
import csv
import re

# read in the arguments of the tree file and csv file
txt_file = sys.argv[1]
csv_file = sys.argv[2]

# data holds the data from the csv file
data = []

# tree is the decision tree
# each level of the decision tree will be a dictionary
tree = {}

# return depth, attribute_type, attribute, classification 
def parse_line(line):

	# increment depth until the first character that is not '|'
	# or a space
	depth = 0
	while line[depth] == '|' or hex(ord(line[depth])) == hex(0x20):
		depth += 1

	# bug: for some reason the while loop increments depth 1 more than necessary
	if depth > 3:
		depth-= 1

	if depth > 3:
		depth-= 1

	# split the line by space
	line = line.split(" ")

	# assign the attribute and its type
	attribute_type = line[depth]
	attribute = line[depth+1]

	# if the line ends in 'good' or 'bad', include it in the return as classification
	if (attribute[len(attribute)-1]) == ':':
		classification = line[depth+2]
		attribute = attribute[:-1]	#remove the ':' from the attribute string
	else:
		# if the line does not end with 'good' or 'bad' return None as the classification
		classification = None

	# print (line)
	# print ('depth:',depth, '	attribute_type:', attribute_type, '		attribute:', attribute, '		classification:',classification)

	return depth, attribute_type, attribute, classification

# function which adds a branch to the tree dictionary
def add_path(parent,attribute_type,classification):
	if parent.get(attribute_type):
		1
	else:
		if classification == None:
			parent[attribute] = {}
			return parent[attribute]
		else:
			parent[attribute] = classification +' (0)'
			return parent

# recursively traverses the tree until all the 'good' and 'bad' counts are returned
def get_results(tree):
	results = []
	for key in tree:
		if type(tree[key]) == dict:
			results.extend(get_results(tree[key]))
		else:
			results.append(tree[key])

	return results

# increments a string of the good or bad count
# ex. good(3) -> good(4)
def increment_count(string):
	str_arr = string.split(" ")

	count = int(str_arr[1][1:-1])
	new_count = count + 1

	new_count = '(' + str(new_count) + ')'

	string = str_arr[0] + ' ' + new_count
	return string

# recursively gets the classification of data
def get_classification(parent,attributes):
	for i in range(0,len(attributes)):
		a = attributes[i].replace('"', "")
		a = a.replace(" ","")

		result = parent.get(a)
		if type(result) == str:
			parent[a] = increment_count(result)
			return parent[a]
		elif type(result) == dict:
			return get_classification(result,attributes)


############
### MAIN ###
############


# read in the csv file 
with open('test.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		data.append(row)
		line_count+=1


#read in the tree txt file
with open(txt_file) as tree_file:
	row = tree_file.readlines()
	row = [x.rstrip() for x in row if x.rstrip()] # Remove newline characters



# CREATE THE TREE
prev_depth = 0
parent = tree
prev_attribute_type = None
prev_parent = None

for line in row:
	depth, attribute_type,attribute,classification =  (parse_line(line))
	
	# if the depth is 0, this path stems from root
	# if the depth is greater than the previous path, this path stems from the previous
	# if the depth is less than the previous path but not 0, it stems from the next level up
	if depth == 0:
		parent = tree
	elif depth > prev_depth:
		prev_parent = parent
		parent = prev_attribute_type
	elif 0 < depth < prev_depth:
		parent = prev_parent

	# add a path from the parent dictionary
	prev_attribute_type = add_path(parent,attribute_type,classification)
	prev_depth = depth


print(tree)

# classify each data type in the csv file
# keep track of how many are unmatched
attribute_names = []
line_count = 0
None_count = 0
for attributes in data:
	if (get_classification(tree, attributes)) == None and line_count > 0:
		None_count+=1
	line_count+=1

print(tree)

# get an array of the results (good count, bad count)
results = (get_results(tree))


print ('\n\n')
# print the results to console
with open(txt_file) as tree_file:
	replace_count = 0
	row = tree_file.readlines()
	for line in row:
		line = line.split(" ")
		char = line[len(line) - 2]

		# if the tree ends with 'good(x)' or 'bad(x)', replace it with the results
		if char[0] == '(':
			line[len(line) - 2] = results[replace_count][-3:]
			replace_count += 1

		# if statment so the lines that are "\n" are not printed
		if len(line) > 1: 
			print (" ".join(line), end ="")

# print the number of unmatched items
print('\nUNMATCHED:', None_count)