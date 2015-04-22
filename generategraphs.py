import numpy as np
import os, os.path
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.cross_validation import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer
from math import copysign
import matplotlib.pyplot as plt
from scipy import interpolate
import sys

stemmer = PorterStemmer()
veg_dataset = "dataset/common_veg.txt"
meat_dataset = "dataset/common_meat.txt"

def main():
	veg_tweets = read_tweets(veg_dataset)
	meat_tweets = read_tweets(meat_dataset)

	tweets, labels = split_by_user(veg_tweets, meat_tweets)

	mf = [1, 10, 20, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 
			1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
	
	scores = []

	clfs = [
		RandomForestClassifier(n_estimators=21),
		MultinomialNB(),
		BernoulliNB(),
		SVC(kernel='linear')
		]

	clf_names = [
		"Random Forest",
		"MultinomialNB",
		"BernoulliNB",
		"Linear SVM"
		]

	colors = [
		'r', 
		'b', 
		'g', 
		'c'
		

	for clf in clfs:
		score = []
		for max_features in mf:
			score.append(get_training_accuracy(clf, max_features, tweets, labels))
		scores.append(score)

	ax = plt.figure().add_subplot(111)
	for i in range(len(colors)):
		tck = interpolate.splrep(mf, scores[i], k=3)
		xnew = np.linspace(min(mf), max(mf), 300)
		ynew = interpolate.splev(xnew, tck)
		ax.plot(xnew, ynew, colors[i], label=clf_names[i])

	# 435 veg + 324 meat = 759 total
	# 57% accuracy if always veg
	ax.plot(mf, [.5731] * len(mf), linestyle='--', color='k', label="All Vegetarian")
	ax.set_xlabel('Number of Features')
	ax.set_ylabel('Accuracy')
	ax.legend(loc=3)
	plt.show()

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

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
	tokens = word_tokenize(text)
	stems = stem_tokens(tokens, stemmer)
	return stems

def get_training_accuracy(clf, max_features, tweets, labels):
	vectorizer = CountVectorizer(stop_words='english', max_features=max_features, tokenizer=tokenize)
	X = vectorizer.fit_transform(tweets)
	y = np.array(labels)

	skf = StratifiedKFold(y, 10)
	acc_vals = []
	for train_index, test_index in skf:
		x_test = X[test_index]
		y_test = y[test_index]
		x_train = X[train_index]
		y_train = y[train_index]

		clf.fit(x_train.toarray(), y_train)
		y_pred = clf.predict(x_test.toarray())
		acc = metrics.accuracy_score(y_pred, y_test)
		acc_vals.append(acc)

	s =  sum(acc_vals) / len(acc_vals)
	print max_features, s
	return s

if __name__ == "__main__":
	main()