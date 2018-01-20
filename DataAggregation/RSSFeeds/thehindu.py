import feedparser
# http://www.thehindu.com/news/?service=rss
# http://feeds.reuters.com/Reuters/worldNews
# http://www.bloomberg.com/politics/feeds/site.xml
# http://www.ft.com/rss/companies/financial-services
feeds = feedparser.parse('http://www.thehindu.com/news/?service=rss')
for param in feeds['entries']:
    print(param['link'])