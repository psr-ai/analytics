import feedparser

feeds = feedparser.parse('https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=w&output=rss')
for param in feeds['entries']:
    print(param['title'])
# for param in feeds['entries']:
#     print(param['title'] + ": " + param['published'])
