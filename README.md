# Topic Modelling on Wall Street Journal and New York Times Op-Ed Articles in 2020
Final project for HUM346 - Introduction to Digital Humanities, Princeton University, Spring 2021. Exploring the New York Times and Wall Street Journal op-ed articles.

## Motivation

## Methodology
### Retrieving New York Times op-eds

The New York Times has its own API for its articles that returns a json file filled with relevant information. 

It includes: an abstract for the article, a web url, a "snippet" of the article, and various metadata such as the author's name, date published, and references to images in the text. 

The New York Times limits call rates to 10 per minute and 4000 per day. It also has a fairly slow response rate, taking roughly 10 minutes to retrieve 5000 articles.

While they make it very easy to access some data, they also make it very hard to access article text. Because they limit the call rate from IPs, it is particularly difficult to get NYTimes article text past the first paragraph.

### Scraping Wall Street Journal op-eds

The Wall Street Journal has no publicly available API to retrieve articles. Hence, we wrote a python script using BeautifulSoup to scrape the necessary text.

To run the script, use 'python scrape-wsj.py [start YYYY] [start MM] [start DD] [end YYYY] [end MM] [end DD]' - e.g. 'python scrape-wsj.py 2020 01 01 2020 01 31' to retrieve op-eds in January 2020 (dates inclusive).

The script returns a csv file with each article in an entry, and contain fields "Date", "Headline", "Type" (referring to the article type, see item 4 in the Choices section below), "URL" and "Text" (containing the full text of the article).

The WSJ server has an upper limit to article scraping. It is unclear how this works exactly, but in various attempts, the server has cut off connection after scraping 150 days worth of op-eds. It is advisable to scrape at most 4 months' worth of articles in one attempt to avoid a server side interruption, which will produce no results.

Choices that were made in the scraping script:
- A script user can enter a date range in the command line to retrieve the appropriate articles. Thus, this script is rather accessible, and has re-use value for any future researchers who might be interested in using WSJ articles for research.
- The script works by accepting a date range, then generating a list of links to news articles on a given day (e.g. https://www.wsj.com/news/archive/2021/01/01 leads to a list of all news articles on January 1, 2021) and scrape all articles in a day that has an Article Type matching the list of types in the script. This means that if the archive link formatting changes, this script might not work or might require updates.
- For simplicity of coding and error handling, the script only accepts dates between 1998 and the present, even though the archive has articles from the last 4 months of 1997.
- Since the WSJ has no overarching "Opinion" type, instead the articles fall into a number of columns and newsletters, we manually went through the listed columns on the website menu, and the featured opinion authors to create a list of Article Types that would match our interest. Since we have an interest in op-eds that have a view on current politics and social affairs, any Reviews (e.g. book or movie reviews) were excluded from this selection. The list includes the following columns: 'Commentary', 'Review & Outlook', 'Letters', 'The Americas', 'Upward Mobility', 'Political Economics', 'Free Expression', 'East is East', 'Politics & Ideas', 'Wonder Land', 'Business World', 'The Weekend Interview', 'Inside View', 'Main Street', 'Global View', 'Declarations', 'Future View', 'Notable & Quotable', 'Best of the Web'._ This list can be edited should a script user be interested in other types of articles._
- The Text in the csv file has already been lightly preprocessed to remove multiple blank spaces and replicate its most natural form, as seen on the website.

### MALLET analysis on op-eds

