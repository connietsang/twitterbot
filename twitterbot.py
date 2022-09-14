#!/usr/local/bin/python3.9
import tweepy
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import random
import time

load_dotenv(sys.path[0] + '/keys.env')

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_KEY_SECRET = os.getenv("CONSUMER_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


client = tweepy.Client(
    consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_KEY_SECRET,
    access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
)

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="http://127.0.0.1/",
    scope=["tweet.read", "tweet.write", "like.read", "like.write"],
    # Client Secret is only necessary if using a confidential client
    client_secret=CLIENT_SECRET
)

query = '(beiguang OR beigguang OR 凝北 OR 北凝 OR ningguang/beidou OR beidou/ningguang) -zhongguang -beikazu -is:retweet -is:reply'

# minimum number of likes/retweets a tweet must have to be liked/rted by bot
min_likes = 50
min_retweets = 20


# returns a list of tweets which satisfies the search query
def searchTweets():
    searchResults = client.search_recent_tweets(
        query=query, tweet_fields='public_metrics', sort_order='relevancy', max_results=100, user_auth=True)
    return searchResults.data


# determines if a tweet has been ratioed
# ratio: "when a post on social media (most commonly Twitter) has more replies than retweets or likes ,
# which likely implies that the contents of the post is controversial or unpopular."
def isRatio(tweet):
    quoteCount = tweet.public_metrics['quote_count']
    replyCount = tweet.public_metrics['reply_count']
    likeCount = tweet.public_metrics['like_count']
    if ((quoteCount > 2 * likeCount) or(replyCount > 2*likeCount)):
        return True
    return False


# determines if a tweet is popular
def isPopular(tweet):
    if (tweet.public_metrics['like_count'] > min_likes or tweet.public_metrics['retweet_count'] > min_retweets):
        return True
    return False


# takes in a list of tweets, and outputs a list of tweets which are popular and have not been ratioed
def retweetable(tweetlist):
    list = []
    for tweet in tweetlist:
        if (isPopular(tweet) and not isRatio(tweet)):
            list.append(tweet)
    return list


def likeAndRT():
    # the set of tweets which have already been retweeted/liked
    retweeted = set()
    retweetable_list = retweetable(searchTweets())
    length = len(retweetable_list)
    print('length of whole list: ', length)
    counter = len(retweeted)
    while (counter < length):
        randomPos = random.randint(0, length-1)
        randomTweet = retweetable_list[randomPos]
        if (randomTweet not in retweeted):
            retweeted.add(randomTweet)
            client.retweet(tweet_id=randomTweet.id, user_auth=True)
            client.like(tweet_id=randomTweet.id,user_auth=True)
            counter = counter + 1
            time.sleep(14400)


def main():
    # print(oauth2_user_handler.get_authorization_url())
    likeAndRT()
    # writeClient.create_tweet(text='test', user_auth=False)


if __name__ == "__main__":
    main()
