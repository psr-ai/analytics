from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import time as mytime
import xlsxwriter


# opening browser and loging into the account


def login(driver):
    elem = driver.find_element_by_xpath("//*[@id=\"email\"]")
    elem.send_keys("raiprabhjot")
    password = driver.find_element_by_name("pass")
    password.send_keys("prabh@123#3")
    elem.send_keys(Keys.RETURN)


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


def scout(id):
    driver = webdriver.Firefox();
    driver.get("http://www.facebook.com/" + id)
    driver.implicitly_wait(5)
    login(driver)
    driver.implicitly_wait(60)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        mytime.sleep(4)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    print("Crawling complete. Writing the results. Please wait...")

    elem1 = driver.find_elements_by_class_name("userContentWrapper")
    url = []
    date = []
    name = []
    newnames = []
    likes = []
    message = []
    for div in elem1:

        # appending message
        elem = div.find_elements_by_class_name("userContent")
        if len(elem) > 0:
            message.append(elem[0].text)
        else:
            message.append("")

            # appending date and time
        time = div.find_element_by_class_name("_5ptz").get_attribute("title")
        date.append(time)

        # appending activity and posted by
        links = div.find_elements_by_class_name("_5pbw")
        if len(links) > 0:
            name.append(links[0].text)

        else:
            name.append("")

        if len(links) > 0:
            poster = links[0].find_elements_by_class_name("fwb")
            if len(poster) > 0:
                newnames.append(poster[0].text)
            else:
                newnames.append("")
        else:
            newnames.append("")


            # appending url
        links = div.find_elements_by_class_name("_5pcp")
        if (len(links) > 0):
            linksnew = links[0].find_elements_by_tag_name("a")
            if len(linksnew) > 0:
                url.append(linksnew[0].get_attribute('href'))
            else:
                url.append('')
        else:
            url.append('')

            # appending likes
        likesData = div.find_elements_by_class_name("UFILikeSentenceText")
        if (len(likesData) > 0):
            likes.append(noOfLikes(likesData[0].text))
        else:
            likes.append(0)

    i = 0
    dictionary = {}
    while i < len(elem1):
        try:
            entryName = "post" + str(i)
            dictionary[entryName] = {}
            dictionary[entryName]['postername'] = newnames[i]
            dictionary[entryName]['activity'] = name[i]
            dictionary[entryName]['textContent'] = message[i]
            dictionary[entryName]['dateTime'] = date[i]
            dictionary[entryName]['likes'] = likes[i]
            dictionary[entryName]['url'] = url[i]

            i += 1
        except Exception:
            entryName = "post" + str(i)
            dictionary[entryName] = {}
            dictionary[entryName]['postername'] = " "
            dictionary[entryName]['activity'] = " "
            dictionary[entryName]['textContent'] = " "
            dictionary[entryName]['dateTime'] = " "
            dictionary[entryName]['likes'] = " "
            dictionary[entryName]['url'] = " "
            i += 1

    return dictionary


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


inputSentence = input("Enter the id you want to scout: ")

writeExcel(scout(inputSentence), "E:/" + inputSentence + ".xlsx")
