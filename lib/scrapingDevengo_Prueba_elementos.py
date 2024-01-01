from lib.elementos import Envio_Informacion
from lib.elementos import Click
from lib.database import Database
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from lib.fuente import Fuente
import time
import re
import sqlite3
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapingDevengo_Prueba_elementos(Fuente):

    def buscar_OC_by_xpath(self, driver, primero):
        try:
            valor = driver.find_element_by_xpath(primero).get_attribute("value")
            if valor == None:
                return "Sin Registro"
            else:
                return valor
        except NoSuchElementException:
            return "Sin Registro"

    def buscar_element_by_xpath(self, driver, primero):
        valor = driver.find_element_by_xpath(primero).get_attribute("value")
        if valor is not None:
            return valor
        else:
            return "Sin Registro"


    def split(self, driver, primero):
        string = driver.find_element_by_xpath(primero).get_attribute("value")
        return string.split(" ")[0]

    def replace(self, driver, primero):
        string = driver.find_element_by_xpath(primero).get_attribute("value")
        # print("===== ", type(int(string.replace(".", ""))) ,int(string.replace(".", "")) )
        return int(string.replace(".", ""))

    def fecha(self, driver, primero):
        fecha = driver.find_element_by_xpath(primero).get_attribute("value")
        return fecha

    def buscar_tipo_Documento(self, driver, primero):
        try:
            valor = driver.find_element_by_xpath(primero).get_attribute("value")
            if valor is None:
                return "Sin Registro"
            else:
                return valor
        except:
            return driver.find_element_by_xpath(primero)

    def __init__(self, json_path):
        Fuente.__init__(self, json_path)

        datos = self.datos

        options = Options()
        options.headless = True
        # driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=options)
        driver = webdriver.Chrome(executable_path=datos['webdriver_path'])

        self.setUp(driver, datos)

    def setUp(self, driver, datos):
        driver.switch_to.window(driver.window_handles[0])
        driver.get(datos['url_sigfe'])

        self.login(driver, datos)

    def login(self, driver, datos):
        envioInformacion = Envio_Informacion()
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_username'], datos['j_username_Hector'])
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_password'], datos['j_password_Hector'])

        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, datos['botton_Ingresar'] )))
        element.click()

        if len( re.findall('(?<=errorAutenticacion).*?(?=._)', driver.current_url) ) > 0:
            click.click_by_id(driver, datos['Cerrar_Sesion'])
            return self.login(driver, datos)

        time.sleep(5)
