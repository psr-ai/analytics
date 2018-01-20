import feedparser
import datetime
import time
import configparser


def append_entry_to_file(entry):
    print(entry['title'])


def update_configuration_file():
    with open('rss_feeds_configuration.ini', 'w') as configfile:
        feed_links.write(configfile)


def get_configuration_file():
    feed_links.read('rss_feeds_configuration.ini')


feed_links = configparser.ConfigParser()
while True:
    configuration_update = False
    get_configuration_file()
    for feed_link in feed_links.sections():
        feed_link = feed_links[feed_link]
        id_of_first_link = ''
        feeds = feedparser.parse(feed_link['link'])
        if feed_link['feed_updated_on'] is '' or datetime.datetime.strptime(feeds['updated'], '%a, %d %b %Y %H:%M:%S %Z') > datetime.datetime.strptime(feed_link['last_updated'], '%a, %d %b %Y %H:%M:%S %Z'):
            configuration_update = True
            print('Feeds of ' + feed_link['link'] + ' updated on: ' + feeds['updated'])
            feed_link['feed_updated_on'] = feeds['updated']
            for entry in feeds['entries']:
                if entry[feed_link['id_field']] != feed_link['last_entry_id']:
                    if id_of_first_link == '':
                        id_of_first_link = entry[feed_link['id_field']]
                    append_entry_to_file(entry)
                    print(feed_link['link'] + ': ' + entry['title'])
                else:
                    break

            if id_of_first_link != '':
                feed_link['last_entry_id'] = id_of_first_link

    if configuration_update:
        update_configuration_file()

    time.sleep(60)
# for param in feeds['entries']:
#     print(param['title'] + ": " + param['published'])
