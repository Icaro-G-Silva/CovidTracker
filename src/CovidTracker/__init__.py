import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from os import path
import re as regex
from .Xpaths import Xpaths

if path.dirname(__file__) == 'main': relativePath = path.join(path.dirname(__file__), '../../../../archives/')
else: relativePath = path.join(path.dirname(__file__), '../../archives/')


class CovidTracker:
    def __init__(self, headless, source = 'https://www.worldometers.info/coronavirus/'):
        self.option = Options()
        self.option.headless = True if headless else False
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', chrome_options=self.option)
        self.source = source
    
    def goTo(self, newURL):
        try:
            self.driver.get(newURL)
            _ = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception:
            raise Exception('The page did not load')

    def getOffline(self):
        self.driver.quit()

    def getInfo(self):
        if regex.search('who', self.source, regex.IGNORECASE): entireObject = self.getWhoInfo()
        else: entireObject = self.getOmetersInfo()
        return entireObject
    
    def getOmetersInfo(self):
        finalObject = {}
        countriesURL = []

        totalCases = self.driver.find_element_by_xpath(Xpaths.ometersInfo['totalCasesXpath']).get_attribute('innerHTML')
        recoveredCases = self.driver.find_element_by_xpath(Xpaths.ometersInfo['recoveredCasesXpath']).get_attribute('innerHTML')
        deaths = self.driver.find_element_by_xpath(Xpaths.ometersInfo['deathsXpath']).get_attribute('innerHTML')

        mainInfos = {
            'totalCases': totalCases.strip(),
            'recoveredCases': recoveredCases.strip(),
            'deaths': deaths.strip()
        }
        finalObject.update(mainInfos)

        for countries in range(5):
            countriesURL.append(self.driver.find_element_by_xpath(Xpaths.ometersInfo[f'{countries+1}Xpath']).get_attribute('href'))

        for countries in range(5):
            self.goTo(countriesURL[countries])
            countryName = self.driver.find_element_by_xpath(Xpaths.ometersInfo['countryNameXpath']).get_attribute('innerHTML')
            countryName = countryName[121:len(countryName)].strip()
            totalCases = self.driver.find_element_by_xpath(Xpaths.ometersInfo['totalCasesXpath']).get_attribute('innerHTML')
            recoveredCases = self.driver.find_element_by_xpath(Xpaths.ometersInfo['recoveredCasesXpath']).get_attribute('innerHTML')
            deaths = self.driver.find_element_by_xpath(Xpaths.ometersInfo['deathsXpath']).get_attribute('innerHTML')
            
            unitInfos = {
                f'{countryName}CountryName': countryName,
                f'{countryName}TotalCases': totalCases.strip(),
                f'{countryName}RecoveredCases': recoveredCases.strip(),
                f'{countryName}Deaths': deaths.strip()
            }
            finalObject.update(unitInfos)
        
        return finalObject

    def getWhoInfo(self):
        countryName = self.driver.find_element_by_xpath(Xpaths.whoInfo['countryNameXpath']).get_attribute('innerHTML')
        newCases = self.driver.find_element_by_xpath(Xpaths.whoInfo['newCasesXpath']).get_attribute('innerHTML')
        confirmedCases = self.driver.find_element_by_xpath(Xpaths.whoInfo['confirmedCasesXpath']).get_attribute('innerHTML')
        deaths = self.driver.find_element_by_xpath(Xpaths.whoInfo['deathsXpath']).get_attribute('innerHTML')

        mainInfos = {
            'countryName': countryName.strip(),
            'newCases': newCases.strip(),
            'confirmedCases': confirmedCases.strip(),
            'deaths': deaths.strip()
        }

        return mainInfos
    
    def generateText(self, countryInfo, standard = True):
        dividedInfo = []
        counter = 0
        date = datetime.now()
        if standard:
            infosTxt = f'Para o dia {date.day}/{date.month}/{date.year},\n\no status de COVID-19 para: Mundo\n\nCasos Totais: {countryInfo["totalCases"]}\nCasos Recuperados: {countryInfo["recoveredCases"]}\nMortos: {countryInfo["deaths"]}'
            countryInfo.pop('totalCases')
            countryInfo.pop('recoveredCases')
            countryInfo.pop('deaths')
            for item in countryInfo.values():
                dividedInfo.append(item)
                counter += 1
                if counter >= 4:
                    infosTxt += f'\n\n\nO status de COVID-19 para: {dividedInfo[0]}\n\nCasos Totais: {dividedInfo[1]}\nCasos Recuperados: {dividedInfo[2]}\nMortos: {dividedInfo[3]}'
                    counter = 0
                    dividedInfo.clear()
        else:
            for item in countryInfo.values(): dividedInfo.append(item)
            infosTxt = f'Para o dia {date.day}/{date.month}/{date.year},\n\no status de COVID-19 para: {dividedInfo[0]}\n\nNovos Casos: {dividedInfo[1]}\nCasos Confirmados: {dividedInfo[2]}\nMortos: {dividedInfo[3]}'
        return infosTxt

    def handleInfos(self, infos):
        infosJson = json.dumps(infos)
        if regex.search('who', self.source, regex.IGNORECASE):
            text = self.generateText(infos, standard = False)
            with open(relativePath + f'{infos["countryName"]}Stats.json', 'w+') as stats:
                stats.writelines(infosJson)
            with open(relativePath + f'{infos["countryName"]}Stats.txt', 'w+') as stats:
                stats.writelines(text)
        else:
            text = self.generateText(infos)
            with open(relativePath + 'GeneralStats.json', 'w+') as stats:
                stats.writelines(infosJson)
            with open(relativePath + 'GeneralStats.txt', 'w+') as stats:
                stats.writelines(text)

    def fetch(self):
        self.goTo(self.source)
        self.handleInfos(self.getInfo())
        self.getOffline()
