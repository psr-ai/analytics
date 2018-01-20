import tweepy
consumer_key = "Td7VSlbKWmSWB3ZXdkx7Z52uc"
consumer_secret = "JJCO2GX6LYYJafTvqjijsPqdVgre2HgGFIeCSe2UMgE31vScMd"
access_token = "757827555567120385-JAsLE7vaFrtLfoNdNC4JdJ1Sx5OByQw"
access_token_secret = "t50r05W4bI32XiegwuWlrRXwlFo3gSXRZY1VgijvW2zaH"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

API = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
