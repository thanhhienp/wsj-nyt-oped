# Topic Modelling on Wall Street Journal and New York Times Opinion Articles in 2020
Final project for HUM346 - Introduction to Digital Humanities, Princeton University, Spring 2021. Exploring the New York Times (NYT) and Wall Street Journal (WSJ) opinion articles.

## Motivation & Hypothesis
We want to research how different news outlets opinion departments reacted to COVID-19, the 2020 US election and other potentially relevant news. Opinion departments (which includes editorials, recurring columnists, and guest contributors) are more interesting than general news because opinions usually are allowed to both be significantly more partisan and they vary a lot more on what they view as important. While all major news organizations likely covered the number of new COVID-19 cases on any given day, the opinions usually wrote about how the government should respond or how America’s response to COVID-19 shows some deeply American trait. We believe that the opinion articles are where the most interesting responses to COVID will be.

Thus, we hope to use topic modelling to identify topics of interest in the NYT (which tends to be more liberal) and the WSJ (which tends to be more conservative), then match the topics and analyze the matching keywords that arises to look into potentially different terms used to describe the events of 2020.

We think the best way to transform our research questions into a testable hypothesis is to ask: is there a significant difference in word usage between opinion articles written in The New York Times versus the Wall Street Journal when an article mentions coronavirus along with one or more keywords? What about the partisanship between these sources in representation of the pandemic and other events leading up to the 2020 election? We believe that if there is a significant difference, it would provide evidence that the two opinion sections have different conceptions of how the events of 2020-21 unfolded and what mattered most to each side. It would also showcase the terminologies used and their difference, which might have assisted in creating partisan bubbles of discourse. If there is not a significant difference, it would suggest that they have more neutral discourse than anticipated and that the perceived partisan divide might not have extended to these newspaper opinion section.

## Preceding works
We're using [MALLET](http://mallet.cs.umass.edu/) as a topic modelling tool to find the key terms that different news organizations used in the same time period.

We also looked at the [2010 Stanford Media Bias Study](https://web.stanford.edu/~gentzkow/research/biasmeas.pdf) which used MALLET topic modelling as well as slant analysis to research how much slant different media organizations have on a Democrat-Republican scale.

We are also interested in research done on the [politicization of COVID-19 news](https://journals-sagepub-com.ezproxy.princeton.edu/doi/full/10.1177/1075547020950735) for inspiration for our project. This paper updated and utilized a dictionary of terms indicating political figures or scientific figures to analyze the prevalence of either sources in the news. This dictionary could be a helpful starting point to devise additional keywords for our analysis. All of these either have research methods, databases, or general ideas that we want to explore in our research.

In order to answer our research questions, we intend to web scrape WSJ articles with Beautiful Soup/OpenRefine and use the NYTimes archive API to acquire a dataset. After we have the data that we want, we will use MALLET topic modelling to find topics related to COVID (government intervention, protests, etc) and political discourse. Finally, we will compare key word usage in NYTimes and WSJ op-eds to each other. If we can find an appropriate dataset assigning the partisanship of keywords (or make one ourselves by strategically rating the keywords discovered) we will compare the NYTimes and WSJ op-eds to keyword usage between Democrats and Republicans.

## Methodology
### Retrieving New York Times opinion articles

The New York Times has its own API for its articles that returns a json file filled with relevant information. 

It includes: an abstract for the article, a web url, a "snippet" of the article, and various metadata such as the author's name, date published, and references to images in the text. 

The New York Times limits call rates to 10 per minute and 4000 per day. It also has a fairly slow response rate, taking roughly 10 minutes to retrieve 5000 articles.

While they make it very easy to access some data, they also make it very hard to access article text. Because they limit the call rate from IPs, it is particularly difficult to get NYTimes article text past the first paragraph.

### Scraping Wall Street Journal opinion articless

The Wall Street Journal has no publicly available API to retrieve articles. Hence, we wrote a python script using BeautifulSoup to scrape the necessary text.

To run the script, use 'python scrape-wsj.py [start YYYY] [start MM] [start DD] [end YYYY] [end MM] [end DD]' - e.g. 'python scrape-wsj.py 2020 01 01 2020 01 31' to retrieve opinion articles in January 2020 (dates inclusive).

The script returns a csv file with each article in an entry, and contain fields "Date", "Headline", "Type" (referring to the article type, see item 4 in the Choices section below), "URL" and "Text" (containing the full text of the article).

The WSJ server has an upper limit to article scraping. It is unclear how this works exactly, but in various attempts, the server has cut off connection after scraping 150 days worth of opinion articles. It is advisable to scrape at most 4 months' worth of articles in one attempt to avoid a server side interruption, which will produce no results.

Choices that were made in the scraping script:
- A script user can enter a date range in the command line to retrieve the appropriate articles. Thus, this script is rather accessible, and has re-use value for any future researchers who might be interested in using WSJ articles for research.
- The script works by accepting a date range, then generating a list of links to news articles on a given day (e.g. https://www.wsj.com/news/archive/2021/01/01 leads to a list of all news articles on January 1, 2021) and scrape all articles in a day that has an Article Type matching the list of types in the script. This means that if the archive link formatting changes, this script might not work or might require updates.
- For simplicity of coding and error handling, the script only accepts dates between 1998 and the present, even though the archive has articles from the last 4 months of 1997.
- Since the WSJ has no overarching "Opinion" type, instead the articles fall into a number of columns and newsletters, we manually went through the listed columns on the website menu, and the featured opinion authors to create a list of Article Types that would match our interest. Since we have an interest in opinion articles that have a view on current politics and social affairs, any Reviews (e.g. book or movie reviews) were excluded from this selection. The list includes the following columns: 'Commentary', 'Review & Outlook', 'Letters', 'The Americas', 'Upward Mobility', 'Political Economics', 'Free Expression', 'East is East', 'Politics & Ideas', 'Wonder Land', 'Business World', 'The Weekend Interview', 'Inside View', 'Main Street', 'Global View', 'Declarations', 'Future View', 'Notable & Quotable', 'Best of the Web'._ This list can be edited should a script user be interested in other types of articles._
- The Text in the csv file has already been lightly preprocessed to remove multiple blank spaces and replicate its most natural form, as seen on the website.

### MALLET analysis on opinion articles

