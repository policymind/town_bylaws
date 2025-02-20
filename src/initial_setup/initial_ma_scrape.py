import json
import datetime
import src.initial_setup.scrape_ma as sc
import src.mongo as mg

WEBSITE_URL = "https://www.mass.gov/info-details/massachusetts-city-and-town-ordinances-and-by-laws"
COL_HEADERS = ['city','bylaws_reg', "zoning","other"]

ct = datetime.datetime.now()
cdate=ct.date()
######### SCRIPT

soup = sc.test_connection(WEBSITE_URL)
table_names = sc.get_table_names(soup)
table_list = soup.find_all('table')

processed_table_list = [ sc.data_cleaning(table, COL_HEADERS) for table in table_list]

table_dict = []
for item in processed_table_list:
    for city in item:
        table_dict.append(city)

# Convert the dictionary to a JSON string
json_data = json.dumps(table_dict)

file_name = f"town_data_{cdate}.json"
with open(file_name, "w") as outfile:
    outfile.write(json_data)