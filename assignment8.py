from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import unittest

def problemOne():
    driver = webdriver.Firefox(executable_path='./geckdriver/geckodriver')
    driver.get("https://www.imdb.com")
    elem = driver.find_element_by_id("navbar-query")
    elem.clear()
    elem.send_keys("The Last: Naruto the Movie")
    elem.send_keys(Keys.RETURN)
    sleep(2)
    assert "No results found." not in driver.page_source
    row = driver.find_element_by_xpath('//tr[@class="findResult odd"]')
    row.find_element_by_tag_name('a').click()
    sleep(1)
    title = driver.find_element_by_tag_name('h1').text
    rating = driver.find_element_by_xpath('//span[@itemprop="ratingValue"]').text
    print(title, 'has a rating of', str(rating) + '.')
    driver.close()
    return

def problemTwo():
    print(add(3, 4))
    print(str(max(3, 4)))
    return
def add(x, y):
    driver = webdriver.Firefox(executable_path='./geckdriver/geckodriver')
    driver.get("https://gdancik.github.io/CSC-360/data/hw/number_cruncher.html")
    inp = driver.find_element_by_id('numbers')
    inp.clear()
    inp.send_keys(str(x)+','+str(y))
    inp.send_keys(Keys.RETURN)
    driver.find_element_by_id('btnAdd').click()
    answer = driver.find_element_by_id('answer').text
    sleep(1)
    driver.close()
    return answer
def max(x, y):
    js_inject = 'document.getElementById("btnFindMax").onclick = "maxNumbers()";\
        function maxNumbers() {\
        numArray = getNumberArray();\
        if (numArray == undefined) {\
        return;\
        }\
        var max = Math.max(numArray);\
        var div = document.getElementById("answer")\
        div.className = "correct";\
        msg = "The sum of the numbers is " + max;\
        div.innerHTML = msg; }'
    driver = webdriver.Firefox(executable_path='./geckdriver/geckodriver')
    driver.get("https://gdancik.github.io/CSC-360/data/hw/number_cruncher.html")
    driver.execute_script(js_inject)
    inp = driver.find_element_by_id('numbers')
    inp.clear()
    inp.send_keys(str(x) + ',' + str(y))
    inp.send_keys(Keys.RETURN)
    driver.find_element_by_id('btnFindMax').click()
    driver.find_element_by_id('answer').add('The maximum value is 3')
    sleep(1)
    driver.close()
    return

if __name__ == '__main__':
    problemOne()
    problemTwo()