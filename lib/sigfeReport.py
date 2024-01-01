from lib.elementos import Envio_Informacion
from lib.elementos import Click
from lib.elementos import Buscar_Elemento
from lib.elementos import Ficheros
from lib.exportar import Exportar
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
import json
import xlsxwriter
import csv
import glob
import os


class SigfeReport():

    def setUp(self, datos):
        
        # Sigfe headless
        #options = webdriver.FirefoxOptions()
        #options.add_argument('-headless')
        #driver = webdriver.Firefox(executable_path=r'/Users/Hector/Documents/desarrollo/automaton/webdriver/geckodriver', firefox_options=options)
        # Sigfe headless

        # PC
        driver = webdriver.Chrome(executable_path=r'C:\Users\hector.ceballos\Desktop\HectorCeballos\automaton\webdriver\chromedriver.exe')
        #driver = webdriver.Firefox(executable_path=r'C:\Users\hector.ceballos\Desktop\HectorCeballos\automaton\webdriver\geckodriver.exe')
        
        # MAC
        #driver = webdriver.Firefox(executable_path=r'/Users/Hector/Documents/desarrollo/automaton/webdriver/geckodriver')
        driver.switch_to.window(driver.window_handles[0])
        driver.get(datos['url_sigfe_report'])

        self.login(driver, datos)

    def login(self, driver, datos):
        envioInformacion = Envio_Informacion()
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_username'], datos['j_username'])
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_password'], datos['j_password'])

        click = Click()
        click.click_by_id(driver, datos['botton_Ingresar'])

        if len( re.findall('(?<=errorAutenticacion).*?(?=._)', driver.current_url) ) > 0:
            click.click_by_id(driver, datos['Cerrar_Sesion'])
            return self.login(driver, datos)

        self.navegacion(driver, datos)

    def navegacion(self, driver, datos):
        reportabilidad = driver.find_element_by_class_name(datos['click_reportabilidad']).click()

        reportabilidad_Presupuestaria = ActionChains(driver).move_to_element(driver.find_element_by_xpath(datos['click_reportabilidad_Presupuestaria']))
        reportabilidad_Presupuestaria.perform()
        time.sleep(1)

        cartera_Financiera_Presupuestaria = ActionChains(driver).move_to_element(driver.find_element_by_xpath(datos['click_cartera_Financiera_Presupuestaria'])).click()
        cartera_Financiera_Presupuestaria.perform()

        self.criterios_de_busqueda(driver, datos)

    def criterios_de_busqueda(self, driver, datos):
        borrar_ficheros_antiguos = Ficheros()
        borrar_ficheros_antiguos.eliminar_elementos(driver, datos['fichero'])
        borrar_ficheros_antiguos.eliminar_elementos(driver, datos['borar_fichero_anterior'])
                 
        click = Click()
        click.click_by_xpath(driver, datos['click_compromiso_Cartera_Financiera'])
        click.click_by_xpath(driver, datos['click_reportabilidad_presupuestaria'])
        
        envioInformacion = Envio_Informacion()
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_fecha_desde'], datos['fecha_desde'])
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_fecha_hasta'], datos['fecha_hasta'])

        click.click_by_id(driver, datos['buscar_Concepto_Presupuestario'])
        time.sleep(5)
        
        try:
            click.click_by_xpath(driver, datos['click_catalogo_presupuestario'])
        except:
            time.sleep(3)
            click.click_by_xpath(driver, datos['click_catalogo_presupuestario'])
        
        click.click_by_id(driver, datos['22_bienes_y_servicios_de_consumo'])
        click.click_by_id(driver, datos['29_adquisicion_de_activos_no_financ'])        
        
        time.sleep(5)
        click.click_by_id(driver, datos['botton_aceptar_Catalogo_presupuestario'])

        click.click_by_id(driver, datos['botton_Buscar_report'])
        click.click_by_id(driver, datos['click_excel_report'])
        click.click_by_id(driver, datos['click_vista_de_datos'])
        click.click_by_id(driver, datos['click_exportar'])

        mover_fichero_nuevo = Ficheros()
        mover_fichero_nuevo.mover_elementos(driver, datos['fichero'], datos['mover_fichero_a'])

        print('>> FIN ')