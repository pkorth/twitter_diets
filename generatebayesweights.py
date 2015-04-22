import numpy as np
import os, os.path
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from math import copysign

def main():
  veg_dataset = "dataset/common_veg.txt"
  meat_dataset = "dataset/common_meat.txt"
  max_features = 1500

  veg_tweets = read_tweets(veg_dataset)
  meat_tweets = read_tweets(meat_dataset)

  tweets, labels = split_by_user(veg_tweets, meat_tweets)

  vectorizer = CountVectorizer(stop_words='english', max_features=max_features)
  X = vectorizer.fit_transform(tweets)
  y = np.array(labels)

  clf = MultinomialNB()
  clf.fit(X, y)
  weights = clf.feature_log_prob_
  vocab = vectorizer.get_feature_names()
  print_weights(weights, vocab)

def print_weights(weights, vocab):
  diff_map = {}
  for v_weight, m_weight, word in zip(weights[0], weights[1], vocab):
    diff_map[word.encode('utf-8')] = (v_weight - m_weight)

  for w in sorted(diff_map, key=diff_map.get, reverse=True):
    print w, diff_map[w]

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

if __name__ == "__main__":
  main()
