import pandas as pd
import sys
import logging
import bs4 
import requests as req

WEBSITE_URL = "https://www.mass.gov/info-details/massachusetts-city-and-town-ordinances-and-by-laws"


logger = logging.getLogger(__name__)

def test_connection(url):
    """
    input: url for scraping
    output: html text if website status is good, else, error
    """

    req = req.get(url)
    req.status_code
    if req.status_code != 200:
        logger.error('Website status code!=200. Exit program.')
        sys.exit()
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    logger.info ("html parsed")
    return soup



# get first table from page
table = soup.find_all('table')[0]
rows = table.find_all('tr')

# how many rows are in the first table
len(rows)

# get header column
header = rows[0].find_all('th')

# get header names
titles = []
for i in range(0,len(header)) :
   titles.append(header[i].text.strip())

titles

tables = soup.find_all('table')


def handle_nulls(x):
    """extracts the href from a cell while maintaining the blanks if an href is not there"""
    if x.text.strip() != '':
        return x.find("a").get('href')
    return ""


def process_table(table_sample):
    """
    input: the table from beautiful soup
    output: data in list form
    """
    rows = table.find_all('tr')
    town_data =[]
    for row in rows[1:]:
        content = []
        city = row.find('th').text.strip()
        print(city)
        content.append(city)
        cells = row.find_all('td')
        len(cells)
        for iter in range(len(cells)) :
            content.append(handle_nulls(cells[iter]))
        town_data.append(content)
    return town_data
    





