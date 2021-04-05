from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import sys
import pathlib
from time import sleep
from urllib.request import urlretrieve


class InvenLostArkItemDictParser:
    def __init__(self):
        super().__init__()

        self.base_link = 'http://lostark.inven.co.kr/dataninfo/item/'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.implicitly_wait(5)
        self.driver.get(self.base_link)

    def setBattleItemTable(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        _ls = soup.select("#lostarkDb > div.lostark.db_filter > table > tbody > tr:nth-child(10) > td > a")
        
        _target = None
        for _link in _ls:
            if _link.get_text() == "배틀 아이템":
                _target = _link["href"]
                break

        # Go BattleItem Table in Inven
        _target = self.base_link + _target
        self.driver.get(_target)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        _ls = soup.select('#lostarkDb > div.lostark.db_board.db_item > table > tbody')

        
        _tdict = {
            "name":[],
            "link":[],
            "img":[]
        }

        # Get Item Name & page link
        _result = _ls[0].select("a[class='name']")
        for link in _result:
            _tdict["name"].append(link.get_text())
            _tdict["link"].append(link["href"])

        # Get Item Image link
        _img_link = _ls[0].select("a > div > img")
        for i in range(0, len(_img_link)):
            _tdict["img"].append(_img_link[i]["src"])
        
        _duplicate_num = []
        for i in range(0, len(_tdict["name"])):
            if "귀속" in _tdict["name"][i]:
                continue
            _duplicate_num.append(i)

        path = pathlib.Path("resources")
        path.mkdir(parents=True, exist_ok=True)
        (path/"battleitem").mkdir(parents=True,exist_ok=True)
        battle_path = path/"battleitem"
        (battle_path/"img").mkdir(parents=True,exist_ok=True)

        for i in _duplicate_num:
            url = _tdict["img"][i]
            urlretrieve(url, "./resources/battleitem/img/"+_tdict["name"][i]+'.png')



        

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
    loaDriver = InvenLostArkItemDictParser()
    loaDriver.setBattleItemTable()


if __name__ == "__main__":
    run()