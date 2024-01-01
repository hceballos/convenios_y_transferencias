from lib.elementos import Envio_Informacion
from lib.elementos import Click
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from lib.fuente import Fuente
import time
import re
import sqlite3
import pandas as pd


class ScrapingXpert(Fuente):

    def buscar_element_by_xpath(self, driver, primero):
        try:
            #print("                 : ", driver.find_element_by_xpath(primero).get_attribute("value") )
            return driver.find_element_by_xpath(primero).get_attribute("value")
        except:
            pass

    def __init__(self, json_path):
        Fuente.__init__(self, json_path)

        datos = self.datos

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=options)
        driver.get("https://barros.experthis.cl/produccion/login.php")

        time.sleep(14)
