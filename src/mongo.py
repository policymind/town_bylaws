from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateOne
from bson.objectid import ObjectId
import src.tools as tl

mongo_client = tl.get_mongo_client()

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
towntab.update_many("bylaws_reg":{"$regex":"ecode360"}, { "$set": { "ecode" : "True" } })

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