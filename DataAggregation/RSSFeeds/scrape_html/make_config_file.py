import configparser
config = configparser.ConfigParser()
config['reuters.com: World News'] = {
    'heading': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/h1'
    },
    'content': {
        'type': 'xpath',
        'value': '//*[@id="articleText"]',
        'remove_characters': ['\n']
    },
    'location': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[1]'
    },
    'author': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[3]'
    }
}
config['reuters.com: Top News'] = {
    'heading': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/h1'
    },
    'content': {
        'type': 'xpath',
        'value': '//*[@id="articleText"]',
        'remove_characters': ['\n']
    },
    'location': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[1]'
    },
    'author': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[3]'
    }
}
config['reuters.com: Business News'] = {
    'heading': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/h1'
    },
    'content': {
        'type': 'xpath',
        'value': '//*[@id="articleText"]',
        'remove_characters': ['\n']
    },
    'location': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[1]'
    },
    'author': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[3]'
    }
}
config['reuters.com: South Asia News'] = {
    'heading': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/h1'
    },
    'content': {
        'type': 'xpath',
        'value': '//*[@id="articleText"]',
        'remove_characters': ['\n']
    },
    'location': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[1]'
    },
    'author': {
        'type': 'xpath',
        'value': '//*[@id="articleContent"]/div/div[2]/span[3]'
    }
}
config['thehindu: All News'] = {
    'heading': {
        'type': 'xpath',
        'value': '//*[@id="left-column"]/h1'
    },
    'content': {
        'type': 'xpath',
        'value': '//*[@id="article-block"]/div/p'
    },
    'location': {
        'type': 'xpath',
        'value': '//*[@id="left-column"]/div[1]/span[2]/span'
    },
    'author': {
        'type': 'xpath',
        'value': '//*[@id="left-column"]/span'
    }
}
config['bloomberg: Politics'] = {
    'heading': {
        'type': 'xpath',
        'value': '//*[@id="content"]/div/div/article/div[1]/div[1]/header/h1/span'
    },
    'content': {
        'type': 'xpath',
        'value': '//*[@id="content"]/div/div/article/div[1]/div[3]/section/div[2]/p'
    },
    'author': {
        'type': 'xpath',
        'value': '//*[@id="content"]/div/div/article/div[1]/div[1]/header/div/div/div[1]/div/div/div/a[1]'
    }
}
with open('news_websites_structure.ini', 'w') as configfile:
    config.write(configfile)