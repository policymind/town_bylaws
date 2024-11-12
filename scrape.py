import pandas as pd
import bs4 
import requests as req

WEBSITE_URL = "https://www.mass.gov/info-details/massachusetts-city-and-town-ordinances-and-by-laws"

req = req.get(WEBSITE_URL)
req.status_code
soup = bs4.BeautifulSoup(req.text, 'html.parser')

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

def handle_nulls(x):
    if x is not None:
        return x.text.strip()
    return ""

town_data =[]
for row in rows[2:]:
    content = []
    cells = row.find_all('td')
    for iter in range(0,3,1) :
        content.append(handle_nulls(cells[iter]))
    town_data.append(content)
    

        city = cells.text.strip()
    bylaws = cells[1].text.strip()
    zoning = cells[2].text.strip()
    other = cells[3].text.strip()
    print(city, bylaws, zoning, other)
