from bs4 import BeautifulSoup
import requests
import urllib3
import selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException


class SP:
    def __init__(self):
        CHROME_BIN_LOCATION = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
        CHROME_DRIVER_LOCATION = r'D:\Питон\chromedriver.exe'
        USER_DATA_DIR = r'C:\environments\selenium'
        options = selenium.webdriver.chrome.options.Options()
        service = selenium.webdriver.chrome.service.Service(CHROME_DRIVER_LOCATION)
        options.add_argument(f'user-data-dir={USER_DATA_DIR}')
        options.add_argument('--disable-popup-blocking')
        options.binary_location = CHROME_BIN_LOCATION
        self.driver = selenium.webdriver.Chrome(options=options, service=service)
        self.driver.maximize_window()


    def close(self):
        self.driver.close()

    def get_page(self, p):
        baseurl = fr'https://bus.gov.ru/registry?d-442831-p={p}&agencyTypesDropDownValue=b_c_a_types&annulment=false&pageSize=30'
        self.driver.get(baseurl)
        self.driver.execute_script('window.scroll(0,document.body.scrollHeight)')

    def get_info(self):
        for p in range(1,34):
            self.get_page(p)
            soup = BeautifulSoup(self.driver.find_element(By.XPATH, "//body").get_attribute('outerHTML'), "html.parser")
            [x.attrs['href'] for x in soup.find_all('a', {'class': 'result__title ng-star-inserted'})]
        # try:
        #     while True:
        #
        # except:
        #     pass



tmp = SP()
tmp.get_info()
#
# src = tmp.driver.find_element(By.XPATH, "//body").get_attribute('outerHTML')
# tmp.close()
# print(src)
#
#
#
#
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# class_html = []
# for p in range(1,35):
#     tmp.get_page(p)
#     soup = BeautifulSoup(tmp.driver.find_element(By.XPATH, "//body").get_attribute('outerHTML'), "html.parser")
#     class_html += [x.attrs['href'] for x in soup.find_all('a', {'class': 'result__title ng-star-inserted'})]
# print(class_html)

# p = 3
# page = requests.get(url, verify=False)
#
# soup = BeautifulSoup(src, "html.parser")
# print(soup)
#
# class_html = soup.find_all('a', {'class': 'result__title ng-star-inserted'})
# print(class_html)
# [x.attrs['href'] for x in class_html]