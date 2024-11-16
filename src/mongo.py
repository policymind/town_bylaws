import requests
import urllib.request

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

def confirm_pdf(link):
    if link != "" :
        if link.rsplit(".",1)[1] == "pdf":
            return 1
        elif 'Content-Type' in dict(requests.head(link,headers=HEADERS).headers).keys():
            if  dict(requests.head(link,headers=HEADERS).headers)['Content-Type'] == 'application/pdf':
                return 1
    return 0


def fetch_pdf_links(dict_row, dict_results):
    city = dict_row.get('city')
    bylaw_link = dict_row.get('bylaws_reg')
    print(bylaw_link)
    file_name = bylaw_link.rsplit('/',1)[1]
    download_path = f"downloads/{city}_{file_name}"

    url = bylaw_link
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as response, open(download_path, "wb") as f:
        f.write(response.read())
    dict_results.update({city,download_path})

def download_pdfs(mongo_db_query_results):
    town_downloads = {}
    for x in mongo_db_query_results:
        fetch_pdf_links(x,town_downloads)
    return town_downloads

def confirm_pdf(link):
    if link != "" :
        if link.rsplit(".",1)[1] == "pdf":
            return 1
        elif 'Content-Type' in dict(requests.head(link,headers=HEADERS).headers).keys():
            if  dict(requests.head(link,headers=HEADERS).headers)['Content-Type'] == 'application/pdf':
                return 1
    return 0