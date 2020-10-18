from bs4 import BeautifulSoup as bs
import string
import collections
import requests
import re


# ----- PRIMARY FUNCTIONS ----- #
def grabData() -> None:
    url = input('Enter Cirnopedia URL: ')
    fileName = input('Enter outfile file name: ').strip('.html') + '.html'

    page = requests.get(url).content
    with open(fileName, 'wb') as raw:
        raw.write(page)

    print('Saved .html page:', url, ' as', fileName)
    print('----- INSTRUCTIONS -----\nExtract all tables with valid data.')
    print('Rename <table id=\'rounded-corner...\' to <table id=\'ZZZ#\' with # increasing by 1.')


def processData() -> None:
    isProcessing = True
    fileName = input('Enter input file name: ').strip('.html') + '.html'
    with open(fileName, 'rb') as raw:               # Open HTML file
        page = raw.read()
    soup = bs(page, 'lxml')
    pointDict = collections.defaultdict(list)       # Creates a dict of empty lists
    pointData = extractData(soup, pointDict)

    cell = input('Enter base target cell: ')
    while isProcessing:
        choice = int(input('----- Menu -----\n1 | List of Items\n2 | Raw Item Cost\n3 | Milestones\n0 | END\nEnter choice: '))
        if choice == 0:
            isProcessing = False
        elif choice == 1:
            for item in pointData:
                print(item)
        elif choice == 2:
            calcRawItemCost(cell, pointData)
        elif choice == 3:
            calcMilestones(pointData)
        else:
            print('Invalid choice. Try again.')


# ----- HELPER FUNCTIONS ----- #
def extractData(soup, pointDict: dict) -> dict:
    num = int(input('Enter # of tables: '))
    for i in range(1, num+1):
        tableName = 'ZZZ' + str(i)
        table = soup.find('table', attrs={'id': tableName}).find('tbody').find_all('tr')
        for row in table:
            textPoints = row.find('td').text.strip()                # Grabs raw number with commas
            itemList = row.text.replace(textPoints, '', 1).split()  # Removes points from item name, splits into list
            if 'x' in itemList[-1]:                                 # If 'x#' exists in last part of item name, get rid of it
                itemList = itemList[:-1]
            if re.search('[a-zA-Z]', itemList[0]):                  # If item name contains letters, remove all numbers in front of name
                itemList[0] = itemList[0].lstrip(string.digits)
            item = ' '.join(itemList)                               # Combines item list parts into item name
            points = int(textPoints.replace(',', ''))               # Turns raw number into integer
            if 'QP' in item:                                        # Makes QP specific dict entry
                pointDict['Total QP'] += [points]
            else:
                pointDict[item] += [points]                         # Adds number to item into dict
    return pointDict


# ----- CHOICE 2 ----- #
def calcRawItemCost(cell, pointData: dict) -> None:
    invalid = True
    while invalid:
        item = input('Enter item name exactly: ')
        if item in pointData:
            invalid = False
        else:
            print('Invalid Item Name. See valid list below:')
            for k in pointData:
                print(k)
            print('\n')
    pretty()
    print('=IFS(', end='')
    index = 0
    lastVal = 0
    for val in reversed(sorted(pointData[item])):
        print(cell + '>=' + str(val) + ',' + str(index), end=',')
        index += 1
        lastVal = val
    print(cell + '<' + str(lastVal) + ',' + str(index) + ')')
    pretty()


# ----- CHOICE 3 ----- #
def calcMilestones(pointData: dict) -> None:
    invalid = True
    while invalid:
        item = input('Enter item name exactly: ')
        if item in pointData:
            invalid = False
        else:
            print('Invalid Item Name. See valid list below:')
            for k in pointData:
                print(k)
    cell = input('Enter target cell: ')
    pretty()
    print('=IFS(', end='')
    index = len(pointData[item])
    for val in sorted(pointData[item]):
        if val >= 1000000:
            val /= 1000000
            if val % 1 == 0:
                val = round(val)
            print(cell + '=' + str(index) + ',\"' + str(val), 'M\"', end=',')
        elif val >= 1000:
            val /= 1000
            if val % 1 == 0:
                val = round(val)
            print(cell + '=' + str(index) + ',\"' + str(val), 'K\"', end=',')
        else:
            if val % 1 == 0:
                val = round(val)
            print(cell + '=' + str(index) + ',\"' + str(val) + '\"', end=',')
        index -= 1
    print(cell + '=0,\"--\")')
    pretty()


# ----- DECORATOR FUNCTION ----- #
def pretty() -> None:
    print('=' * 50)
    

def main():
    if input('Type \'1\' to grab page data. Type anything else to start processing data: ').strip() == '1':
        grabData()
    else:
        processData()


if __name__ == '__main__':
    main()
