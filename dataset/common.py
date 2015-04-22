import re, sys
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer

class Tweet:
    def __init__(self, regex_split):
        self.label = regex_split[0]
        self.user = regex_split[1]
        reg = r"[@#][a-zA-Z0-9_]+"
        self.text = re.sub(reg, " ", regex_split[2])

def read_tweets(filename):
    infile = open(filename)
    corpus = infile.read()
    infile.close

    pattern = r"<BEGIN LABEL=([a-z]+) USER=([a-zA-Z0-9]+)>(.*)<END>"

    result = re.findall(pattern, corpus)
    tweets = []
    for r in result:
        tweets.append(Tweet(r))
    return tweets
    
def tweet_by_user(tweets):
	user_dict = {}
	for tweet in tweets:
		if tweet.user not in user_dict:
			user_dict[tweet.user] = ""
			user_dict[tweet.user] += tweet.text
		else:
			user_dict[tweet.user] += tweet.text
		
	return user_dict


def split_by_tweet(veg_tweets, meat_tweets):
	tweets = []
	labels = []
	for tweet in veg_tweets:
		tweets.append(tweet.text)
		labels.append(1)

	for tweet in meat_tweets:
		tweets.append(tweet.text)
		labels.append(-1)

	return tweets, labels

def split_by_user(veg_tweets, meat_tweets):
	veg_map = {}
	meat_map = {}
	tweets = []
	labels = []
	for tweet in veg_tweets:
		if tweet.user in veg_map:
			veg_map[tweet.user] += " " + tweet.text
		else:
			veg_map[tweet.user] = tweet.text
	for tweet in meat_tweets:
		if tweet.user in meat_map:
			meat_map[tweet.user] += " " + tweet.text
		else:
			meat_map[tweet.user] = tweet.text
	for veg in veg_map:
		tweets.append(veg_map[veg])
		labels.append(1)
	for meat in meat_map:
		tweets.append(meat_map[meat])
		labels.append(-1)

	return tweets, labels

stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
	tokens = word_tokenize(text)
	return tokens

def leave_common_words(common_set, tweets):
	for tweet in tweets:
		text_token = tokenize(tweet.text)
		temp_string = ""
		temp_count = 0
		for token in text_token:
			if(token in common_set):
				temp_count += 1
				temp_string += token
				temp_string += " "
		tweet.text = temp_string
	return tweets
	
def print_tweets(tweets):
	for tweet in tweets:
		if (tweet.text == "" or tweet.text == " "):
			continue
		print "<BEGIN LABEL=" + tweet.label + " USER=" + tweet.user + ">",
		print tweet.text + "<END>"
		
#------------------------- Main Section---------------------------------

# python bayes.py dataset_no_stopwords.txt


veg_dataset = "veg_dataset_no_stopwords.txt"
meat_dataset = "meat_dataset_no_stopwords.txt"

veg_tweets = read_tweets(veg_dataset)
meat_tweets = read_tweets(meat_dataset)


"""
veg_string = ""
meat_string = ""
for tweet in veg_tweets:
	veg_string += tweet.text	

for tweet in meat_tweets:
	meat_string += tweet.text
"""
veg_token = []
meat_token = []

for tweet in veg_tweets:
	veg_token += tokenize(tweet.text)
	
for tweet in meat_tweets:
	meat_token += tokenize(tweet.text)	


#veg_token = tokenize(veg_string)
#meat_token = tokenize(meat_string)

veg_token_set = set(veg_token)
meat_token_set = set(meat_token)

#print len(veg_token_set) #19875
#print len(meat_token_set) #16130


common_list = list( set(veg_token) & set(meat_token) )

#print len(common_list) #5054

common_set = set(common_list)

common_veg_tweets = leave_common_words(common_set, veg_tweets)
common_meat_tweets = leave_common_words(common_set, meat_tweets)

print_tweets(common_veg_tweets)
#print_tweets(common_meat_tweets)
