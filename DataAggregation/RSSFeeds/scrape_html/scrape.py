from lxml import html
import requests
import configparser
import time

# This class's constructor first takes a configuration object for how the DOM elements look for different websites. It's
# get_page_structured_data() method takes source_name which is the section name in the configuration object.


class HTMLScraper:

    def __init__(self, dom_configuration_object_path):
        self.pages_structure = HTMLScraper.read_configuration(dom_configuration_object_path)

    @staticmethod
    def get_page_content(page_url):
        try:
            return requests.get(page_url).content
        except Exception as e:
            print(e)
            print("Exception occured. Sleeping for one minute.")
            time.sleep(60)
            return HTMLScraper.get_page_content(page_url)

    @staticmethod
    def read_configuration(path):
        configuration = {}
        feed_links = configparser.ConfigParser()
        feed_links.read(path)
        for elem in feed_links.sections():
            configuration[elem] = {}
            for key in feed_links[elem]:
                configuration[elem][key] = eval(feed_links[elem][key])
        return configuration

    def get_page_structured_data(self, page_url, source_name):
        structured_page_content = {}
        tree = html.fromstring(HTMLScraper.get_page_content(page_url))
        for elem_name in self.pages_structure[source_name]:

            if self.pages_structure[source_name][elem_name]['type'] == 'xpath':
                extracted_content = tree.xpath(self.pages_structure[source_name][elem_name]['value'] + '//text()')
                extracted_content = ' '.join(extracted_content)
                if 'remove_characters' in self.pages_structure[source_name][elem_name]:
                    for pattern in self.pages_structure[source_name][elem_name]['remove_characters']:
                        extracted_content = extracted_content.replace(pattern, '')
                structured_page_content[elem_name] = extracted_content

        return structured_page_content


# html_scraper = HTMLScraper('news_websites_structure.ini')
# url = 'http://www.bloomberg.com/politics/articles/2016-06-24/' \
#       'donald-trump-in-scotland-says-brexit-vote-is-a-great-thing'
# print(html_scraper.get_page_structured_data(url, 'http://www.bloomberg.com/politics/feeds/site.xml'))




