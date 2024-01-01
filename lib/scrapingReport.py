from lib.elementos import Envio_Informacion
from lib.elementos import Click
from lib.elementos import Ficheros
from lib.database import Database
from lib.fuente import Fuente
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import re
import sqlite3
import pandas as pd


class ScrapingReport(Fuente):
    def __init__(self, json_path):
        Fuente.__init__(self, json_path)

        datos = self.datos

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=datos['webdriver_path'])
        #driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=options)
        driver.get(datos['url_sigfe_report'])
        #print ("Headless Chrome Initialized")
        self.login(driver, datos)

    def login(self, driver, datos):
        print('>> login ')
        envioInformacion = Envio_Informacion()
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_username'], datos['j_username_Hector'])
        envioInformacion.envio_Informacion_by_name(driver, datos['inputText_password'], datos['j_password_Hector'])

        click = Click()
        click.click_by_id(driver, datos['botton_Ingresar'])

        if len( re.findall('(?<=errorAutenticacion).*?(?=._)', driver.current_url) ) > 0:
            click.click_by_id(driver, datos['Cerrar_Sesion'])
            return self.login(driver, datos)

        self.navegacion(driver, datos)

    def navegacion(self, driver, datos):
        time.sleep(3)
        print('>> navegacion ')
        driver.find_element_by_class_name(datos['click_reportabilidad']).click()

        reportabilidad_Presupuestaria = ActionChains(driver).move_to_element(driver.find_element_by_xpath(datos['click_reportabilidad_Presupuestaria']))
        reportabilidad_Presupuestaria.perform()
        time.sleep(1)

        cartera_Financiera_Presupuestaria = ActionChains(driver).move_to_element(driver.find_element_by_xpath(datos['click_cartera_Financiera_Presupuestaria'])).click()
        cartera_Financiera_Presupuestaria.perform()

        self.criterios_de_busqueda(driver, datos)

    def criterios_de_busqueda(self, driver, datos):
        print('>> criterios_de_busqueda ')
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
        except NoSuchElementException:
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
        #mover_fichero_nuevo.mover_elementos(driver, datos['fichero'], datos['mover_fichero_a'])


        spider = Database(datos)

        cnx = sqlite3.connect('database.db')
        consulta  = " \
            Select \
                unico, \
                Rut, \
                Numero_Documento, \
                Folio, \
                N_Concepto, \
                Tipo_Documento \
            From \
                Asigfe A \
            Where NOT EXISTS \
            ( select 1 from Complemento B \
            Where A.unico = B.unico \
            ) \
            ORDER BY \
                A.'unico' DESC \
        "
        query = pd.read_sql_query(consulta, cnx)

        for index, row in query.iterrows():
            print(row['unico'], row['Rut'], row['Folio'], row['Numero_Documento'], row['Folio'], row['N_Concepto'], row['Tipo_Documento'])


            cursor = cnx.cursor()
            sqlite_insert_with_param = """INSERT INTO Complemento
                              (unico, Rut, Numero_Documento, Folio, N_Concepto, Tipo_Documento)
                              VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (row['unico'], row['Rut'], row['Numero_Documento'], row['Folio'], row['N_Concepto'], row['Tipo_Documento'])
            cursor.execute(sqlite_insert_with_param, data_tuple)
            cnx.commit()
            cursor.close()
        print("Table Complemento updated...... ")





        print('>> FIN ')
