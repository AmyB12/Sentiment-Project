# import tools required for the streaming of relevant tweets
from tweepy import Stream

import twitter_cred


# TWEET STREAMER
class TwitterStreamer():  # class made to stream the tweets
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
        print(status)


if __name__ == "__main__":
    # Authenticate using config.py and connect to Twitter Streaming API.
    # what is stored in hash_tag_list and the file in fetch_tweets_filename
    hash_tag_list = ["Kakashi", "Sasuke", "Raikage", "Asuma"]
    fetch_tweets_filename = "tweets.txt"

    # defining the twitter streamer object
    twitter_streamer = TwitterStreamer()
    # calling the method stream_tweets which takes 2 parameters
    twitter_streamer.stream_tweets(fetch_tweets_filename, hash_tag_list)


    # when removed fetch_tweets_filename and put just tweets.txt
    # and remove the __init__
    # Error on_data write() argument must be str, not bytes

