import sys
import re


def file_to_string(filename):
	string = ""
	with open(filename, 'r') as input_file:
		string = input_file.read()
	return string

def file_to_stopword_list(filename):
	stopword_list = []
	string = file_to_string(filename)
	#print string
	string= re.sub(r'\s',' ',string)
	return string.split()
	
	
# c.Function that removes the stopwords
def removeStopwords(token_list):
	stopword_list = file_to_stopword_list("stopwords.txt")
	no_stopword_list = [x for x in token_list if x not in stopword_list]
	return no_stopword_list	
	
	
	
	
# -----------------------------Main Sectioin ------------------------

# python stopword_remover.py stopwords.txt meat_dataset_editing.txt


stopwords_file_name = sys.argv[1] # stopwords file	
target_file_name = sys.argv[2] # file that stopwords need to be removed

stopword_list = file_to_stopword_list(stopwords_file_name)
target_file_string = file_to_string(target_file_name)

line_list = target_file_string.split("\n")

total_list = []

for line in line_list:
	removed_list = removeStopwords(line.split())
	temp_string = ' '.join(removed_list)
	total_list.append(temp_string)


#print total_list
print '\n'.join(total_list)
