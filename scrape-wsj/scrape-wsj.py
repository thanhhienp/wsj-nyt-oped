# Script to scrape the Wall Street Journal op-ed section
import pandas as pd
import argparse
from bs4 import BeautifulSoup
import requests

# parser object to receive command-line arguments
parser = argparse.ArgumentParser(description='Obtain password')
parser.add_argument('password', type=str, help='WSJ account password')
args = parser.parse_args()

# log-in credentials for WSJ
email = 'thanhp@princeton.edu'
password = args.password
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

# List of article types that should be scraped
articleTypeList = ['Commentary', 'Review & Outlook', 'Wonder Land']

# url for scraping
testurl = 'https://www.wsj.com/news/archive/2021/01/01'

# Retrieve the page
dayPage = requests.get(testurl, headers=headers)
daySoup = BeautifulSoup(dayPage.content, 'html.parser')

# Retrieve page main contents, list of flashlines (article types) and headlines
dailyMain = daySoup.main
flashlines = dailyMain.find_all('div', class_='WSJTheme--articleType--34Gt-vdG')
headlines = dailyMain.find_all('div', class_='WSJTheme--headline--7VCzo7Ay')

# Empty list for article information
opinion = {'Headline': [], 'URL': [], 'Type': [], 'Text': []}

# Get list of opinion articles
for idx in range(len(flashlines)):
    type = flashlines[idx].span.get_text()
    if type in articleTypeList:
        opinion['Headline'].append(headlines[idx].a.get_text())
        opinion['URL'].append(headlines[idx].a.get('href'))
        opinion['Type'].append(type)

# parse content within an opinion page
for url in opinion['URL']:
    opinionPage = requests.get(url, headers=headers)
    opinionSoup = BeautifulSoup(opinionPage.content, 'html.parser')
    opinionContent = opinionSoup.find('div', class_='article-content')
    opinion['Text'] = [s.get_text() for s in opinionContent.find_all('p')]

print(opinion)