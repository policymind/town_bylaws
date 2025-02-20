
import uuid
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation
import src.tools as tl


python_opts = CodecOptions(uuid_representation=UuidRepresentation.PYTHON_LEGACY)
# Store a legacy C#-formatted UUID


mongo_client = tl.get_mongo_client()
collection = mongo_client.TownPolicy.get_collection("by_laws_md", codec_options=python_opts) 


def parse_markdown_and_store(url_id):
    """
    Parses a Markdown file, converts it to HTML, and stores it in MongoDB.

    Args:
        markdown_file_path (str): The path to the Markdown file.
    """
    markdown_file_path = f"{url_id}.md"
    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            markdown_text = file.read()
    except FileNotFoundError:
         print(f"Error: File not found at {markdown_file_path}")
         return
    
    document = {"uuid_text":url_id,  "markdown_content": markdown_text}
    collection.insert_one(document)
    print(f"Markdown content from '{markdown_file_path}' stored in MongoDB.")

# Example usage:
# Close the connection






# #------------------------------------------------------------
# # set db as mydatabase
# mydb = client["mydatabase"]
# # create new table matownpilicy
# towntab = mydb['matownpolicy']

# # create ecode var
# towntab.update_many("bylaws_reg":{"$regex":"ecode360"}, { "$set": { "ecode" : "True" } })

# # find towns with clear pdf in url
# pdf_query = {"ecode": {"$ne" :"True"}}
# mydoc2 = towntab.find(pdf_query).to_list()

# confirmed_websites = [{'id':str(row.get('_id')), 'has_pdf': mg.confirm_pdf(row.get('bylaws_reg'))} for row in progressbar(mydoc2)]
# filtered_data = [d['id'] for d in confirmed_websites if d['has_pdf'] != 0]

# # update mongo table
# updates = []
# for id  in filtered_data:
#     updates.append(UpdateOne({'_id': ObjectId(id)}, {'$set': {'ispdf': 1}}))
# towntab.bulk_write(updates)