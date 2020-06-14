import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from os import path

info = {
    'url': 'https://covid19.who.int/region/amro/country/br',
    'newCasesXpath': '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/span[1]',
    'confirmedCasesXpath': '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[3]/div/span[1]',
    'deathsXpath': '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[4]/div/span[1]'
}
relativePath = path.join(path.dirname(__file__), '../../archives/')

class CovidTracker:
    def __init__(self, headless):
        self.option = Options()
        self.option.headless = True if headless else False
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', chrome_options=self.option)
    
    def getOnline(self):
        try:
            self.driver.get(info['url'])
            _ = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "root")))
        except Exception:
            raise Exception('The page did not load')

    def getOffline(self):
        self.driver.quit()

    def getInfo(self):
        newCases = self.driver.find_element_by_xpath(info['newCasesXpath']).get_attribute('innerHTML')
        confirmedCases = self.driver.find_element_by_xpath(info['confirmedCasesXpath']).get_attribute('innerHTML')
        deaths = self.driver.find_element_by_xpath(info['deathsXpath']).get_attribute('innerHTML')
        covidNumbers = {
            'newCases': newCases,
            'confirmedCases': confirmedCases,
            'deaths': deaths
        }
        return covidNumbers
    
    def handleInfos(self, infos):
        infosJson = json.dumps(infos)
        date = datetime.now()
        infosTxt = f'''
        Para o dia {date.day}/{date.month}/{date.year},
        o status de COVID-19 para o Brasil:

        Novos casos: {infos['newCases']}
        Casos Confirmados: {infos['confirmedCases']}
        Mortos: {infos['deaths']}

        '''
        with open(relativePath + 'stats.json', 'w+') as stats:
            stats.writelines(infosJson)
        with open(relativePath + 'stats.txt', 'w+') as stats:
            stats.writelines(infosTxt)

    def fetch(self):
        self.getOnline()
        self.handleInfos(self.getInfo())
        self.getOffline()
