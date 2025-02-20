from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
# add headless Chrome option
options.add_argument("--headless=new")
# set up Chrome in headless mode
driver = webdriver.Chrome(options=options)


driver.maximize_window()
driver.get("https://library.municode.com/ma")
# identify elements with tagname <a>
lnks=driver.find_elements(By.CSS_SELECTOR, 'a')
# traverse list
hrefs =[]
text_desc =[]
for lnk in lnks:
   # get_attribute() to get all href
   text_desc.append(lnk.text)
   hrefs.append(lnk.get_attribute('href'))

len(hrefs)
hrefs[:-10]
[x for x in hrefs if '/ma/' in x.lower()]

driver.quit()


"""
<li ng-repeat="node in toc.topLevelNodes track by node.Id" id="genToc_TOWN_WINTHROPMUCO" data-ng-include="'mccGenTocNodeTemplate'" data-ng-class="{'active': toc.isActive(node)}" depth="0">
        <span id="genTocAnchor_TOWN_WINTHROPMUCO" class="anchor-offset"></span>
        <!----><button ng-if="::node.HasChildren" ng-click="toc.toggleShowChildrenClick($event, node)" class="toc-item-expand btn btn-flat" aria-controls="children_of_TOWN_WINTHROPMUCO" aria-expanded="false">
            <span><span class="visually-hidden">Expand TOWN OF WINTHROP - MUNICIPAL CODE</span>
            <i class="fa-fw fa fa-chevron-right" ng-class="{'fa fa-chevron-right': !node.isExpanded, 'fa fa-chevron-down': node.isExpanded}"></i></span>
        </button><!---->
        <a href="https://library.municode.com/ma/winthrop/codes/code_of_ordinances?nodeId=TOWN_WINTHROPMUCO" data-ng-href="https://library.municode.com/ma/winthrop/codes/code_of_ordinances?nodeId=TOWN_WINTHROPMUCO" class="toc-item-heading" ng-click="toc.setNavOrigin()">
            <span data-ng-bind="::node.Heading" data-ng-class="{'folderRoot' : node.Children.length}">TOWN OF WINTHROP - MUNICIPAL CODE</span>
            <!---->
            <!---->
            <!---->
            <!---->
            <!---->
            <!---->
            <!---->
            <!---->
        </a>
            <!---->
    </li>
"""