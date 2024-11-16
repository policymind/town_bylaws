import json
import datetime
import boto3
from progressbar import progressbar

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateOne
from bson.objectid import ObjectId
import keyring

import src.scrape as sc
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


# Create an S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'matownbylaws'
object_key = f'ma_town_list/{file_name}'

# Upload the JSON data to S3
response = s3.upload_file(file_name, BUCKET_NAME, object_key)

# Create a new client and connect to the server
client = MongoClient(keyring.get_password('mongodb', 'cluster0'), server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# set db as mydatabase
mydb = client["mydatabase"]
# create new table matownpilicy
towntab = mydb['matownpolicy']

# create ecode var
towntab.update_many( "bylaws_reg":{"$regex":"ecode360"}}, { "$set": { "ecode" : "True" } }) 

# find towns with clear pdf in url
pdf_query = {"ecode": {"$ne" :"True"}}
mydoc2 = towntab.find(pdf_query).to_list()

confirmed_websites = [{'id':str(row.get('_id')), 'has_pdf': mg.confirm_pdf(row.get('bylaws_reg'))} for row in progressbar(mydoc2)]
filtered_data = [d['id'] for d in confirmed_websites if d['has_pdf'] != 0]

# update mongo table
updates = []
for id  in filtered_data:
    updates.append(UpdateOne({'_id': ObjectId(id)}, {'$set': {'ispdf': 1}}))
towntab.bulk_write(updates)