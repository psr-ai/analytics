import requests
import json

headers = {
    # Request headers
    'X-Api-Key': 'ex4fen9g2zh63d9kkg329mu6'
}

data = dict()
data['queryString'] = 'banks'
data['queryContext'] = dict()
data['queryContext']['curations'] = ["ARTICLES"]

# response = requests.post('http://api.ft.com/content/search/v1', json.dumps(data),
#                          headers=headers)

# response = requests.get('http://api.ft.com/site/v1/pages', headers=headers)
# print(len(json.loads(response.text)['pages']))

response = requests.get('http://api.ft.com/content/items/v1/68b9365c-286d-11e6-8ba3-cdd781d02d89', headers=headers)
print(response.text)
# for post in json.loads(response.text)['pages']:
#     print(post)
#     print(requests.get(post['apiUrl'] + '/main-content', headers=headers).text)
# for post in json.loads(response.text)['results'][0]['results']:
#     print(post['id'])
