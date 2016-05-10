import sys, time, random
import getpass, urlparse
import socks, socket
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
import unicodedata

controller = Controller.from_port(port=9051)


def newIdentity():
    controller.authenticate()
    controller.signal(Signal.RELOAD)

def FirefoxProfileSettings():
	profile=webdriver.FirefoxProfile()
	profile.set_preference('network.proxy.type', 1)
	profile.set_preference('network.proxy.socks', '127.0.0.1')
	profile.set_preference('network.proxy.socks_port', 9050)

	return profile

def normText(unicodeText):
	return unicodedata.normalize('NFKD', unicodeText).encode('ascii','ignore')



def ConnectDatabase():
<<<<<<< HEAD
    conn = pymysql.connect(host='*********',
                    user = 'root',
                    passwd = '********',
=======
    conn = pymysql.connect(host='***********',
                    user = 'root',
                    passwd = '**********',
>>>>>>> 770b9b660a3e9f4590b2fa214789065085923e43
                    db='linkedin',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
    return conn

def queryTable(newPerson):
    conn = ConnectDatabase()
    print newPerson
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO `newData`(`pid`,`first`,`last`,`name`,`cw`,`title`,`affiliation`,`location`,`industry`,`school`,`degree`,`timeperiod`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",newPerson)
            #result = cursor.fetchone()

        conn.commit()
    finally:
        conn.close()


def writeTofile(content):
    page = BeautifulSoup(content,'html.parser')
    file = open(page.title.string+".html","w")
    content = normText(page.prettify())
    file.write(content)
    file.close()

def appendUrl(url):
    file = open("urlRepo.txt","a")
    file.write("\n"+url)
    file.close()

def normText(unicodeText):
    return unicodedata.normalize('NFKD', unicodeText).encode('ascii','ignore')

def viewBot(browser, pidNumber):
    conn = ConnectDatabase()
    print "database connected"
    results = []
    response = True
    browsers = []
    url = browser.current_url
    i = 0
    browsers.append(browser)
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT DISTINCT * FROM `pea` where (pid >%s and pid<=887537) GROUP BY pid',pidNumber)
            results = cursor.fetchall()

        conn. commit()
    finally:
        conn.close()
    visited = {}
    print "got results"
    count = len(results)
    foundLink = None
    if results:
        for result in results:
            values = [result['pid'], result['first'], result['last'], result['name']]

            school = "noSchool"
            degree = "noDegree"
            timeperiod = "noTime"

            time.sleep(random.uniform(5,10))

            while response:
                try:
                    if browser.find_element_by_id('first-name') or browser.find_element_by_id('session_key-login'):
                        print "linkedin people found us. I am reloading"
                        newIdentity()
                        browsers.append(webdriver.Firefox(firefox_profile = FirefoxProfileSettings()))
                        browsers[i].close()
                        i = i + 1
                        time.sleep(random.uniform(10, 20))
                        browsers[i].get(url)
                        viewBot(browsers[i], result['pid'])
                    else:
                        response = False

                except NoSuchElementException as noele:
                    print "good to go!"
                    response = False

            try:
                firstNameElement = browser.find_element_by_id("firstName")
                lastNameElement = browser.find_element_by_id("lastName")
                firstNameElement.clear()
                lastNameElement.clear()
                lastNameElement.send_keys(result['last'])
                firstNameElement.send_keys(result['first'])
                lastNameElement.submit()

            #os.system('clear')
                count = count -1
                print "[+] Sucess, bot will start crawling"
                print str(count)+" remaining"
                #download the html source
                #write logic to check if the page has multiple links
                if not browser.find_elements_by_class_name('fn'):
                    print "page has results checking headline"
                    response = True
                    while response:
                        try:
                            if browser.find_element_by_id('first-name') or browser.find_element_by_id(
                                    'session_key-login'):
                                print "linkedin people found us. I am reloading"
                                newIdentity()
                                browsers.append(webdriver.Firefox(firefox_profile=FirefoxProfileSettings()))
                                browsers[i].close()
                                i = i + 1
                                time.sleep(random.uniform(10, 20))
                                browsers[i].get(url)
                                viewBot(browsers[i], result['pid'])
                            else:
                                response = False

                        except NoSuchElementException as noele:
                            print "good to go!"
                            response = False
                    elements = browser.find_elements_by_class_name('headline')
                    if elements:
                        for element in elements:
                            div = element.find_elements_by_xpath("//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'"+result['school']+"')]")
                            div2 = element.find_elements_by_xpath("//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'"+result['cw']+"')]")
                            div3 = element.find_elements_by_xpath(
                                "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'" +
                                result['affiliation'] + "')]")
                            if div or div2 or div3:
                                print "check anchors"
                                anchors = element.find_elements_by_xpath('..')
                                for anchor in anchors:
                                    #print type(result['school'])
                                    if (normText(result['school']).lower() in normText(anchor.text).lower()) or(normText(result['affiliation']).lower() in normText(anchor.text).lower()) or (normText(result['cw']).lower() in normText(anchor.text).lower()):
                                        print "found the original person"
                                        foundLink = anchor.find_element_by_css_selector('a')
                                        #writeTofile(browser.page_source)
                                    #end of if results
                            #end of if div
                        #write insert into command here
                        #queryTable(values)
                        browser.get(foundLink.get_attribute("href"))
                        response = True
                        while response:
                            try:
                                if browser.find_element_by_id('first-name') or browser.find_element_by_id(
                                        'session_key-login'):
                                    print "linkedin people found us. I am reloading"
                                    newIdentity()
                                    browsers.append(webdriver.Firefox(firefox_profile=FirefoxProfileSettings()))
                                    browsers[i].close()
                                    i = i + 1
                                    time.sleep(random.uniform(10, 20))
                                    browsers[i].get(foundLink.get_attribute("href"))
                                    viewBot(browsers[i], result['pid'])
                                else:
                                    response = False

                            except NoSuchElementException as noele:
                                print "good to go!"
                                response = False

                    #end of if elements
                #end of browser
                appendUrl(normText(browser.current_url))
                #insert into database here
                #if browser.find_element_by_xpath('//p[@data-section="headline"]'):
                    #cw
                values.append(browser.find_element_by_xpath('//p[@data-section="headline"]').text)
                #if browser.find_element_by_class_name("item-title"):
                    #title
                values.append(browser.find_element_by_class_name("item-title").text)
                #if browser.find_element_by_class_name("item-subtitle"):
                    #affiliation
                values.append(browser.find_element_by_class_name("item-subtitle").text)
                #if browser.find_element_by_class_name("locality"):
                    #location
                values.append(browser.find_element_by_class_name("locality").text)
                #if browser.find_element_by_class_name("descriptor"):
                    #industry
                values.append(browser.find_element_by_class_name("descriptor").text)

                values.append(school)
                values.append(degree)
                values.append(timeperiod)
                if browser.find_elements_by_id("education"):
                    education = browser.find_elements_by_id("education")
                    if type(education) is list:
                        for edu in education:
                            values.remove(school)
                            values.remove(degree)
                            values.remove(timeperiod)

                            if edu.find_element_by_class_name("item-title") is list:
                                for sch in edu.find_element_by_class_name("item-title"):
                                    school = sch.text
                            else:
                                school = edu.find_element_by_class_name("item-title").text
                            if edu.find_element_by_class_name("item-subtitle") is list:
                                for deg in edu.find_element_by_class_name("item-subtitle"):
                                    degree = deg.text
                            else:
                                degree = edu.find_element_by_class_name("item-subtitle").text
                            if edu.find_element_by_class_name("date-range") is list:
                                for ti in edu.find_element_by_class_name("date-range"):
                                    timeperiod = ti.text
                            else:
                                timeperiod = edu.find_element_by_class_name("date-range").text

                            values.append(school)
                            values.append(degree)
                            values.append(timeperiod)
                            print tuple(values)
                            queryTable(tuple(values))
                    else:
                        if education.find_element_by_class_name("item-title"):
                            values.remove(school)
                            values.remove(degree)
                            values.remove(timeperiod)
                            school = browser.find_elements_by_class_name("item-title").text
                            values.append(school)
                            values.append(degree)
                            values.append(timeperiod)
                        if education.find_element_by_class_name("item-subtitle"):
                            values.remove(degree)
                            values.remove(timeperiod)
                            degree=education.find_element_by_class_name("item-subtitle").text
                            values.append(degree)
                            values.append(timeperiod)
                        if education.find_element_by_class_name("date-range"):
                            values.remove(timeperiod)
                            timeperiod = education.find_element_by_class_name("date-range").text
                            values.append(timeperiod)
                        queryTable(tuple(values))

                writeTofile(browser.page_source)
            except NoSuchElementException as Noe:
                print 'the stacktace is : (%s)' % Noe
            except StaleElementReferenceException as ele:
                print "stacktrace is: (%s)" % ele
                print "I am writing all results to a file"
                writeTofile(browser.page_source)

def main():
    browser = []
    browser.append(webdriver.Firefox(firefox_profile = FirefoxProfileSettings()))
    browser[0].get("https://www.linkedin.com/in/jeffweiner08")
    response = True
    i = 0
    #loginpage = browser.find_element_by_id('first-name')
    while response:
        try:
            loginpage = browser[i].find_element_by_id('first-name')
            if loginpage or browser[i].find_element_by_id('session_key-login'):
                print "Linkedin found us, changing Identity"
                time.sleep(random.uniform(10,20))
                newIdentity()
                browser.append(webdriver.Firefox(firefox_profile = FirefoxProfileSettings()))
                browser[i].close()
                i = i + 1
                browser[i].get("https://www.linkedin.com/in/jeffweiner08")
            else:
                response = False
        except NoSuchElementException:
            response = False
    viewBot(browser[i], 1478)
    browser[i].close()

if __name__ == "__main__":
    main()
