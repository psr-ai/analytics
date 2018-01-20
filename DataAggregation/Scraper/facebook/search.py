import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from DataAggregation.Scraper.ScraperException import CannotFindElement
import DataAggregation.Scraper.facebook.searchConfig as Config
import logging

log_filename = 'logs/DataAggregation/Scraper/application.log'
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info("Creating a PhantomJS driver instance...")
print("Creating a PhantomJS driver instance...")
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
driver_wait = WebDriverWait(driver, 10)
print("Trying http://www.facebook.com/")
driver.get("http://www.facebook.com/")


# opening browser and logging into the account
def dom_path_conversion(dom_path, element, return_as_an_element=False):
    for dom_elem in dom_path:
        if dom_elem['type'] == 'class':
            element = element.find_elements_by_class_name(dom_elem['name'])
            if 'index' in dom_elem and dom_elem['index'] < len(element):
                element = element[dom_elem['index']]
        elif dom_elem['type'] == 'attribute':
            element = element.get_attribute(dom_elem['name'])
        elif dom_elem['type'] == 'name':
            element = element.find_element_by_name(dom_elem['name'])
        elif dom_elem['type'] == 'xpath':
            element = element.find_element_by_xpath(dom_elem['name'])
        elif dom_elem['type'] == 'tag':
            element = element.find_elements_by_tag_name(dom_elem['name'])
            if 'index' in dom_elem and dom_elem['index'] < len(element):
                element = element[dom_elem['index']]

    if return_as_an_element:
        return element

    if dom_path[len(dom_path)-1]['type'] != 'attribute' and type(element) is not list:
        return element.text
    elif type(element) is list and len(element) is 0:
        return None
    else:
        return element


def wait_till_element_is_present(element_path, driver_instance, driver_wait_instance):
    for element in element_path:
        try:
            if element['type'] is 'xpath':
                driver_wait_instance.until(EC.presence_of_element_located((By.XPATH, element['name'])))
            elif element['type'] is 'name':
                driver_wait_instance.until(EC.presence_of_element_located((By.NAME, element['name'])))
            elif element['type'] is 'class':
                driver_wait_instance.until(EC.presence_of_element_located((By.CLASS_NAME, element['name'])))
            elif element['type'] is 'tag':
                driver_wait_instance.until(EC.presence_of_element_located((By.TAG_NAME, element['name'])))
            elif element['type'] is 'attribute':
                print("Passing the check of element since attribute is present")
                pass

        except TimeoutException:
            driver_instance.save_screenshot('logs/DataAggregation/Scraper/facebook/screen_shots/TimeoutException.png');
            print("Operation timed out. The expected element was not loaded on the screen. For screen shot, refer to "
                  "logs/DataAggregation/Scraper/facebook/TimeoutException.png")
            logging.critical("Operation timed out. The expected element was not loaded on the screen. For screen shot, "
                             "refer to logs/DataAggregation/Scraper/facebook/screen_shots/TimeoutException.png")
            driver_instance.close()
            driver_instance.quit()
            raise CannotFindElement("Operation timed out. "
                                    "Element not found: " + str(element_path) +
                                    ". For screen shot refer to logs/DataAggregation/Scraper/"
                                    "facebook/screen_shots/TimeoutException.png")


def login():
    print("Logging in...")
    logging.info("Logging in...")
    wait_till_element_is_present(Config.login['username_dom'], driver, driver_wait)
    wait_till_element_is_present(Config.login['password_dom'], driver, driver_wait)
    user_id_field = dom_path_conversion(Config.login['username_dom'], driver, True)
    user_id_field.send_keys(Config.login['details']['username'])
    password_field = dom_path_conversion(Config.login['password_dom'], driver, True)
    password_field.send_keys(Config.login['details']['password'])
    driver.save_screenshot('logs/DataAggregation/Scraper/facebook/screen_shots/LoginPage.png')
    user_id_field.send_keys(Keys.RETURN)
    print("Logged in successfully as " + Config.login['details']['username'])
    logging.info("Logged in successfully as " + Config.login['details']['username'])


def execute_scraping(search_query, till_date):
    job_starting_time = datetime.datetime.now()
    print("Job started at " + str(job_starting_time))
    scrape_till_date = datetime.datetime.strptime(till_date, '%m-%d-%Y %H:%M:%S')
    print("Scrape till date:" + " " + str(scrape_till_date))
    logging.info("Scrape till date:" + " " + str(scrape_till_date))
    new_driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])

    # for getting the logged in sessions from driver
    for cookie in driver.get_cookies():
        new_driver.add_cookie(cookie)

    new_driver_wait = WebDriverWait(new_driver, 10)
    # new_driver.switch_to.window(new_driver.window_handles[-1])
    new_driver.get(Config.URL + search_query)
    print("URL:" + Config.URL + search_query)
    logging.info("URL:" + Config.URL + search_query)
    try:
        wait_till_element_is_present(Config.social_entity_dom['path'], new_driver, new_driver_wait)
    except CannotFindElement:
        print("The search query didn't load enough elements on screen. "
              "For screen shot, refer to logs/DataAggregation/Scraper/facebook/TimeoutException.png. "
              "Returning zero elements...")
        logging.critical("The search query didn't load enough elements on screen. For screen shot, "
                         "refer to logs/DataAggregation/Scraper/facebook/TimeoutException.png. Returning "
                         "zero elements...")
        return []

    new_driver.save_screenshot("logs/DataAggregation/Scraper/facebook/screen_shots/Query.png")
    length_of_page = new_driver.execute_script("return document.documentElement.scrollHeight")
    last_count = length_of_page
    match = False
    got_first_entity = False
    fetched_data = []
    last_entity_index = 0
    posts_scrolled_through = 0

    while match is False:
        social_entities = dom_path_conversion(Config.social_entity_dom['path'], new_driver, True)

        if len(social_entities) > 0:

            for index in range(last_entity_index, len(social_entities)):
                entity = {}
                for property_name in Config.social_entity_details:
                    entity[property_name] = dom_path_conversion(Config.social_entity_details[property_name], social_entities[index])

                time_of_post = datetime.datetime.fromtimestamp(int(entity['time']))
                time_of_post_required_format = time_of_post.strftime('%m-%d-%Y %H:%M:%S')
                print("Found a post on: " + str(time_of_post))
                logging.info("Found a post on" + " " + str(time_of_post))
                print("Link of the post: " + entity['link_to_entity'])

                if time_of_post < scrape_till_date:
                    print("Scraping complete till the given date.")
                    logging.info("Scraping complete till the given date.")
                    match = True
                    break

                if not got_first_entity:
                    got_first_entity = True
                    print("Found first post at " + str(time_of_post))
                    logging.info("Found first post at " + str(time_of_post))
                    previous_entity_date = time_of_post
                    scrape_from_date = time_of_post - datetime.timedelta(minutes=1)
                    print("Starting scraping from date " + str(scrape_from_date))
                    logging.info("Starting scraping from date " + str(scrape_from_date))

                if time_of_post <= previous_entity_date:
                    if time_of_post <= scrape_from_date:
                        entity['time'] = time_of_post_required_format
                        fetched_data.append(entity)
                        print("Appended a post on" + " " + str(time_of_post))
                        logging.info("Appended a post on" + " " + str(time_of_post))

                    previous_entity_date = time_of_post
                    posts_scrolled_through += 1

                else:
                    break

            last_entity_index = posts_scrolled_through
            last_count = length_of_page
            new_driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            try:
                new_driver_wait.until(lambda drv: new_driver.execute_script("return document.documentElement.scrollHeight;") > last_count)
            except TimeoutException:
                print("Cannot scroll down more.")
                logging.info("Cannot scroll down more.")
                match = True

        if not match:
            print("Scrolled Down...")
            logging.info("Scrolled Down...")
            length_of_page = new_driver.execute_script("return document.documentElement.scrollHeight;")

        if time_of_post < scrape_till_date or last_count == length_of_page:
            match = True

    new_driver.close()
    new_driver.quit()
    return fetched_data

login()
driver.save_screenshot('logs/DataAggregation/Scraper/facebook/screen_shots/LoggedIn.png')
