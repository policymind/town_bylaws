""" functions for scraping the MA GOV town bylaws"""
import sys
import logging
import datetime
import bs4
import requests


WEBSITE_URL = "https://www.mass.gov/info-details/massachusetts-city-and-town-ordinances-and-by-laws"
COL_HEADERS = ['city','bylaws_reg', "zoning","other"]

logger = logging.getLogger(__name__)

ct = datetime.datetime.now()
cdate=ct.date()

def test_connection(url):
    """
    input: url for scraping
    output: html text if website status is good, else, error
    """

    req = requests.get(url, timeout=10)
    if req.status_code != 200:
        logger.error('Website status code!=200. Exit program.')
        sys.exit()
    results = bs4.BeautifulSoup(req.text, 'html.parser')
    logger.info ("html parsed")
    return results


def get_table_names(results):
    """ Not every letter of the alphabet has its own table
    this allows the data to be grabbed dynamicaly """
    heading = results.find_all('h3')
    table_vars = [x.text.strip() for x in heading if len(x.text.strip()) <4]
    num_tables = len(table_vars)
    logger.info("%s tables found", str(num_tables))
    return table_vars

def get_column_headers(results):
    """ get column headers for first table"""
    table = results.find_all('table')[0]
    rows = table.find_all('tr')
    header = rows[0].find_all('th')
    col_vars = []
    for index, value in enumerate(header) :
        col_vars.append(value.text.strip())
    return col_vars

def handle_nulls(x):
    """extracts the href from a cell while maintaining the blanks if an href is not there"""
    if x.text.strip() != '':
        contents = x.find_all('a', href=True)
        if len(contents) > 1:
            url_link = ";".join([item['href'] for item in contents])
        else:
            url_link = contents[0]['href']
        return url_link
    return ""

def process_table(table_sample):
    """
    input: the table from beautiful soup
    output: data in list form
    """
    rows = table_sample.find_all('tr')
    town_data =[]
    for row in rows[1:]:
        content = []
        city = row.find('th').text.strip()
        print(city)
        content.append(city)
        cells = row.find_all('td')

        for index, value in enumerate(cells):
            content.append(handle_nulls(cells[index]))
        town_data.append(content)
    return town_data

def convert_to_dict(table_sample, cols_vars):
    """restructure output into dictionry for nesting"""
    city_data = [{x:y for x,y in zip(cols_vars, row_val)} for row_val in table_sample]
    return city_data

def data_cleaning(table, cols_vars):
    """ combining previous functions into one"""
    scraped_data = process_table(table)
    town_dict = convert_to_dict(scraped_data, cols_vars)
    return town_dict
