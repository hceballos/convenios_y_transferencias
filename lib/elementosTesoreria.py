from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import time
import re


class Envio_Informacion(object):
    
    def envio_Informacion_by_name(self, driver, primero, segundo):
        envio  = driver.find_element_by_name(primero)
        envio.clear()
        envio.send_keys(segundo)
        time.sleep(2)
        
    def envio_Informacion_by_id(self, driver, primero, segundo):
        envio  = driver.find_element_by_id(primero)
        envio.clear()
        envio.send_keys(segundo)
        time.sleep(2)

class Click(object):
    
    def click_by_id(self, driver, primero):
        click = driver.find_element_by_id(primero)
        click.click()        
        time.sleep(2)

    def click_by_xpath(self, driver, primero):
        click = driver.find_element_by_xpath(primero)
        click.click()
        time.sleep(2)

    def click_by_name(self, driver, primero):
        click = driver.find_element_by_name(primero)
        click.click()        
        time.sleep(2)