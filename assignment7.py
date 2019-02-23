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
import matplotlib.pyplot as plt
import time

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
    namesList = []
    officeList = []
    x = {}      #{namesList: officeList}
    page = requests.get('http://www.easternct.edu/computerscience/faculty/', headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    for row in soup.find_all('tr', {'class': 'row-1 odd'}):
        namesList.append(row.text[1:-1])
    log.warning('namesList:\n' + str(namesList))
    for row in soup.find_all('tr', {'class': 'row-3 odd'}):
        officeList.append(row.text[1:-1])
    log.warning('officeList:\n' + str(officeList))
    if not (len(namesList) == len(officeList)):
        log.warning('Uh oh, the lists don\'t make no sense')
    for i in range(0, len(namesList)):
        tempdic = {namesList[i]: officeList[i]}
        x.update(tempdic)
    print('{:20}'.format('Name') + '\t\tOffice')
    for key in x.keys():
        print('{:20}'.format(str(key)) + '\t\t' + x[key])
    return


def getRating(url):
    time.sleep(1)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find('div', {'class': parser('title-wrapper')}).find('h1')
    name = name.text.split('(')
    name = str(name[0].strip())
    rating = str(soup.find('strong', {'title': parser('based')}))
    ratings = rating.split("\"")
    rating = ratings[1]
    ratings = rating.split()
    rating = float(ratings[0])
    return {name: rating}

def problemThree():
    links = ['https://www.imdb.com/title/tt0109830/?ref_=fn_al_tt_1', 'https://www.imdb.com/title/tt0076759/?ref_=fn_tt_tt_1', 'https://www.imdb.com/title/tt0368226/?ref_=nv_sr_2', 'https://www.imdb.com/title/tt2980516/?ref_=nv_sr_1', 'https://www.imdb.com/title/tt0145487/?ref_=nv_sr_5']

    ratings = {}
    for item in links:
        ratings.update(getRating(item))
    print(ratings)
    plt.title('Movie ratings!')
    plt.bar(range(len(ratings)), list(ratings.values()), align='center')
    plt.xticks(range(len(ratings)), list(ratings.keys()))
    plt.show()


if __name__ == '__main__':
    problemOne()
    problemTwo()
    problemThree()