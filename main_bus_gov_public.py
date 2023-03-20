import json
import re
import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


class BG:
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

    def get_page(self, inn):
        baseurl = fr'https://bus.gov.ru/public/register/search.html?pageSize=30&agency={inn}&city=&tofkName=&tofkCode=&authority=&level=&agencyTypesDropDownValue=b_c_a_types&status=&annulment=false'
        self.driver.get(baseurl)
        self.driver.execute_script('window.scroll(0,document.body.scrollHeight)')

    def get_info(self, inn):

        self.get_page(inn)

        check = BeautifulSoup(self.driver.find_element(By.XPATH,
                                                       "/html/body/div[3]/div/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td[2]/form/div[3]/span").get_attribute(
            'outerHTML'), "html.parser")
        tot = check.find("span").text
        total_found = int(tot.replace('Найдено: ', '').strip())
        if total_found == 0:
            return 0

        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                            '/html/body/div[3]/div/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr/td[2]/form/div[4]/table/tbody/tr/td[2]/div[1]/a')))
        soup = str(BeautifulSoup(self.driver.find_element(By.CSS_SELECTOR,
                                                          "#agency > tbody > tr > td:nth-child(2) > div.result-element > a").get_attribute(
            'outerHTML'), "html.parser"))

        match = re.search(r'agency=(\d+)', soup)
        if match:
            number = match.group(1)
            with open('agency_after_inn.txt', 'a') as file: #создается файл с agegy, c которым работает код в agency_api
                file.write(number + '\n')
            with open('agency_and_inn.txt', 'a') as file: #создается файл для проверки, в котором пишется inn и его agency
                file.write('agency:' + number + ' inn:' + inn + '\n')


if __name__ == '__main__':
    with open('data.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
    inns = [txt['inn'] for txt in text]
    tmp = BG()
    for i in tqdm(inns):
        tmp.get_info(i)
