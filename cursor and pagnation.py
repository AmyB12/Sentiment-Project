# import tools required for the streaming of relevant tweets
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler

import twitter_cred


# Cursor-based pagination works by returning a pointer to a specific item in the
# dataset. This form of pagination is able handle real time data.
# Pagination is a process that is used to divide a large data into smaller discrete
# pages.



# Twitter Client
class TwitterClient():
    def __init__(self, twitter_user=None):  # None is default and will be used if no user is specified
        self.auth = TwitterAuthenticator().authenticate_twitter_app()  # object to properly authenticate app
        self.twitter_client = API(self.auth)  # passing the authenticator to the API to be checked there

        self.twitter_user = twitter_user  # this allows anyone that wants to use code to specify the Twitter user

    # to get the tweets (num_tweets is for amount of tweets wanted to show)
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []  # define list
        # loop through tweets a certain number of tweets and store each into the list
        # from the API there is a user_timeline method which allows you to get the tweets from timeline
        # .item is a method from cursor to help specify the number of tweets we want, we add num_tweets to for that
        # id would be for telling who the Twitter user is
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


    # parameters for the class Stream//fetch tweets filename added because it was in the __init__ and made the computer
    # think that the access token secret was  not there



# basic listener class to print tweets received to stdout.
class StdOutListener(Stream):
    # StdOutListener is a subclass of Stream where is it adding additional functions to stream
    # constructor to associate the object to a filename


    # when removed
    # Error on_data 'StdOutListener' object has no attribute
    # 'fetch_tweets_filename'


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


if __name__ == "__main__":
    # Authenticate using config.py and connect to Twitter Streaming API.
    # what is stored in hash_tag_list and the file in fetch_tweets_filename
    hash_tag_list = ["Kakashi", "Sasuke", "Raikage", "Asuma"]
    fetch_tweets_filename = "tweets.txt"

    twitter_client = TwitterClient('tunboski')  # twitter client object
    # 'pycon' is the Twitter user instead of none (my account) it will go through pycon profile instead
    print(twitter_client.get_home_timeline_tweets(2))  # testing the object to get twitter timeline

    # # # defining the twitter streamer object # # #
    # twitter_streamer = TwitterStreamer()
    # # # calling the method stream_tweets which takes 2 parameters # # #
    # twitter_streamer.stream_tweets(fetch_tweets_filename, hash_tag_list)


    # when removed fetch_tweets_filename and put just tweets.txt
    # and remove the __init__
    # Error on_data write() argument must be str, not bytes

