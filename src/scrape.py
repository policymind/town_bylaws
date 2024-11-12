import sys
import logging
import bs4 
import requests
import json
import datetime

WEBSITE_URL = "https://www.mass.gov/info-details/massachusetts-city-and-town-ordinances-and-by-laws"

logger = logging.getLogger(__name__)

ct = datetime.datetime.now()
cdate=ct.date()



def test_connection(url):
    """
    input: url for scraping
    output: html text if website status is good, else, error
    """

    req = requests.get(url)
    req.status_code
    if req.status_code != 200:
        logger.error('Website status code!=200. Exit program.')
        sys.exit()
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    logger.info ("html parsed")
    return soup


def get_table_names(soup):
    """ Not every letter of the alphabet has its own table
    this allows the data to be grabbed dynamicaly """
    heading = soup.find_all('h3') 
    table_names = [x.text.strip() for x in heading if len(x.text.strip()) <4]
    num_tables = len(table_names)
    logger.info("%s tables found", str(num_tables))
    return table_names

def get_column_headers(soup):
    """ get column headers for first table"""
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    header = rows[0].find_all('th')
    col_headers = []
    for i in range(0,len(header)) :
        col_headers.append(header[i].text.strip())
    return col_headers

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
    rows = table_sample.find_all('tr')
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

def convert_to_dict(table_sample, col_headers):
    city_data = {row_val[0] : {x:y for x,y in zip(col_headers[1:], row_val[1:])} for row_val in table_sample}   
    return city_data

def data_cleaning(table, col_headers):
    scraped_data = process_table(table)
    town_dict = convert_to_dict(scraped_data, col_headers)
    return town_dict

######### SCRIPT

soup = test_connection(WEBSITE_URL)
table_names = get_table_names(soup)
col_headers = get_column_headers(soup)

table_list = soup.find_all('table')

table_data = {}
if len(table_list) == len(table_names):
    table_data = {section:data_cleaning(table) for section,table in zip(table_names,table_list)}

# Convert and write JSON object to file
with open(f"MA_BYLAWS_{cdate}.json", "w") as outfile:
    json.dump(table_data, outfile)

