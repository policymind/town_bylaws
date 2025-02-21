""" 
MUNICODE is an ordinance hosting platform for local governments. 
In an ideal world we'd call an API to get the policy content, but here we are.

Instead, we take advantage of the fact that municode sites have the same base structrue

STEPS:
 - scrape town ordinances site with selenium
 - query the results with java to get the lefthand table of contents
 - extract all links from table of contents
 - loop over those links to scrape each of those pages
 - extract code content from each page
 - use html cleaner to get only the necessary content
"""
from pathlib import Path
from lxml_html_clean import Cleaner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from markdownify import markdownify

from bs4 import BeautifulSoup
from time import sleep

java_queries= {'text':
               'return document.querySelector("#codesContent > div.codes-chunks-pg > ul").innerHTML',
               'nested_toc':
               'return document.querySelector("#codesContent > div.small-padding > div.codes-toc > ul").innerHTML'
               }

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

town_site = "https://library.municode.com/ma/winthrop"


def convert_municode_link(town_site):
    if town_site.split('/')[-1] != "code_of_ordinances":
        updated_link = f"{town_site}/codes/code_of_ordinances"
        return updated_link
    return town_site

def get_toc_links(test):
    trial = test.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    print(trial)
    a_items = test.find_elements(By.CSS_SELECTOR, 'a')
    print('5')
    TOC_links = [x.get_attribute('href') for x in a_items]
    print('6')
    TOC_nodes = [x.split('=')[-1] for x in TOC_links]
    return TOC_nodes

def clean_html_div(html_soup):
    for object in html_soup.find_all('div', class_ = 'mcc_codes_content_action_bar'):
        object.decompose()
    return html_soup

def content_query(driver):
    java_query = 'return document.querySelector("#codesContent > div.codes-chunks-pg > ul").innerHTML'
    policy_content = driver.execute_script(java_query)
    return policy_content


def got_node_content(town_site, node_id, driver):
    town_site = town_site
    node_link = f"{town_site}?nodeId={node_id}"
    driver.get(node_link)
    driver.fullscreen_window()
    policy_content = content_query(driver)
    cleaner = Cleaner(page_structure=False, links=False, javascript=False )
    html = cleaner.clean_html(policy_content)
    soup = BeautifulSoup(html, 'html.parser')

    with open(f"html_downloads/{node_id}.html", "w") as file:
        file.write(str(soup))

confirmed_link = convert_municode_link(town_site)

driver = webdriver.Chrome(options=options)
driver.get(confirmed_link)
driver.fullscreen_window()
test = driver.execute_script('return document.querySelector("#genTocList")')
a_items = test.find_elements(By.CSS_SELECTOR, 'a')
returns = test.find_elements(By.CSS_SELECTOR, 'a')
TOC_links = [x.get_attribute('href') for x in a_items]
TOC_nodes = [x.split('=')[-1] for x in TOC_links]



#first part
driver = webdriver.Chrome(options=options)
confirmed_link = convert_municode_link(town_site)
driver.get(confirmed_link)
driver.fullscreen_window()
test = driver.execute_script('return document.querySelector("#genTocList")')
driver.quit()
#second part
TOC_list = get_toc_links(test)
nested_toc = []
# handle straight forward text grabs first
for node in TOC_list:
    print(node)
    driver = webdriver.Chrome(options=options)
    try:
        got_node_content(confirmed_link, node, driver)
        driver.quit()
        sleep(2)
    except JavascriptException as e:
        print(f"Error processing {node}: {e}")
        nested_toc.append(node)
    continue

print(nested_toc)
len(TOC_list)


#testing finding the table of contents on a page
driver = webdriver.Chrome(options=options)
driver.get('https://library.municode.com/ma/winthrop/codes/code_of_ordinances?nodeId=TIT12STSIPUPL')
driver.fullscreen_window()
second_content_path = 'document.querySelector("#codesContent > div.codes-chunks-pg > ul")'
test = driver.execute_script('return document.querySelector("#codesContent > div.small-padding > div.codes-toc")')

# find links for toc level 2
check = test.find_elements(By.CSS_SELECTOR, "li[nodedepth='2']")
sub_toc_list = [item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href').split("=")[1] for item in check]
driver.quit()


sub_nested_toc = []
# handle straight forward text grabs first
for node in sub_toc_list:
    print(node)
    driver = webdriver.Chrome(options=options)
    try:
        got_node_content(confirmed_link, node, driver)
        driver.quit()
        sleep(2)
    except JavascriptException as e:
        print(f"Error processing {node}: {e}")
        sub_nested_toc.append(node)
        driver.quit()
    continue


print(sub_nested_toc)

url = 'https://library.municode.com/ma/winthrop/codes/code_of_ordinances?nodeId=TIT12STSIPUPL_CH12.28TOLA'
driver = webdriver.Chrome(options=options)
driver.get(url)
driver.fullscreen_window()
second_content_path = 'return document.querySelector("#main-content")'
test = driver.execute_script(second_content_path)

test.get_attribute("innerHTML")

cleaner = Cleaner(page_structure=False, links=False, javascript=False )
html = cleaner.clean_html(test.get_attribute("innerHTML"))

soup = BeautifulSoup(html, 'html.parser')

with open(f"html_downloads/TIT12STSIPUPL_CH12.28TOLA", "w") as file:
    file.write(str(soup))

markdown_doc = markdownify(str(soup), heading_style="ATX")
Path("html_downloads/TIT12STSIPUPL_CH12.28TOLA.md").write_bytes(markdown_doc.encode())

