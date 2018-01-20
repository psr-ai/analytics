from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import DataAggregation.Scraper.LiveStreamingConfig as config
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException


# opening browser and loging into the account

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


def login(driver):
    user_id_field = dom_path_conversion(config.login['username_dom'], driver, True)
    user_id_field.send_keys(config.login['details']['username'])
    password_field = dom_path_conversion(config.login['password_dom'], driver, True)
    password_field.send_keys(config.login['details']['password'])
    user_id_field.send_keys(Keys.RETURN)


def writeFile(collection, path):
    f = open(path, 'w')
    f.truncate()
    for lines in collection:
        f.write(str(collection[lines]) + "\n")


def noOfLikes(statement):
    s = statement
    count = 0

    result = ''.join([i for i in s if i.isdigit()])
    if not result.isdigit():
        if s.count(",") == 0 and " and " in s:
            return 2
        elif s.count(",") == 0 and not " and " in s:
            return 1
        elif s.count(",") == 1 and " and " in s:
            return 3
        else:
            return 0
    else:
        if " and " in s:
            return int(result) + int(s.count(',')) + 1
        else:
            return int(result)


def execute_scraping():
    driver = webdriver.Firefox();
    driver.set_window_position(-2000,0)
    driver.get(config.URL)
    driver.implicitly_wait(5)
    if config.login:
        login(driver)
    driver.implicitly_wait(5)
    while True:
        try:
            dom_path_conversion(config.update_notifier['path'], driver, True).click()
        except (NoSuchElementException, ElementNotVisibleException):
            pass


    # social_entities = dom_path_conversion(config.social_entity_dom['path'], driver, True)
    #
    # print('Creating workbook...')
    # workbook = xlsxwriter.Workbook('/Users/rai/Documents/Social Media Analytics/output.xlsx')
    # worksheet = workbook.add_worksheet()
    # worksheet.write(0, 0, "Message")
    # worksheet.write(0, 1, "Date and Time")
    # worksheet.write(0, 2, "Activity")
    # worksheet.write(0, 3, "URL")
    # worksheet.write(0, 4, "Likes")
    # print("Workbook made.")
    #
    # for social_entity in social_entities:
    #     entity = {
    #         'message': dom_path_conversion(config.social_entity_dom['text'], social_entity),
    #         'time': dom_path_conversion(config.social_entity_dom['time'], social_entity),
    #         'activity': dom_path_conversion(config.social_entity_dom['activity'], social_entity),
    #         'url': dom_path_conversion(config.social_entity_dom['link_to_entity'], social_entity),
    #         'likes': dom_path_conversion(config.social_entity_dom['likes'], social_entity)
    #     }
    #     print("Writing post in excel...")
    #     worksheet.write(row_count_for_excel, 0, entity['message'])
    #     worksheet.write(row_count_for_excel, 1, entity['time'])
    #     worksheet.write(row_count_for_excel, 2, entity['activity'])
    #     worksheet.write(row_count_for_excel, 3, entity['url'])
    #     worksheet.write(row_count_for_excel, 4, entity['likes'])
    #     row_count_for_excel += 1
    # workbook.close()

execute_scraping()