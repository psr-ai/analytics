from DataAggregation.Scraper.Twitter.authentication import API
import tweepy
import datetime
import logging
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError
from tweepy.error import TweepError
import ssl
import time
import re

print('Twitter API authenticated.')
logging.info('Twitter API authenticated.')
tweet_object_default_structure = {
    'entities': {
        'hashtags': None,
        'urls': None,
        'media': None,
        'user_mentions': None
    },
    'place': {
        'attributes': None,
        'bounding_box': None,
        'country': None,
        'country_code': None,
        'full_name': None,
        'id': None,
        'name': None,
        'place_type': None,
        'url': None
    },

}


def get_rate_limit_status_searchtweets():
    return API.rate_limit_status()['resources']['search']['/search/tweets']


def check_objects_in_tweet(tweet, queries):
    for object in tweet_object_default_structure:

        if tweet[object] is None:
            tweet[object] = tweet_object_default_structure[object]

        else:
            for key in tweet_object_default_structure[object]:
                if key not in tweet[object]:
                    tweet[object][key] = tweet_object_default_structure[object][key]

    tweet['queries_contained_in_tweet_text'] = []

    for query in queries:
        if (query.startswith("'") and query.endswith("'")) or (query.startswith('"') and query.endswith('"')):
            transformed_query = query[1:-1]
            if transformed_query.lower() in tweet['text'].lower():
                tweet['queries_contained_in_tweet_text'].append(query)

        else:
            if query.lower() in tweet['text'].lower():
                tweet['queries_contained_in_tweet_text'].append(query)

            else:
                subqueries = query.split()
                for subquery in subqueries:
                    if subquery.lower() in tweet['text'].lower():
                        tweet['queries_contained_in_tweet_text'].append(subquery)

    # Create Your Own Objects
    tweet['link_of_tweet'] = 'http://www.twitter.com/PractAnalytics/status/' + tweet['id_str']


def historical_search(query, till_date=None):
    output = []
    queries = re.split(" OR ", query)

    if till_date is not None:
        execute_till_date = datetime.datetime.strptime(till_date, '%m-%d-%Y %H:%M:%S')
        # converting the execute_till_date object to GMT
        execute_till_date = execute_till_date - datetime.timedelta(hours=5, minutes=30)

    found_required_tweets = False
    query_object = tweepy.Cursor(API.search, q=query, lang="en", count=100)
    while not found_required_tweets:
        try:
            for tweet in query_object.items():
                print("Found a tweet, id: " + tweet.id_str + " Time: " + str(tweet.created_at))
                logging.info("Found a tweet, id: " + tweet.id_str + " Time: " + str(tweet.created_at))
                if 'execute_till_date' in locals() and tweet.created_at < execute_till_date:
                    print("Breaking at " + str(tweet.created_at + datetime.timedelta(hours=5, minutes=30)))
                    logging.info("Breaking at " + str(tweet.created_at + datetime.timedelta(hours=5, minutes=30)))
                    found_required_tweets = True
                    break
                print("Appending the above tweet... TotalTweets:" + str(len(output) + 1))
                logging.info("Appending the above tweet... TotalTweets:" + str(len(output) + 1))

                check_objects_in_tweet(tweet._json, queries)
                output.append(tweet._json)

            found_required_tweets = True

        except (Timeout, ssl.SSLError, ReadTimeoutError, ConnectionError, TweepError) as exc:
            print("Connection Timed Out Exception Called.")
            logging.info("Connection Timed Out Exception Called.")
            print("Exception: " + str(exc))
            logging.info("Exception: " + str(exc))
            print("Sleeping for 120 seconds...")
            time.sleep(120)
            continue

    print("Returning " + str(len(output)) + " captured tweets...")
    logging.info("Returning " + str(len(output)) + " captured tweets...")
    return output


# historical_search('"donald trump" OR "HILLARY"', '08-04-2016 17:14:00')
# print(historical_search('donald trump', '06-30-2016 13:52:00'))
