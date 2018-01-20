from Twitter.API import api

trends_place = api.trends_place(2295390)

for trends in trends_place:
    for trend in trends['trends']:
        print(trend['name'])
