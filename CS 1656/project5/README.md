# Repository: project5.template
# Assignment #5: Decision Trees

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Spring 2019   
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> 
> Assignment: #5.  
> Released: April 8, 2019  
> **Due:      April 20, 2019**

### VERY IMPORTANT NOTICE ###
This assignment is **optional**. We will count the best 4 assignment grades out of all your submitted assignments (i.e., up to 5).

### Description
This is the **fifth assignment** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2019 semester.

### Goal
The goal of this assignment is to familiarize you with classification systems in general and with decision tree classifiers in particular.


### What to do -- dec_tree.py
You are asked to write a Python program, called `dec_tree.py` that will  
1. read a decision tree (stored in a plain text file),  
2. read a test data set (stored in a csv file, with the first row having the variable names),  and
3. evaluate the test data using the provided decision tree and provide statistics. 

Your program should be invoked as:
```
python3 dec_tree.py tree.txt test.csv
```

### (1) Decision Tree Format
The decision tree will be provided as a text file and will essentially be the output from the ID3 Decision Tree Classifier. 

A sample decision tree is provided below and also included as file `tree.txt` within this repository:
```
color black: bad (2) 
color blue
|   fruit blueberries: good (2) 
|   fruit grapes: bad (1) 
color green
|   fruit blueberries: bad (2) 
|   fruit grapes: good (2) 
color red
|   fruit blueberries: bad (1) 
|   fruit grapes: good (1) 
```

The above was generated by the `treegen.py` program which is also included within this repository. The format is fairly straightforward: the above tree corresponds to a two-level decision tree, with `color` being the first variable (valid options: `black`, `blue`, `green`, and `red`) and `fruit` the second variable (valid options: `blueberries` and `grapes`). There are only two labels: `good` and `bad`. The numbers in parentheses denote how many samples each rule was built upon. 

Your program **should handle decision trees up to 3 levels deep**.  

Please note that although you are encouraged to experiment with the `decision-tree-id3` module (https://svaante.github.io/decision-tree-id3/index.html), used by the `treegen.py` program, as part of preparing your assignment, you are **not allowed to use the decision-tree-id3 module in your submission**.


### (2) Test Data Format
The test data set will be provided as a CSV file. The first row will contain the variable names. A sample test data file, named `test.csv`, is provided within this repository. The first 3 lines of the file are shown below:
```
"day_of_week", "fruit", "color"
"mon", "blueberries", "black"
"mon", "blueberries", "blue"
```

Please note that the number of variables in the test data set is greater than or equal to the number of variables specified in the decision tree file. In this example, `day_of_week` was not part of the decision tree.

 
### (3) How to evaluate the decision tree
Given the decision tree and the test data input files, you are asked to do two things:
1. for each row in the test data set, find which rule from the decision tree it will match against, and   
2. keep track of how many times each rule in the decision tree was matched and print these statistics   

Your program should only print the statistics for all rules and it must follow the same format as in the decision tree format. 

For example, the correct output for running your program with the provided `tree.txt` and `test.csv` files should be the following (included in the repository as `output.txt`):
```
color black: bad (6) 
color blue
|   fruit blueberries: good (3) 
|   fruit grapes: bad (2) 
color green
|   fruit blueberries: bad (4) 
|   fruit grapes: good (5) 
color red
|   fruit blueberries: bad (2) 
|   fruit grapes: good (4) 
UNMATCHED: 1
```

Note that you must include a line at the end if the test data contain rows that were not matched by any decision tree rules.

**Important Hint** In order to solve this assignment, you are strongly encouraged to read the documentation for the `exec()` python command
https://docs.python.org/3/library/functions.html#exec


### Important: special-cases.txt 
If you do something in your code that you would consider a special case, then you are requested to submit an extra file, along with your submission, named `special-cases.txt`, where you described in plain text what the special case(s) is/are and how you handled it/them in your program. We will use this mechanism instead of asking such questions in piazza.


### Important notes about grading
It is absolutely imperative that your python program:  
* runs without any syntax or other errors (using Python 3)  
* strictly adheres to the format specifications for input and output, as explained above.     

Failure in any of the above will result in **severe** point loss. 


### Allowed Python Libraries (Updated)
You are allowed to use the following Python libraries (although a fraction of these will actually be needed):
```
argparse
collections
csv
json
glob
math 
numpy
os
pandas
re
requests
string
sys
time
```
If you would like to use any other libraries, you must ask permission by Sunday, April 14th, 2019, using [piazza](http://cs1656.org).


### About your github account
It is very important that:  
* Your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  
* You use the same github account for the duration of the course  
* You use the github account that you specified at the beginning of the course  

### How to submit your assignment
For this assignment, you must use the repository that was created for you after visiting the classroom link. You need to update the repository to include your own python files as described above, and other files that are needed for running your program. You need to make sure to commit your code to the repository provided. We will clone all repositories shortly after midnight the day of the deadline **Saturday, April 20th, 2019 (i.e., at 12:15am, Sunday, April 21st, 2019)**. There are no late submissions allowed for this assignment.
