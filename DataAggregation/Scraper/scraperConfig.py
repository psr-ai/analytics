URL = 'https://www.facebook.com/search/latest/?q=\'india\''

# login details dom
login = {
    'username_dom': [{'type': 'xpath', 'name': '//*[@id=\"email\"]'}],
    'password_dom': [{'type': 'name', 'name': 'pass'},],
    'details': {'username': '', 'password': ''}
}

# social_entity can be a Facebook post, a Tweet or a News Article
social_entity_dom = {
    'path': [{'type': 'class', 'name': 'userContentWrapper'}],
    # all the below paths are relative to the path variable in social entity dom
    'text': [{'type': 'class', 'index': 0, 'name': 'userContent'}],
    'time': [{'type': 'class', 'index': 0, 'name': '_5ptz'}, {'type': 'attribute', 'name': 'title'}],
    'link_to_entity': [{'type': 'class', 'index': 0, 'name': '_5pcp'}, {'type': 'tag', 'index': 0, 'name': 'a'}, {'type': 'attribute', 'name': 'href'}],
    'activity': [{'type': 'class', 'index': 0, 'name': '_5pbw'}],
    'likes': [{'type': 'class', 'index': 0, 'name': '_4arz'}]
}


