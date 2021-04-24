# Script to scrape the Wall Street Journal op-ed section, from 1998 to present
# Run using 'python scrape-wsj.py [start YYYY] [start MM] [start DD] [end YYYY] [end MM] [end DD]
from datetime import date
import datetime
import argparse
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# parser object to receive command-line arguments
parser = argparse.ArgumentParser(description='Obtain password')
parser.add_argument('startYear', type=int, help='Start Year (YYYY)')
parser.add_argument('startMonth', type=int, help='Start Month (MM)')
parser.add_argument('startDate', type=int, help='Start Date (DD)')
parser.add_argument('endYear', type=int, help='End Year (YY)')
parser.add_argument('endMonth', type=int, help='End Month (MM)')
parser.add_argument('endDate', type=int, help='End Date (DD)')
args = parser.parse_args()

# List of months with corresponding number of days
months28Days = [2]
months30Days = [4, 6, 9, 11]
months31Days = [1, 3, 5, 7, 8, 10, 12]

# Retrieve today's date, month, year
today = date.today()
todayDate = int(today.strftime("%d"))
todayMonth = int(today.strftime("%m"))
todayYear = int(today.strftime("%Y"))


def numberOfDays(month, year):
    '''
    Input a month and year, and return the number of days in that month
    '''
    if month in months28Days and year % 4 == 0:
        days = 29
    elif month in months28Days and year % 4 != 0:
        days = 28
    elif month in months30Days:
        days = 30
    elif month in months31Days:
        days = 31
    return days


def validateArguments(year, month, date):
    '''
    Input year, month, date and validate the values
    '''
    assert year in range(1998, todayYear + 1), "Year must be between 1998 and " + todayYear
    assert month in range(1, 13), 'Month must be between 1 and 12'
    if month in months28Days and year % 4 == 0:
        assert date in range(1, 30), 'Date for February in leap year must be between 1 and 29'
    elif month in months28Days and year % 4 != 0:
        assert date in range(1, 29), 'Date for February must be between 1 and 28'
    elif month in months30Days:
        assert date in range(1, 31), 'Date must be between 1 and 30 for this month'
    elif month in months31Days:
        assert date in range(1, 32), 'Date must be between 1 and 31 for this month'
    if year == todayYear:
        assert month <= todayMonth, "Date is in the future"
        assert date <= todayDate, "Date is in the future"


print('Validating start date')
validateArguments(args.startYear, args.startMonth, args.startDate)
print('Validating end date')
validateArguments(args.endYear, args.endMonth, args.endDate)
assert datetime.date(args.startYear, args.startMonth, args.startDate) <= \
       datetime.date(args.endYear, args.endMonth, args.endDate), "End date has to be after or the same as start date"

# header for WSJ site
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

# List of article types that should be scraped - Columns under Opinion, except for Reviews and Audio/Video content
articleTypeList = ['Commentary', 'Review & Outlook', 'Letters', 'The Americas', 'Upward Mobility', 'Political Economics',
                   'Free Expression', 'East is East', 'Politics & Ideas', 'Wonder Land', 'Business World',
                   'The Weekend Interview', 'Inside View', 'Main Street', 'Global View', 'Declarations',
                   'Future View', 'Notable & Quotable', 'Best of the Web']

# create list of url for scraping
urls = []

print('Retrieving opinion URLs')

for year in range(args.startYear, args.endYear + 1):
    for month in range(1, 13):
        if year == args.startYear and month < args.startMonth:
            continue
        if year == args.endYear and month > args.endMonth:
            break
        daysRange = numberOfDays(month, year)
        for day in range(1, daysRange + 1):
            if year == args.startYear and month == args.startMonth and day < args.startDate:
                continue
            if year == args.endYear and month == args.endMonth and day > args.endDate:
                break
            dayurl = 'https://www.wsj.com/news/archive/' + str(year) + '/' + str(month).zfill(2) + '/' + str(day).zfill(2)
            urls.append(dayurl)


# Scrape articles from the list of urls
opinions = {'Date': [], 'Headline': [], 'Type': [], 'URL': [], 'Text': []}

print("Retrieving " + str(len(urls)) + " day(s) of articles")
for index in range(len(urls)):
    if index % 5 == 0:
        print('Reached the ' + str(index) + 'th day.', end='\r')
    # Retrieve a day's page
    dayPage = requests.get(urls[index], headers=headers)
    daySoup = BeautifulSoup(dayPage.content, 'html.parser')

    # Retrieve page main contents, list of flashlines (article types) and headlines
    dailyMain = daySoup.main
    flashlines = dailyMain.find_all('div', class_='WSJTheme--articleType--34Gt-vdG')
    headlines = dailyMain.find_all('div', class_='WSJTheme--headline--7VCzo7Ay')

    # Empty dict for article information
    opinion = {'Date': [], 'Headline': [], 'Type': [], 'URL': []}

    # Get list of opinion articles
    for idx in range(len(flashlines)):
        type = flashlines[idx].span.get_text()
        if type in articleTypeList:
            opinion['Headline'].append(headlines[idx].a.get_text())
            opinion['URL'].append(headlines[idx].a.get('href'))
            opinion['Type'].append(type)
            opinion['Date'].append(urls[index][-10:])

    # parse content within an opinion page
    for idx in range(len(opinion['URL'])):
        opinionPage = requests.get(opinion['URL'][idx], headers=headers)
        opinionSoup = BeautifulSoup(opinionPage.content, 'html.parser')
        opinionContent = opinionSoup.find('div', class_='article-content')
        opinions['Headline'].append(opinion['Headline'][idx])
        opinions['URL'].append(opinion['URL'][idx])
        opinions['Type'].append(opinion['Type'][idx])
        opinions['Date'].append(opinion['Date'][idx])
        text = [s.get_text() for s in opinionContent.find_all('p')]
        cleanedText = ''
        for p in text:
            new = p.replace('\n', '')
            new = re.sub(' +', ' ', new)
            new = new + '\n'
            cleanedText += new

        opinions['Text'].append(cleanedText)


# Export dataset
print('Exporting data to csv')
dataset = pd.DataFrame(opinions)
name = './scraped-wsj-data/WSJ_' + str(args.startYear) + '-' + str(args.startMonth) + '-' + str(args.startDate) + '_' + str(args.endYear) + \
       '-' + str(args.endMonth) + '-' + str(args.endDate) + '.csv'
dataset.to_csv(name, index=False)

print('All done!')
