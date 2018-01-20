import queue
import _thread

import tweepy
from DataAggregation.Scraper.Twitter.authentication import API
from DataAggregation.Scraper.Twitter.data_types import LiveStreamUserQuery, TweepyStreamQuery
from DataCleaning.corpus_cleaner import clean_text
from DataAnalysis.SentimentAnalysis.classifier import classifier
from DataAnalysis.SentimentAnalysis.feature_extractions import bag_of_words_with_counts

tweets_queue = queue.Queue()


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweets_queue.put(status)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


def process_queue():
    write_file = open("output.txt", 'w')
    while True:
        tweet_text = tweets_queue.get().text
        cleaned_tweet = clean_text(tweet_text)
        print(tweet_text)
        print("Clean Text: " + cleaned_tweet['cleaned_corpus'])
        print("URLS: " + ", ".join(map(str, cleaned_tweet['urls'])))
        print("Sentiments: " + classifier.classify(bag_of_words_with_counts(cleaned_tweet['cleaned_corpus'])))

        # try:
        #     write_file.write(tweet_text)
        #     write_file.write("\n")
        #     write_file.write("Clean Text: " + cleaned_tweet['cleaned_corpus'])
        #     write_file.write("\n")
        #     write_file.write("URLS: " + ", ".join(map(str, cleaned_tweet['urls'])))
        #     write_file.write("\n")
        # except Exception:
        #     print('Exception Occured in writing file, passing it.')
        #     pass


def process_stream():
    myStream.filter(track=tweepy_stream_query.track, locations=tweepy_stream_query.locations,
                follow=tweepy_stream_query.follow, languages=tweepy_stream_query.languages)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=API.auth, listener=myStreamListener)
tweepy_stream_query = [LiveStreamUserQuery('DonaldTrump', 'track')]
tweepy_stream_query = TweepyStreamQuery(tweepy_stream_query, API=API)


_thread.start_new_thread(process_queue, ())
_thread.start_new_thread(process_stream(), ())

# liveStreamOutput = {}
# for keyword in trackKeywords:
#     liveStreamOutput[keyword] = []

# myStream.filter(track=[0])
# myStream.filter(locations=[74.064331, 30.075927, 76.360474, 32.275232])
# myStream.filter(follow=[str(api.get_user('rai_prabh').id)])

