from bs4 import BeautifulSoup
import requests
import urllib3
import selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm


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

    def get_page(self, p, city):
        baseurl = fr'https://bus.gov.ru/registry?d-442831-p={p}&agencyTypesDropDownValue=b_c_a_types&annulment=false&city={city}&pageSize=30'
        self.driver.get(baseurl)
        self.driver.execute_script('window.scroll(0,document.body.scrollHeight)')


    def get_info(self, city):

        self.get_page(1, city)
        time.sleep(3)
        check = BeautifulSoup(self.driver.find_element(By.XPATH,"/html/body/div[2]/ui-view/ui-view-ng-upgrade/ui-view/app-registry/div[2]/div/div[1]/h3/span").get_attribute('outerHTML'), "html.parser")
        tot = check.find("span").text
        total_found = int(tot.replace('\xa0', '').strip())

        for p in range(1, (total_found//30 + 2)):

            if total_found > 1000 or total_found == 0:
                break
            if total_found % 30 == 0 and p > total_found//30:
                continue


            self.get_page(p,city)
            checking = BeautifulSoup(self.driver.find_element(By.XPATH,"/html/body/div[2]/ui-view/ui-view-ng-upgrade/ui-view/app-registry/div[2]/div/div[1]/h3/span").get_attribute('outerHTML'), "html.parser")
            what = int((checking.find("span").text).replace('\xa0', '').strip())

            if what == 0:
                break

            waiting = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/ui-view/ui-view-ng-upgrade/ui-view/app-registry/div[2]/div/div[2]/div/div[1]/div/div[1]/a[1]')))

            soup = BeautifulSoup(self.driver.find_element(By.XPATH, "//body").get_attribute('outerHTML'), "html.parser")
            with open('hrefs.txt', 'a') as file:
                file.write('\n'.join([x.attrs['href'] for x in soup.find_all('a', {'class': 'result__title ng-star-inserted'})]) + '\n')
            with open('dop_hrefs.txt', 'a') as file:
                file.write(' '.join([x.attrs['href'] for x in soup.find_all('a', {'class': 'result__title ng-star-inserted'})]))
            print([x.attrs['href'] for x in soup.find_all('a', {'class': 'result__title ng-star-inserted'})])

        with open('dop_hrefs.txt', 'a', encoding='utf-8') as file:
            file.write(' ' + city + '\n')



with open('regions.txt', 'r',encoding='utf-8') as f:
    regions = f.readlines()

regions = [x.replace('\n','').replace(' г','').strip() for x in regions ]


tmp = SP()
for i in tqdm(regions):
    tmp.get_info(i)
