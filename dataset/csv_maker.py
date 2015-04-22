import re, sys


class Tweet:
    def __init__(self, regex_split):
        self.label = regex_split[0]
        self.user = regex_split[1]
        self.text = regex_split[2]

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
    
def print_csv(tweets):
	print "label, user, text" 

	for tweet in tweets:
		print tweet.label + "," + tweet.user + "," + tweet.text
	return 0
			
#-----------------------Main Section------------------------

filename = sys.argv[1] # ex: meat_dataset.txt
tweets = read_tweets(filename)
print_csv(tweets)
