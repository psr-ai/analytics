from Twitter.API import api
import tweepy

user = api.get_user('TheEconomist')

for status in tweepy.Cursor(api.user_timeline, id=user.id).items():
    print(status.text)
