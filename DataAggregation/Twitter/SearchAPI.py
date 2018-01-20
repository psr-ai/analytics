from DataAggregation.Twitter.API import api
import tweepy


def historical_search(query, till_date=None):
    output = []
    max_tweets = 1000
    for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
        output.append(status)
    return output

