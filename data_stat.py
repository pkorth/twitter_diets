import re, sys
from collections import defaultdict

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

def print_stats(tweets):
    tweet_count = 0
    word_count = 0
    users = defaultdict(int)
    vocab = defaultdict(int)

    for tweet in tweets:
        tweet_count += 1
        users[tweet.user] += 1
        clean_text = re.sub("[\.,]", " ", tweet.text)
        for word in clean_text.split():
            vocab[word] += 1
            word_count += 1

    hashtags = 0
    atuser = 0
    for v in vocab:
        if v.find("#") != -1:
            hashtags += vocab[v]
        if v.find("@") != -1:
            atuser += vocab[v]

    print "Num tweets", tweet_count
    print "Num users", len(users)
    print "Max tweets/user", max(users.values())
    print "Average tweets/user", sum(users.values()) / float(len(users))
    print "Min tweets/user", min(users.values())
    print "Vocab size", len(vocab)
    print "Highest Vocab TF", max(vocab.values())
    print "Average Vocab TF", sum(vocab.values()) / float(len(vocab))
    print "Hashtags", hashtags
    print "@user", atuser

    return vocab

def print_vocab(vocab):
    for w in sorted(vocab, key=vocab.get, reverse=True):
        print w, vocab[w]

filename = "meat_dataset.txt"
tweets = read_tweets(filename)
vocab = print_stats(tweets)
#print_vocab(vocab)
