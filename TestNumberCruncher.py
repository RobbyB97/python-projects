"""
Unit testing is an important framework for testing
classes and functions. When a script is modified,
unit tests can easily be run again to make sure
that the script still works correctly.

"""

import unittest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# set options for "headless" mode
options = Options()
#options.add_argument("--headless")

# on your own machine
driver = webdriver.Firefox(firefox_options=options, executable_path='./geckdriver/geckodriver')

# on school computer
#driver = webdriver.Firefox(executable_path='C:\geckodriver\geckodriver.exe',firefox_options = options)

localFile = "/home/robs_pc/PycharmProjects/csc360/numberCruncher.html"
driver.get("file://"+localFile)

def enterNumbers(driver, string) :
    numbers = driver.find_element_by_id("numbers")
    numbers.clear()
    numbers.send_keys(string)


# define a class that inherits from unittest.TestCase
class TestNumberCruncher(unittest.TestCase):

    # test method names must start with "test"
    def test_addNumbersValid(self) :

        ### test numbers 1,5,7 ##############################
        enterNumbers(driver, '1,5,7')
        driver.find_element_by_id('btnAdd').click()

        # test correct answer
        div = driver.find_element_by_id('answer')
        message = div.text
        self.assertEqual(message, 'The sum of the numbers is 13')

        # test correct CSS
        color = div.value_of_css_property('color')
        self.assertEqual(color, 'rgb(0, 128, 0)')

    def test_addNumbersError(self) :
        ### test numbers 1,B,7 ##############################
        enterNumbers(driver, '1,B,7')
        driver.find_element_by_id('btnAdd').click()

        # test correct message
        div = driver.find_element_by_id('answer')
        message = div.text
        self.assertEqual(message, 'Error: at least one value is not an integer')

        # test correct CSS
        color = div.value_of_css_property("color")
        self.assertEqual(color, 'rgb(255, 0, 0)')

    def test_maxNumbersValid(self) :

        ### test numbers 1,5,7 ##############################
        enterNumbers(driver, '1,5,7')
        driver.find_element_by_id('btnFindMax').click()

        # test correct answer
        div = driver.find_element_by_id('answer')
        message = div.text
        self.assertEqual(message, 'The highest number is 7')

        # test correct CSS
        color = div.value_of_css_property('color')
        self.assertEqual(color, 'rgb(0, 0, 255)')

    def test_maxNumbersError(self) :
        ### test numbers 1,B,7 ##############################
        enterNumbers(driver, '1,B,7')
        driver.find_element_by_id('btnFindMax').click()

        # test correct message
        div = driver.find_element_by_id('answer')
        message = div.text
        self.assertEqual(message, 'Error: at least one value is not an integer')

        # test correct CSS
        color = div.value_of_css_property("color")
        self.assertEqual(color, 'rgb(255, 0, 0)')



# create a suite (collection of tests)
suite = unittest.TestLoader().loadTestsFromTestCase(TestNumberCruncher)

# run the tests
unittest.TextTestRunner(verbosity=2).run(suite)
