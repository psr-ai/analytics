import time as mytime
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import DataAggregation.Scraper.scraperConfig as config
import xlsxwriter


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


def execute_scraping(till_date):
    scrape_till_date = till_date.datetime.strptime(entity['time'], '%A, %d %B %Y at %H:%M')
    previous_entity_date = datetime.now()
    time_of_post = datetime.now()
    driver = webdriver.Firefox();
    driver.get(config.URL)
    driver.implicitly_wait(5)
    if config.login:
        login(driver)
    driver.implicitly_wait(2)
    length_of_page = driver.execute_script("return document.body.scrollHeight")
    match = False
    file_made = False
    got_first_entity = False
    fetched_data = []
    last_entity_index = 0
    row_count_for_excel = 1

    while match == False:
        social_entities = dom_path_conversion(config.social_entity_dom['path'], driver, True)

        if len(social_entities) > 0:

            if not file_made:
                print('Creating workbook...')
                workbook = xlsxwriter.Workbook('E:/output.xlsx')
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, "Message")
                worksheet.write(0, 1, "Date and Time")
                worksheet.write(0, 2, "Activity")
                worksheet.write(0, 3, "URL")
                worksheet.write(0, 4, "Likes")
                print("Workbook made.")
                file_made = True

            for index in range(last_entity_index, len(social_entities)):

                entity = {
                    'message': dom_path_conversion(config.social_entity_dom['text'], social_entities[index]),
                    'time': dom_path_conversion(config.social_entity_dom['time'], social_entities[index]),
                    'activity': dom_path_conversion(config.social_entity_dom['activity'], social_entities[index]),
                    'url': dom_path_conversion(config.social_entity_dom['link_to_entity'], social_entities[index]),
                    'likes': dom_path_conversion(config.social_entity_dom['likes'], social_entities[index])
                }
                time_of_post = datetime.strptime(entity['time'], '%A, %d %B %Y at %H:%M')

                if time_of_post < scrape_till_date:
                    break

                if not got_first_entity or time_of_post <= previous_entity_date:
                    got_first_entity = True
                    previous_entity_date = time_of_post
                    fetched_data.append(entity)
                    print("Writing post in excel...")
                    worksheet.write(row_count_for_excel, 0, entity['message'])
                    worksheet.write(row_count_for_excel, 1, entity['time'])
                    worksheet.write(row_count_for_excel, 2, entity['activity'])
                    worksheet.write(row_count_for_excel, 3, entity['url'])
                    worksheet.write(row_count_for_excel, 4, entity['likes'])
                    row_count_for_excel += 1

            last_entity_index = len(fetched_data)
            last_count = length_of_page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            mytime.sleep(4)
            length_of_page = driver.execute_script("return document.body.scrollHeight;")

        if last_count == length_of_page or time_of_post<scrape_till_date:
            match = True
            if file_made:
                workbook.close()


def writeExcel(dictionary, path):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    i = 1

    worksheet.write(0, 0, "Posted By")
    worksheet.write(0, 1, "Activity")
    worksheet.write(0, 2, "Message")
    worksheet.write(0, 3, "Date and Time")
    worksheet.write(0, 4, "Likes")
    worksheet.write(0, 5, "URL")
    print("Heading written.")
    for posts in dictionary:
        print("Writing post: " + str(i))
        worksheet.write(i, 0, dictionary[posts]["postername"])
        worksheet.write(i, 1, dictionary[posts]["activity"])
        worksheet.write(i, 2, dictionary[posts]["textContent"])
        worksheet.write(i, 3, dictionary[posts]["dateTime"])
        worksheet.write(i, 4, dictionary[posts]["likes"])
        worksheet.write(i, 5, dictionary[posts]["url"])
        i += 1


execute_scraping()

