"""functions that orchestrate the doc coversion """

import sys
from urllib.parse import urlparse
import urllib.request
from pathlib import Path
import requests
import boto3
from bs4 import BeautifulSoup
import pymupdf4llm

from markdownify import markdownify
import postgres_functions as pf


# Create an S3 client

BUCKET_NAME = 'matownbylaws'
RAW_UPLOAD_DIR = "policy_raw"
MARKDOWN_UPLOAD_DIR = "markdown_dir"
EXT_DICT = {'pdf':'pdf', 'ecode':'html', 'municode':'html'}
header_str_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                   "AppleWebKit/537.36 (KHTML, like Gecko)",
                   "Chrome/58.0.3029.110 Safari/537.36"]
HEADERS = {"User-Agent":
           " ".join(header_str_list)}


s3 = boto3.client('s3')
my_bucket = s3.Bucket(BUCKET_NAME)

### Upload to s3 

def raw_s3_upload(url_id, url_type):
    """grab raw downloaded file and uploads it to s3 bucket for raw files"""
    file_name = f"{url_id}.{EXT_DICT[url_type]}"
    object_key = f'{RAW_UPLOAD_DIR}/{file_name}'
    response = s3.upload_file(file_name, BUCKET_NAME, object_key)
    return response

def markdown_s3_upload(url_id):
    """uploads converted markdown file to markdown s3 bucket"""
    file_name = f"{url_id}.md"
    object_key = f'{MARKDOWN_UPLOAD_DIR}/{file_name}'
    response = s3.upload_file(file_name, BUCKET_NAME, object_key)
    return response

## Download s3 file

def get_s3_files(sub_dir):
    """ gets list of files from target folder"""
    oid_list = []
    for objects in my_bucket.objects.filter(Prefix=f"{sub_dir}"):
        oid_list.append(objects.key)
    return oid_list

def get_file(uuid_file):
    """ downloads specific file to local"""
    with open('FILE_NAME', 'wb') as f:
        s3.download_fileobj(BUCKET_NAME, uuid_file, f)

# confirm link is to pdf
def confirm_pdf(link):
    "to test if link is actually to pdf file"
    if link != "" :
        if link.rsplit(".",1)[1] == "pdf":
            return 1
        elif 'Content-Type' in dict(requests.head(link,headers=HEADERS).headers).keys():
            if  dict(requests.head(link,headers=HEADERS).headers)['Content-Type'] == 'application/pdf':
                return 1
    return 0

#  pdf parse
def fetch_pdf_file(policy_id, policy_url):
    """ download pdf"""
    download_path = f"{policy_id}.pdf"
    req = urllib.request.Request(policy_url, headers=HEADERS)
    with urllib.request.urlopen(req) as response, open(download_path, "wb") as f:
        f.write(response.read())

# ecode files
def fetch_ecode_file(policy_id, policy_url):
    """get policy from ecode360 link """
    # Extract last part of url string
    parsed_url = urlparse(policy_url)
    html_ecode_link = f"https://ecode360.com/output/word_html{parsed_url.path}"

    req = requests.get(html_ecode_link, timeout=10)
    if req.status_code != 200:
        sys.exit()
    results = BeautifulSoup(req.text, 'html.parser')

    html_filename =  f"{policy_id}.html"
    with html_filename.open("w") as fp:
        fp.write(results)


## convert to markdown functions
def convert_html_markdown(url_id):
    """ convert html file to markdown doc"""
    file_path = f"{url_id}.html"
    with file_path.open('r') as fp:
        results = fp.read()
    doc = markdownify(results, heading_style="ATX")
    Path(f"{url_id}.md").write_bytes(doc.encode())

def convert_pdf_markdown(url_id, url_type):
    """ converts raw download file into markdown"""
    download_path = f"{url_id}.pdf"
    doc = pymupdf4llm.to_markdown(download_path)
    Path(f"{url_id}.md").write_bytes(doc.encode())

