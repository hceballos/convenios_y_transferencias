from lib.elementosTesoreria import Envio_Informacion
from lib.elementosTesoreria import Click
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import time
import re
import pandas as pd
from lib.fuente import Fuente

class ScrapingTesoreria(Fuente):

    def __init__(self, json_path):
        Fuente.__init__(self, json_path)

        datos = self.datos

        options = Options()
        options.headless = True
        #driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=options)
        driver = webdriver.Chrome(executable_path=datos['webdriver_path'])
        driver.get(datos['url_sigfe'])

        self.login(driver, datos)

    def login(self, driver, datos):
        envioInformacion = Envio_Informacion()
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_username'], datos['j_username_Hector'])
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_password'], datos['j_password_Hector'])

        click = Click()
        click.click_by_id(driver, datos['botton_Ingresar'])

        if len( re.findall('(?<=errorAutenticacion).*?(?=._)', driver.current_url) ) > 0:
            click.click_by_id(driver, datos['Cerrar_Sesion'])
            return self.login(driver, datos)

        time.sleep(3)

        self.navegacion(driver, datos)

    def navegacion(self, driver, datos):
        click = Click()
        click.click_by_xpath(driver, datos['menu_tesoreria'])
        hover = ActionChains(driver).move_to_element(driver.find_element_by_xpath("//*[@id='idPgTpl:j_id52']/td[2]")).click()
        hover.perform()
        time.sleep(4)

        self.tipo_de_Operación(driver, datos)

    def tipo_de_Operación(self, driver, datos):
        click = Click()
        click.click_by_xpath(driver, datos['tipo_de_Operación'])
        time.sleep(3)

        self.folios(driver, datos)

    def folios(self, driver, datos):
        excel_data_df = pd.read_excel('input_excel_tesoreria/Tesoreria.xlsx')
        folios = excel_data_df['folio'].tolist()

        d = {"los_folios" : folios}
        datos.update(d)

        for x in datos['los_folios']:
            print("Processing folio : ", x )
            envioInformacion = Envio_Informacion()
            envioInformacion.envio_Informacion_by_id(driver, datos['inputText_Folio'], str(x) )

            self.botonBuscar(driver, datos)

        print("Aqui viene la union de los PDF's")

    def botonBuscar(self, driver, datos):
        try:
            click = Click()
            click.click_by_id(driver, datos['botton_Buscar_tesoreria'])

            self.transaccional(driver, datos)
        except :
            print("EL error botonbuscar Folio de arriba")

    def transaccional(self, driver, datos):
        try:
            click = Click()
            click.click_by_id(driver, datos['Transaccional'])
            time.sleep(2)
            self.emitir_Formulario(driver, datos)
        except :
            time.sleep(2)
            print("EL error transaccional Folio de arriba")

    def emitir_Formulario(self, driver, datos):
        click = Click()
        click.click_by_id(driver, datos['botton_emitir_Formulario'])
        time.sleep(2)

        self.condiciones_Emision(driver, datos)

    def condiciones_Emision(self, driver, datos):
        click = Click()
        click.click_by_id(driver, datos['botton_aceptar'])
        time.sleep(2)

        return self.cerrar(driver, datos)

    def cerrar(self, driver, datos):
        click = Click()
        click.click_by_id(driver, datos['cerrar_condiciones_Emision'])
        time.sleep(2)
        click.click_by_id(driver, datos['cerrar_vista_transaccional'])
        time.sleep(2)
