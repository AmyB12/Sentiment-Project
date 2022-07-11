# import tools required for the streaming of relevant tweets
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler

import twitter_cred
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Visualise the twitter data 
"""


# Twitter Client
class TwitterClient():
    def __init__(self, twitter_user=None):  # None is default and will be used if no user is specified
        self.auth = TwitterAuthenticator().authenticate_twitter_app()  # object to properly authenticate app
        self.twitter_client = API(self.auth)  # passing the authenticator to the API to be checked there

        self.twitter_user = twitter_user  # this allows anyone that wants to use code to specify the Twitter user

    # function to interact with api and extract data from the tweets
    def get_twitter_client_api(self):
        return self.twitter_client

    """ 
    to get the tweets (num_tweets is for amount of tweets wanted to show)
    loop through tweets a certain number of tweets and store each into the list
    from the API there is a user_timeline method which allows you to get the tweets from timeline
    .item is a method from cursor to help specify the number of tweets we want, we add num_tweets to for that
    id would be for telling who the Twitter user is
    """

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []  # define list
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)  # store the tweets to the list
        return tweets

    # play around with the others and understand how they work
    # get list of friends
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.get_friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    # get the top tweets on home timeline
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# Twitter Authenticator
# this authenticator works with the cursor and doesn't interfare with the stream method
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_cred.CONSUMER_KEY, twitter_cred.CONSUMER_SECRET)
        auth.set_access_token(twitter_cred.ACCESS_TOKEN, twitter_cred.ACCESS_TOKEN_SECRET)
        return auth


# TWEET STREAMER
class TwitterStreamer():  # class made to stream the tweets

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    # fetch_tweets_filename has the txt file and the hash_tag_list is the list of keywords
    def stream_tweets(self, fetch_tweets_filename, hash_tag_list):
        # class method to save tweets to txt file to process later
        # this handles Twitter authentication and connection to Twitter API
        listener = StdOutListener(fetch_tweets_filename, twitter_cred.CONSUMER_KEY, twitter_cred.CONSUMER_SECRET,
                                  twitter_cred.ACCESS_TOKEN, twitter_cred.ACCESS_TOKEN_SECRET)
        # filters twitter streams to capture data by keywords.
        listener.filter(track=hash_tag_list)


# basic listener class to print tweets received to stdout.
class StdOutListener(Stream):
    # StdOutListener is a subclass of Stream where is it adding additional functions to stream
    # constructor to associate the object to a filename

    def __init__(self, fetch_tweets_filename, consumer_key, consumer_secret, access_token, access_token_secret):
        # get the data and put the data in the associated file
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        # super calls the class extended(Stream) then call initialise method on class
        self.fetch_tweets_filename = fetch_tweets_filename

    def on_data(self, raw_data):  # rewriting the function of on_data
        # to help deal with possible errors
        try:
            # if successful print and write tweet into the file
            print(raw_data)
            with open(self.fetch_tweets_filename, 'a') as tf:
                tf.write(raw_data.decode('utf-8') + "\n")
            return True
        # if there was an error print the following
        except BaseException as e:
            print("Error on_data %s" % str(e))

    def on_error(self, status):  # static method won't affect object
        if status == 420:
            # if there is an error on the on_data return False
            return False
        print(status)


# analysing and categorizing the data received from Twitter
class TwitterAnalyser():
    # for analysing data
    def tweet_to_data_frame(self, tweets):
        # take the tweets and store in the pandas dataframe
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        # the different columns and info we want in the columns
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        pd.set_option("display.max_rows", None, "display.max_columns", None)
        # shows the amount of columns and rows
        return df


if __name__ == "__main__":
    twitter_client = TwitterClient()  # created twitter client
    tweet_analyser = TwitterAnalyser()

    api = twitter_client.get_twitter_client_api()  # api is to interact with the twitter_client
    # streaming tweets with whom we want the tweets from and how much screen name and count found in API doc
    tweets = api.user_timeline(screen_name="FamilyGuyonFOX", count=10)

    # print(dir(tweets[0])) to show the directories used in Twitter output
    # print(tweets[0].retweet_count) how many times tweet 0 was retweeted

    df = tweet_analyser.tweet_to_data_frame(tweets)
    # print(df.head(10))  # print first 10

    # get the average length over all tweets
    # print(np.mean(df['len']))

    # get number of likes for most liked tweet (the largest number in likes column)
    # print(np.max(df['likes']))

    # get the number of retweets for the most retweeted tweet
    # print(np.max(df['retweets']))

    # time series-the amount of something over time
    # time_likes = pd.Series(data=df['len'].values, index=df['date'])
    # time_likes.plot(figsize=(16, 4), color='r')
    # plt.show()

    # time_favourite = pd.Series(data=df['likes'].values, index=df['date'].values)
    # time_favourite.plot(figsize=(16, 4), color='r')
    # plt.show()

    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_retweets.plot(figsize=(16, 4), color='r')
    plt.show()

    # layered time series = the amount of different things over time
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16, 4), label="likes", legend=True)

    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    # plt.show()

    """
    index is the unique identifier of an item of data in a collection
    .value Return Series as ndarray or ndarray-like depending on the dtype
    """