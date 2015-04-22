# eecs498

## Vegetarian or Meat Lover?

##### You'll need to make a Twitter app to get a key/secret to access their data.
```
Create a Twitter account
Go to https://apps.twitter.com/
Create a new app
Click Keys and Accesss Tokens
Fill in the corresponding strings into demo.py and crawler/tweepytest.py
```

##### You'll need to install NLTK, the punkt tokenization package, and Tweepy:
```
sudo pip install nltk
sudo pip install tweepy
```
start an interactive python shell
```
import ntlk
nltk.download()
```
(click models, download punkt)

##### Scraping
Since twitter has a limit as to how far back you can search using their API, we had to hack together a way to generate a large list of users who said the phrase "I am a meat lover" and "I am a vegetarian".  To do this we searched twitter for the phrase and saved the resulting page to file.

Once we had the file we wrote a python script found in crawler/name_scrape.py that takes in a file as an argument and prints out a list of all of the twitter users it finds on that page.

The raw pages that we used is crawler/meat_raw.txt and crawler/veg_raw.txt.  The output of our scraper is crawler/meatlovers.txt and crawler/vegs.txt respectively.

##### Crawling
We have three utilities to gather tweets, both of which are located in crawler/tweepytest.py

* get_followers(api, page_name, page_limit) will give you an unique set of followers that follow the twitter page "page_name"
* get_tweets(api, userid, page_limit) will give you a set of tweets from the twitter user with id "userid"
* scrape_users(api, filename, label, page_limit) will print out a set of tweets from all of the users in "filename" with label "label"

We utilized the scrape_users function on the two list of users we scraped from twitter.  The crawler takes a LONG time because Twitter limits 100 requests per 15 minutes, so you'll need to let it run for 10+ hours on our userlist.  The output of the crawler can be found in crawler/meat_dataset.txt and crawler/veg_dataset.txt

##### Data Cleaning
The data from Twitter is really easy to overfit because of its low quality.  We wrote two utilities to clean up the data to be in a usable state.  dataset/stopword_remover.py is straightforward and utilizes dataset/stopwords as its vocabulary of stop words.  The output of this can be found in dataset/meat_dataset_no_stopwords.txt and dataset/veg_dataset_no_stopwords.txt

We also wrote a python script to remove words that weren't in common with vegetarians and meat-lovers (some people have the same typos, use odd slang, etc).  After running the script dataset/common.py we arrived at our final dataset of common_meat.txt and common_veg.txt

##### Classification
We have three scripts to showcase our data in different ways:
* generategraphs.py creates graphs of the performance of the classifiers over a range of maximum features
* generatebayesweights.py creates a list of the vocabulary of the Multinomial Naive Bayes classifier and the associated weights sorted by "meat-lover-ness"
* demo.py allows you to give a Twitter user to classify and output the corresponding confidence value
