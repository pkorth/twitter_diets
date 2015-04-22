import tweepy
import sys

# global cals
reputation_threshold = .5
tweet_blacklist = [
    "i am a vegetarian",
    "i am a meat lover",
    "http"
]

def conduct_search(api, query, max_tweets = 10):
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            print e
            break
    return searched_tweets

def has_blacklist(text):
    for bl in tweet_blacklist:
        if text.find(bl) != -1:
            return True
    return False

def get_tweets(api, userid, page_limit=-1):
    tweets = []
    page = 1
    try:
        while True:
            timeline = api.user_timeline(id=userid, page=page);
            if timeline:
                for tweet in timeline:
                    text = tweet.text.encode('utf-8').lower()
                    if text.find("rt") == 0 or tweet.retweeted or has_blacklist(text):
                        continue
                    tweets.append(text)
            else:
                break;
            if page_limit != -1 and page_limit < page:
                break;
            page += 1
    except:
        pass; # ignore users who block us
    return tweets

def get_followers(api, page_name, page_limit=-1):
    followers = []
    cursor = -1
    page = 1
    while True:
        part_followers = api.followers(id=page_name, cursor=cursor)
        if part_followers:
            cursor = part_followers[1][1]
            for pf in part_followers[0]:
                rep = float(pf.followers_count) / (pf.followers_count + pf.friends_count)   
                if rep < reputation_threshold:
                    continue
                followers.append(pf.screen_name)
        else:
            break
        if page_limit != -1 and page_limit < page:
            break
        page += 1
    return followers

def scrape_users(api, filename, label, page_limit=-1):
    infile = open(filename)
    for user in infile.readlines():
        user = user[0:len(user)-1]
        tweets = get_tweets(api, user, page_limit)
        for tweet in tweets:
            print "<BEGIN LABEL=%s USER=%s>%s<END>" % (label, user, tweet)
    infile.close()   

def main():
    consumer_key = "" FILL IN HERE;
    consumer_secret = "" FILL IN HERE;
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    page_limit = 1
    scrape_users("vegs.txt", "veg", page_limit)
    scrape_users("meatlovers.txt", "meat", page_limit)
    sys.exit(0)


    veg_list = [];
    veg_pages = ["VegTimes"];

    for veg_page in veg_pages:
        for follower in get_followers(api, veg_page, 5):
            veg_list.append(follower)


    for veg in veg_list:
        print veg
        for tweet in get_tweets(api, veg, 5):
            print tweet
        print "";

if __name__ == '__main__':
    main()
