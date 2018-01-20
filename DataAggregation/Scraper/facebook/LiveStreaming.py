import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from DataAggregation.Scraper.ScraperException import CannotFindElement
import Scraper.facebook.searchConfig as Config

driver = webdriver.Firefox()
driver_wait = WebDriverWait(driver, 10)
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
        return element.get_attribute('innerText')
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
            print("Operation timed out. The expected element was not loaded on the screen.")
            driver_instance.close()
            raise CannotFindElement("Operation timed out. Element not found: " + str(element_path))


def login():
    wait_till_element_is_present(Config.login['username_dom'], driver, driver_wait)
    wait_till_element_is_present(Config.login['password_dom'], driver, driver_wait)
    user_id_field = dom_path_conversion(Config.login['username_dom'], driver, True)
    user_id_field.send_keys(Config.login['details']['username'])
    password_field = dom_path_conversion(Config.login['password_dom'], driver, True)
    password_field.send_keys(Config.login['details']['password'])
    user_id_field.send_keys(Keys.RETURN)
    print("Logged in successfully as " + Config.login['details']['username'])


def execute_scraping(search_query):
    print("Job started at " + str(datetime.datetime.now()))
    # new_driver = webdriver.PhantomJS()
    new_driver = driver
    # for getting the logged in sessions from driver
    # for cookie in driver.get_cookies():
    #     new_driver.add_cookie(cookie)

    # new_driver_wait = WebDriverWait(new_driver, 10)
    new_driver_wait = driver_wait
    # new_driver.switch_to.window(new_driver.window_handles[-1])
    new_driver.get(Config.URL + search_query)
    print("URL:" + Config.URL + search_query)
    login()
    wait_till_element_is_present(Config.social_entity_dom['path'], new_driver, new_driver_wait)
    fetched_data = []
    found_initially_loaded_elements_on_page = False
    initially_loaded_elements_on_page = -1

    initial_entities = dom_path_conversion(Config.social_entity_dom['path'], new_driver, True)
    last_len_social_entities = len(initial_entities)

    while True:
        social_entities = dom_path_conversion(Config.social_entity_dom['path'], new_driver, True)

        if len(social_entities) > last_len_social_entities:

            if not found_initially_loaded_elements_on_page and len(initial_entities) > 0:
                for index in range(len(initial_entities)):
                    if dom_path_conversion(Config.social_entity_details['link_to_entity'], social_entities[index]) == dom_path_conversion(Config.social_entity_details['link_to_entity'], initial_entities[index]):
                        initially_loaded_elements_on_page = index
                    else:
                        break

            found_initially_loaded_elements_on_page = True
            last_len_social_entities = len(social_entities)

            for index in range(len(social_entities) - len(fetched_data) - 1, initially_loaded_elements_on_page, -1):
                entity = {};
                for property_name in Config.social_entity_details:
                    entity[property_name] = dom_path_conversion(Config.social_entity_details[property_name], social_entities[index])
                    if property_name is 'time':
                        entity[property_name] = datetime.datetime.strptime(entity[property_name], '%A, %d %B %Y at %H:%M')
                        entity[property_name] = entity[property_name].strftime('%m-%d-%Y %H:%M:%S')
                fetched_data.append(entity)
                print(entity['text'])

execute_scraping("india")
