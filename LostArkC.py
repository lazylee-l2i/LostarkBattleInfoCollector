from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import sys
import pathlib
from time import sleep

class LostArkItemDictParser:
    def __init__(self):
        super().__init__()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.implicitly_wait(5)
        self.driver.get('https://lostark.game.onstove.com/ItemDictionary')

    def getPotionInfo(self):
        self.driver.find_element_by_name('itemdic-name').send_keys('회복약')
        self.driver.find_element_by_xpath('//div[@class="form"]/div[@class="bt"]/span[@class="submit"]/button[@type="submit"]').click()
        sleep(1)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        _ls = soup.select('#lostark-wrapper > div > main > div > div > div > div.itemdic-contents > div.list > div > ul > li')

        sleep(3)
        for n in _ls:
            _msg = n.text.strip().split("\n")
            print(_msg)


    def getLifeContentsItems(self):
        element = self.driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div/div/div[1]/form/fieldset/div[2]/div[1]/label[11]/input')
        self.driver.execute_script("arguments[0].click();", element)
        sleep(2)
        element = self.driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div/div/div[1]/form/fieldset/div[2]/div[2]/label[2]/input')
        self.driver.execute_script("arguments[0].click();", element)
        sleep(2)


        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        _ls = soup.select('#lostark-wrapper > div > main > div > div > div > div.itemdic-contents > div.list > div > ul > li')

        for n in _ls:
            _msg = n.text.strip().split("\n")
            print(_msg[0])


def run():
    loaDriver = LostArkItemDictParser()
    loaDriver.getLifeContentsItems()


if __name__ == "__main__":
    #run()
    path = pathlib.Path(".resources/life_contents")
    path.mkdir(parents=True, exist_ok=True)
