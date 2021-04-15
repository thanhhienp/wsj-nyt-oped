# Script to scrape the Wall Street Journal op-ed section
# To see the scraping structure, check README.md
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
articleType = ['Commentary']
url = 'https://www.wsj.com/articles/the-j-j-covid-vaccine-pause-11618354443'

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

article_content = soup.find('div', class_='article-content')
article_text = [s.get_text() for s in article_content.find_all('p')]
print(article_text)