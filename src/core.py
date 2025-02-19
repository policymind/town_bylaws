import json
import datetime
import boto3
from progressbar import progressbar

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateOne
from bson.objectid import ObjectId
import keyring

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

############################################

import urllib.request

url_sample = "https://www.townofchesterfieldma.com/sites/g/files/vyhlif7606/f/uploads/general_town_by-laws_2022.pdf"
mg.confirm_pdf(url_sample)

download_path = f"sample_pdfs/policy_file.pdf"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}



req = urllib.request.Request(url_sample, headers=HEADERS)
with urllib.request.urlopen(req) as response, open(download_path, "wb") as f:
    f.write(response.read())

import json
from pathlib import Path
from docling.document_converter import DocumentConverter
import pandas as pd
converter = DocumentConverter()


result = converter.convert(download_path)

result_dict = result.document.export_to_dict()
print(json.dumps(result_dict, indent=2))
output_dir = Path("")

doc_filename = result.input.file.stem
print(f"Document filename: {doc_filename}")
# Iterate over tables in the document and save them as CSV and HTML formats.
for table_idx, table in enumerate(result.document.tables):
  table_df: pd.DataFrame = table.export_to_dataframe()
  print(f"$$ Table {table_idx}")
  # Save as CSV
  table_df.to_csv(f"{doc_filename}-table-{table_idx}.csv")
  # Save as HTML
  html_filename = output_dir / f"{doc_filename}-table-{table_idx+1}.html"
  with html_filename.open("w") as fp:
    fp.write(table.export_to_html())

result_dict.keys()
result_dict['body']['children'][25]

json_data = json.dumps(result_dict, indent=2)

file_name = f"policy_json.json"
with open(file_name, "w") as outfile:
    outfile.write(json_data)


import pymupdf4llm
download_path = f"sample_pdfs/belmontpage3.pdf"
doc = pymupdf4llm.to_markdown(download_path)
from pathlib import Path
Path("belmontpage3.md").write_bytes(doc.encode())
print(doc)

import pymupdf 
with pymupdf.open(download_path) as doc:  # open document
    text = chr(12).join([page.get_text() for page in doc])
# write as a binary file to support non-ASCII characters
Path(download_path + ".txt").write_bytes(text.encode())



from PyPDF2 import PdfReader, PdfWriter

def convert_to_regular_pdf(input_path, output_path):
    """
    Converts an Adobe PDF to a regular PDF by flattening it.

    Args:
        input_path (str): Path to the input Adobe PDF file.
        output_path (str): Path to save the converted regular PDF file.
    """
    try:
        with open(input_path, 'rb') as input_file:
            reader = PdfReader(input_file)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        print(f"Successfully converted '{input_path}' to '{output_path}'")
    
    except FileNotFoundError:
         print(f"Error: Input file '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_pdf_path = 'sample_pdfs/Town of Belmont, MA.pdf'  # Replace with your input PDF path
    output_pdf_path = 'sample_pdfs/reformated_belmont.pdf'  # Replace with your desired output path
    convert_to_regular_pdf(input_pdf_path, output_pdf_path)

import pytesseract
from pdf2image import convert_from_path

# convert to image using resolution 600 dpi 
pages = convert_from_path("sample_pdfs/chestfieldpage3.pdf", 600)

# extract text
text_data = ''
for page in pages:
    text = pytesseract.image_to_string(page)
    text_data += text + '\n'
print(text_data)


# ---------------------------------------------------------------------------------

import os
import base64
import pytesseract
from pdf2image import convert_from_path
from bs4 import BeautifulSoup

# Function to convert PDF to images
def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path, fmt='tiff')

# Function to convert image to hOCR using pytesseract
def image_to_hocr(image):
    return pytesseract.image_to_pdf_or_hocr(image, extension='hocr')

# Function to convert hOCR to markdown
def hocr_to_markdown(hocr):
    soup = BeautifulSoup(hocr, 'html.parser')
    markdown_text = ""

    for line in soup.find_all('span', class_='ocr_line'):
        line_text = " ".join([word.get_text() for word in line.find_all('span', class_='ocrx_word')])
        markdown_text += f"{line_text}\n"

    return markdown_text

# Main function to convert PDF to Markdown
def pdf_to_markdown(pdf_path):
    images = pdf_to_images(pdf_path)
    markdown_text = ""

    for image in images:
        hocr = image_to_hocr(image)
        markdown_text += hocr_to_markdown(hocr) + "\n\n"

    return markdown_text

# Example usage
if __name__ == "__main__":
    pdf_path = "sample_pdfs/policy_file.pdf"  # Path to your PDF file
    markdown_output = pdf_to_markdown(pdf_path)
    with open("output.md", "w") as file:
        file.write(markdown_output)



###### --------------------------------------

class policy_processor():
    def __init__(self, url_type):
        self.url_type = url_type
        pass


with open(file_path, 'r') as file:
    file_content = file.read()
    data = json.loads(file_content)