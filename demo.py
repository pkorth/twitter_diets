import math
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import sys
import tweepy
import string

import bayes.bayestest as bayestest
import crawler.tweepytest as tweepytest


def main():
  consumer_key = "" FILL IN HERE;
  consumer_secret = "" FILL IN HERE;
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  api = tweepy.API(auth, wait_on_rate_limit=True)
  
  if len(sys.argv) != 2:
    print 'usage: python demo.py handle'
    return

  handle = sys.argv[1]
  print 'Collecting tweets...',
  sys.stdout.flush()
  tweets = tweepytest.get_tweets(api, handle, 5)
  if len(tweets) == 0:
    print 'found none'
    return
  print 'found ' + str(len(tweets))
  sys.stdout.flush()
  tweet_concat = ''
  for t in tweets:
    tweet_concat += t + ' '
  tweet_concat = ''.join(filter(lambda x: x in string.printable, tweet_concat))
  tweet_concat = tweet_concat.encode('utf-8').lower()

  print 'Loading training corpus'
  sys.stdout.flush()
  veg_dataset = "dataset/veg_dataset_no_stopwords.txt"
  meat_dataset = "dataset/meat_dataset_no_stopwords.txt"
  veg_tweets = bayestest.read_tweets(veg_dataset)
  meat_tweets = bayestest.read_tweets(meat_dataset)
  train_tweets, train_labels = bayestest.split_by_user(veg_tweets, meat_tweets)

  vectorizer = CountVectorizer(stop_words='english', max_features=500)
  all_tweets = [tweet_concat] + train_tweets
  all_labels = [0] + train_labels

  x = vectorizer.fit_transform(all_tweets)
  y = np.array(all_labels)

  clf = MultinomialNB()
  clf.fit(x[1:], y[1:])

  prediction = clf.predict(x[0])
  confidence = clf.predict_proba(x[0])
  meat_prob = confidence[0][0]
  vege_prob = confidence[0][1]
  print 'Prediction:',
  print ('vegetarian' if prediction == 1 else 'meat-lover'),
  print 'with %.2f%% confidence' % max(meat_prob, vege_prob)

if __name__ == "__main__":
  main()
