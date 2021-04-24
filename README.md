# Topic Modelling on Wall Street Journal and New York Times Op-Ed Articles in 2020
Final project for HUM346 - Introduction to Digital Humanities, Princeton University, Spring 2021. Exploring the New York Times and Wall Street Journal op-ed articles.

## Motivation

## Methodology
### Retrieving New York Times op-eds
    The New York Times has its own API for its articles that returns a json file filled with relevant information. It includes: an abstract for the article, a web url, a "snippet" of the article, and various metadata such as the author's name, date published, and references to images in the text. The New York Times limits call rates to 10 per minute and 4000 per day. It also has a fairly slow response rate, taking roughly 10 minutes to retrieve 5000 articles. While they make it very easy to access some data, they also make it very hard to access article text. Because they limit the call rate from IPs, it is particularly difficult to get NYTimes article text past the first paragraph.
### Scraping Wall Street Journal op-eds

