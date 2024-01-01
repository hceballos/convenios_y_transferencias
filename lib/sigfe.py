from lib.elementos import Envio_Informacion
from lib.elementos import Click
from lib.elementos import Buscar_Elemento
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


class Sigfe():

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
        driver.get(datos['url_sigfe'])
        # Mercado Publico
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(datos['url_mercado_publico'])
        print( " SIGFE >>>>>>>>>>>>" )
        Sigfe   = driver.switch_to.window(driver.window_handles[0])

        self.login(driver, datos)

    def login(self, driver, datos):
        print( "login" )
        envioInformacion = Envio_Informacion()
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_username'], datos['j_username'])
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_password'], datos['j_password'])

        click = Click()
        click.click_by_id(driver, datos['botton_Ingresar'])

        if len( re.findall('(?<=errorAutenticacion).*?(?=._)', driver.current_url) ) > 0:
            click.click_by_id(driver, datos['Cerrar_Sesion'])
            return self.login(driver, datos)

        time.sleep(5)

        self.navegacion(driver, datos)

    def navegacion(self, driver, datos):
        print( "navegacion" )
        try:
            print("navegacion try")
            devengo = driver.find_element_by_xpath('//*[@id="idPgTpl:j_id30"]/div/table/tbody/tr/td[2]/a').click()
            time.sleep(2)
            hover = ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="idPgTpl:j_id31"]/td[2]')).click()
            hover.perform()
            time.sleep(4)

            self.ingresar_ConceptoPresupuestarios(driver, datos)
        except :
            print(">> navegacion except")
            click = Click()
            click.click_by_xpath(driver, datos['menu_devengo'])
            time.sleep(2)
            click.click_by_xpath(driver, datos['buscar_devengo'])

            self.ingresar_ConceptoPresupuestarios(driver, datos)

    def ingresar_ConceptoPresupuestarios(self, driver, datos):
        time.sleep(3)
        try:
            print('>> ingresar_ConceptoPresupuestarios try')
            envioInformacion = Envio_Informacion()
            envioInformacion.envio_Informacion_by_id(driver, datos['inputText_Concepto_Presupuestario_id'], datos['Conceptos_Presupuestarios'])
            self.botonBuscar(driver, datos)
        except:
            time.sleep(3)
            print('>> ingresar_ConceptoPresupuestarios except')
            envioInformacion = Envio_Informacion()
            envioInformacion.envio_Informacion_by_name(driver, datos['inputText_Concepto_Presupuestario_name'], datos['Conceptos_Presupuestarios'])
            self.botonBuscar(driver, datos)

    def botonBuscar(self, driver, datos):
        time.sleep(5)
        print('>> botonBuscar ')
        click = Click()
        click.click_by_id(driver, datos['botton_Buscar'])

        self.tabla(driver, datos)

    def tabla(self, driver, datos):
        time.sleep(5)
        print('>> tabla ')
        lineas =  re.findall('(?<=_afrrk=").*?(?=Historial)', driver.page_source)
        for linea in lineas:
            numero = re.findall('.*?(?=" class="af_table_data-row)', linea)[0]
            print(numero)
            contenido =re.findall('(?<=nowrap="">).*?(?=<\/td)', linea)

            self.visualizar(driver, datos, numero, contenido)

        self.siguiente(driver, datos)

    def siguiente(self, driver, datos):
        siguiente = driver.find_element_by_link_text('Siguiente >>')
        time.sleep(4)
        siguiente.click()

        self.tabla(driver, datos)

    def visualizar(self, driver, datos, numero, contenido):
        tabla = driver.find_element_by_id('idTmpB:tRes:'+str(numero)+':idCmlIrVisualizar')
        tabla.click()
        time.sleep(5)

        self.pestanasVisualizar(driver, datos, contenido)

    def pestanasVisualizar(self, driver, datos, contenido):
        pestanas =  list(dict.fromkeys(re.findall('VisualizaVariacionPopup:nvPnDet:docum_\d|VisualizaOtrosDocsPopup:nvPnDet:docum_\d', driver.page_source)))

        for x in pestanas:
            print(x)

        for pestana in pestanas:
            click = Click()
            click.click_by_id(driver, pestana )

            parse = Buscar_Elemento()
            parse.elemento(driver, datos )
            time.sleep(4)

        print("  ====================================== ")
        self.cerrarVisualizar(driver)

    def cerrarVisualizar(self, driver):
        try:
            cerrarVisualizar = driver.find_element_by_id("VisualizaOtrosDocsPopup:idDialVisualizaPersona::close")
            cerrarVisualizar.click()
            return
        except :
            cerrarVisualizar = driver.find_element_by_id("VisualizaVariacionPopup:idDialVisualizaPersona::close")
            cerrarVisualizar.click()
            return

        print('>> FIN ')
