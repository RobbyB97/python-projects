"""
Author: Robby Bergers
Assignment: 7
Course: CSC-360
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import lxml

global log      # Logger
log = logging.getLogger('debug')

headers = {'user-agent': '007 (Robby B) bergersr@my.easternct.edu'}     # Ethical scraping :P


def total(inp, sum=0):      # I: List O: sum of list
    for element in inp:
        sum += int(element)
    return sum


def problemOne():
    # Get soup
    page = requests.get('https://gdancik.github.io/CSC-360/data/notes/schedule.html', headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soup.prettify()
    # Get name from header
    name = soup.find('h1').text
    names = name.split()
    name = names[0] + " " + names[1][:-2]
    # Get table
    tabl = soup.find('table')
    titles = []
    table = {}
    for row in tabl.find_all('tr'):
        if row.find('th'):
            for data in row.find_all('th'):
                title = data.text
                titles.append(title)
            for element in titles:
                diccc = {element: []}
                table.update(diccc)
            log.warning('TABLE Format:\n %s \n' % table)
        else:
            i = 0
            for data in row.find_all('td'):
                table[titles[i]].append(data.text)
                i += 1
            log.warning('Row complete:\n %s \n' % table)

    log.warning('table complete...\n')
    for element in table[' # credits']:
        element = int(element.lstrip())

    numClasses = len(table[' # credits'])
    numCredits = total(table[' # credits'])
    print(name, 'is teaching', str(numClasses), 'classes. (' + str(numCredits), 'credits)')
    return


def parser(x):      # For finding class of element with multiple classes
    return x in x.split()


def problemTwo():
    page = requests.get('http://www.easternct.edu/computerscience/faculty/', headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    for table in soup.find_all('table'):
        print(table)
        tables = table.findChildren('tr')[1:]
    print(tables)
    f = open('problem2tables.txt', 'w')
    f.write(str(tables))
    f.close()
    #TODO: This problem :(
    return


if __name__ == '__main__':
    problemOne()
    problemTwo()
