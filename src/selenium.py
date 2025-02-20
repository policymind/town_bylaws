from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--enable-javascript")

# Initialize Chrome driver with the options
browser = webdriver.Chrome(options=chrome_options)

# initialize an instance of the chrome driver (browser)
# driver = webdriver.Chrome()

target_url = "https://library.municode.com/ma/holyoke/codes/code_of_ordinances"
general = "https://library.municode.com/ma/holyoke"
malden_redirect = "https://library.municode.com/ma/malden/code/code_of_ordiances"
hosted_url = "https://malden.municipalcodeonline.com/"


# visit your target site
browser.get(malden_redirect)
# print(browser.current_url)
# browser.quit()

try:
    element = WebDriverWait(browser, 10).until(
        EC.url_changes(malden_redirect)
    )
finally:
    file_path = "municode_sample.html"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(browser.page_source)
    browser.quit()



# output the full-page HTML
# print(driver.page_source)
file_path = "municode_sample.html"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(driver.page_source)

print(f"HTML file saved to {file_path}")
# release the resources allocated by Selenium and shut down the browser
driver.quit()



<a title="Code of Ordinances" ng-href="https://library.municode.com/ma/holyoke/codes/code_of_ordinances?nodeId=10999" href="https://library.municode.com/ma/holyoke/codes/code_of_ordinances?nodeId=10999">





from selenium import webdriver
driver = webdriver.Remote(
  desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
driver.get(malden_redirect)
file_path = "municode_sample.html"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(driver.page_source)
driver.quit()


from selenium import webdriver
driver = webdriver.Chrome (executable_path="C:\chromedriver.exe")
driver.maximize_window()
driver.get("https://www.google.com/")
# identify elements with tagname <a>
lnks=driver.find_elements_by_tag_name("a")
# traverse list
for lnk in lnks:
   # get_attribute() to get all href
   print(lnk.get_attribute(href))
driver.quit()