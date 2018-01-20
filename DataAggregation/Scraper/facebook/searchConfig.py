URL = 'https://www.facebook.com/search/latest/?q='

# login details dom
login = {
    'username_dom': [{'type': 'xpath', 'name': '//*[@id=\"email\"]'}],
    'password_dom': [{'type': 'name', 'name': 'pass'},],
    'details': {'username': 'analytics.practice@outlook.com', 'password': 'hadoop123'}
}

# social_entity can be a Facebook post, a Tweet or a News Article
social_entity_dom = {
    'path': [{'type': 'class', 'name': 'userContentWrapper'}],
}
social_entity_details = {
    # all the below paths are relative to the path variable in social entity dom
    'text': [{'type': 'class', 'index': 0, 'name': 'userContent'}],
    'time': [{'type': 'class', 'index': 0, 'name': '_5ptz'}, {'type': 'attribute', 'name': 'data-utime'}],
    'link_to_entity': [{'type': 'class', 'index': 0, 'name': '_5pcp'}, {'type': 'tag', 'index': 0, 'name': 'a'}, {'type': 'attribute', 'name': 'href'}],
    'link_to_posted_by': [{'type': 'class', 'index': 0, 'name': '_5va3'}, {'type': 'tag', 'index': 0, 'name': 'a'}, {'type': 'attribute', 'name': 'href'}],
    'activity': [{'type': 'class', 'index': 0, 'name': '_5pbw'}],
    'posted_by': [{'type': 'class', 'index': 0, 'name': '_5pbw'}, {'type': 'class', 'index': 0, 'name': 'fwb'}, {'type': 'tag', 'index': 0, 'name': 'a'}],
    'posted_to': [{'type': 'class', 'index': 0, 'name': '_5pbw'}, {'type': 'class', 'index': 0, 'name': '_wpv'}],
    'likes': [{'type': 'class', 'index': 0, 'name': '_4arz'}]
}


