import tweepy
consumer_key = "aN5oFfyfehLBDTcMa7r22qiE9"
consumer_secret = "nth07Fz0fpLv5wiKjIulaBIuQhtdbkF8kn4zp9ui5PSHap9liy"
access_token = "1906973388-mvTTmD5FKtJhI5FUHjqJSeMzGUeDWOldFRJwsMZ"
access_token_secret = "w4EuikRNUx0clU1BIxCwpVBHZarAgFiYBNOra9XoBki7S"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)