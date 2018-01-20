import configparser
config = configparser.ConfigParser()
config['reuters.com: World News'] = {
    'link': 'http://feeds.reuters.com/Reuters/worldNews',
    'last_entry_id': '',
}
config['reuters.com: Top News'] = {
    'link': 'http://feeds.reuters.com/reuters/INtopNews',
    'last_entry_id': '',
}
config['reuters.com: Business News'] = {
    'link': 'http://feeds.reuters.com/reuters/INbusinessNews',
    'last_entry_id': '',
}
config['reuters.com: South Asia News'] = {
    'link': 'http://feeds.reuters.com/reuters/INsouthAsiaNews',
    'last_entry_id': '',
}
config['thehindu: All News'] = {
    'link': 'http://www.thehindu.com/news/?service=rss',
    'last_entry_id': '',
}
config['bloomberg: Politics'] = {
    'link': 'http://www.bloomberg.com/politics/feeds/site.xml',
    'last_entry_id': '',
}
config['Financial Times: Financial-Services'] = {
    'link': 'http://www.ft.com/rss/companies/financial-services',
    'last_entry_id': '',
}


with open('collect_rss_feeds/configuration.ini', 'w') as configfile:
    config.write(configfile)