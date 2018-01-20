import configparser
config = configparser.ConfigParser()
config.read('rss_feeds_configuration.ini')

for data in config.sections():
    print(config[data]['feed_updated_on'])