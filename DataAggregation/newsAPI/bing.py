# import feedparser
#
# feeds = feedparser.parse('http://news.google.com/news?q=apple&output=rss')
# print(len(feeds))
# for feed in feeds['entries']:
#     print(feed['summary'])

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, json

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'a4e945d244de438ca9a1e97c4f539d93',
}

params = urllib.parse.urlencode({
    # Request parameters
    'q': 'apple',
    'count': '100',
    'offset': '200',
    'mkt': 'en-us',
    'safeSearch': 'Moderate',
})

try:
    conn = http.client.HTTPSConnection('bingapis.azure-api.net')
    conn.request("GET", "/api/v5/news/search?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    print(len(data['value']))
    for entity in data['value']:
        print(entity['description'])
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))