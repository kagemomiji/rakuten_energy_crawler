# coding: utf-8

import requests
import configparser
import os
import errno

class Client:
    def __init__(self):
        self.__load_config()
        self.__url = self.__config.get('URL')
        self.__user = self.__config.get('USER')
        self.__password = self.__config.get('PASSWORD')

    def __load_config(self):
        config_ini = configparser.ConfigParser()
        config_ini_path = "config.ini"
        if os.path.exists(config_ini_path):
            # iniファイルが存在する場合、ファイルを読み込む
            with open(config_ini_path, encoding='utf-8') as fp:
                config_ini.read_file(fp)
            
            self.__config = config_ini["WEBHOOK"]
    
    def post_data(self,json_data):
        r = requests.post(self.__url,data=json_data,auth=(self.__user,self.__password))
        print(r)

