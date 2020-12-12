import json
import time
from selenium import webdriver
import chromedriver_binary
import configparser
import os
import errno
from datetime import datetime,timedelta
import json

from .utils import *

class RakutenEnergyCrawler():
    def __init__(self):
        self.energy_list = list()
        self.__load_config()
        self.__init_driver() 
        try:
            self.__login()
            self.__jump_to_top()
        except:
            self.__driver.quit()
    
    def __load_config(self):
        config_ini = configparser.ConfigParser()
        config_ini_path = 'config.ini'

        if not os.path.exists(config_ini_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
        
        config_ini.read(config_ini_path, encoding='utf-8')

        # iniの値取得
        self.__config = config_ini['RAKUTEN_ENERGY']
    
    def __init_driver(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--lang=' + self.__config['LANG'])
        option.add_argument('--headless')
        self.__driver = webdriver.Chrome(options=option)
    
    def __login(self):
        self.__driver.get(self.__config['LOGINURL'])
        id = self.__driver.find_element_by_id("loginInner_u")
        id.send_keys(self.__config['USER'])
        password = self.__driver.find_element_by_id("loginInner_p")
        password.send_keys(self.__config['PASSWORD'])

        time.sleep(1)

        # ログインボタンをクリック
        login_button = self.__driver.find_element_by_name("submit")
        login_button.click()

        time.sleep(3)
    
    def __jump_to_top(self):
        self.__driver.find_element_by_link_text("施設トップ").click()
        time.sleep(2)
    
    def __jump_previous_day(self):
        prev_button = self.__driver.find_element_by_xpath("//button[span[contains(text(),'前日')]]")
        prev_button.click()
        time.sleep(1)

    def __jump_post_day(self):
        post_button = self.__driver.find_element_by_xpath("//button[span[contains(text(),'翌日')]]")
        post_button.click()
        time.sleep(1)


    def __set_yaxis_params(self):
        map = {"x": [], "y":[]}
        for i in range(2,6):
            xpath = "//*[name()='svg']//*[name()='g' and contains(@class,'highcharts-yaxis-labels')]/*[name()='text']["+str(i) +"]"
            axis_data = self.__driver.find_element_by_xpath(xpath)
            height = int(axis_data.get_attribute('y'))
            kwh = float(axis_data.get_attribute('innerHTML').replace("kWh",""))
            map["x"].append(height)
            map["y"].append(kwh)
        self.__yaxis_params = least_square(map)
    
    def __set_energy_list(self):
        a,b = self.__yaxis_params

        #for i in range(1,49):
        xpath = "//*[name()='g' and @class='highcharts-series-group']/*[name()='g' and contains(@class,'highcharts-series-0')]/*[name()='rect']"
        rects = self.__driver.find_elements_by_xpath(xpath)
        for rect in rects:
            self.energy_list.append(round(round(a,3) * int(rect.get_attribute("height")) * -1.0,2))
        
        
    
    def __set_timestamps(self):
        xpath = "//span[@class='date ng-scope ng-binding']"
        date_element = self.__driver.find_element_by_xpath(xpath)
        date_str = date_element.text.split("（")[0]
        start = datetime.strptime(date_str,"%Y年%m月%d日")
        delta = timedelta(minutes=30)

        self.timestamps = list(map(lambda x: int((start + delta * x).timestamp()),range(len(self.energy_list))))

    def __create_json(self):
        obj = []
        for i in range(len(self.energy_list)):
            energy = self.energy_list[i]
            if (energy > 0.0):
                obj.append({
                    "timestamp": self.timestamps[i],
                    "energy": energy
                 }) 
        
        return json.dumps(obj)
    
    def get_json(self,day=1):
        for i in range(abs(day)):
            self.__jump_previous_day()

        self.__set_yaxis_params()
        self.__set_energy_list()
        self.__set_timestamps()

        for i in range(abs(day)):
            self.__jump_post_day()        

        return self.__create_json()
    

        #print(axis_data.find_element_by_xpath("/following-sibling::*[name()=text]").get_attribute('innerHTML'))




    
    def close(self):
        self.__driver.quit()

    

