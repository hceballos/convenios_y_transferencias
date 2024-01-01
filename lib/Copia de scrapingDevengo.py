from lib.elementos import Envio_Informacion
from lib.elementos import Click
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from lib.fuente import Fuente
import time
import re
import sqlite3
import pandas as pd


class ScrapingDevengo(Fuente):

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

        click = Click()
        click.click_by_id(driver, datos['botton_Ingresar'])

        if len( re.findall('(?<=errorAutenticacion).*?(?=._)', driver.current_url) ) > 0:
            click.click_by_id(driver, datos['Cerrar_Sesion'])
            return self.login(driver, datos)

        time.sleep(5)

        self.navegacion(driver, datos)

    def navegacion(self, driver, datos):
        try:
            driver.find_element_by_xpath('//*[@id="idPgTpl:j_id30"]/div/table/tbody/tr/td[2]/a').click()
            time.sleep(2)
            hover = ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="idPgTpl:j_id31"]/td[2]')).click()
            hover.perform()
            time.sleep(4)

            self.ingresar_ConceptoPresupuestarios(driver, datos)
        except :
            click = Click()
            click.click_by_xpath(driver, datos['menu_devengo'])
            time.sleep(2)
            click.click_by_xpath(driver, datos['buscar_devengo'])

            self.ingresar_ConceptoPresupuestarios(driver, datos)

    def ingresar_ConceptoPresupuestarios(self, driver, datos):
        time.sleep(4)
        cnx = sqlite3.connect('database.db')

        consulta  = " \
            SELECT \
                Asigfe.'Número Documento', \
                Asigfe.'N_Concepto', \
                Asigfe.'Rut', \
                Asigfe.'Título' \
            FROM \
                Asigfe \
            WHERE \
                Asigfe.'identificacion' IS NULL \
            ORDER BY \
                Asigfe.'Número Documento' ASC \
            LIMIT 1 \
        "
        query = pd.read_sql_query(consulta, cnx)

        print(query)

        for index, row in query.iterrows():
            envioInformacion = Envio_Informacion()
            envioInformacion.envio_Informacion_by_id(driver, "idTmpB:idInteNumDocumento::content", row['Número Documento'])
            envioInformacion.envio_Informacion_by_id(driver, "idTmpB:idInteConceptoPresupuestario::content", row['N_Concepto'])

            self.botonBuscar(driver, datos, row, cnx)

    def botonBuscar(self, driver, datos, row, cnx):
        time.sleep(5)
        click = Click()
        click.click_by_id(driver, datos['botton_Buscar'])

        try:
            identificacion = driver.find_element_by_class_name("af_column_data-cell").text
        except:
            identificacion = driver.find_element_by_xpath("//*[@id='idTmpB:tRes::db']/table/tbody/tr/td[1]/nobr")

        time.sleep(5)
        self.visualizar(driver, datos, row, identificacion, cnx)

    def visualizar(self, driver, datos, row, identificacion, cnx):
        tabla = driver.find_element_by_id('idTmpB:tRes:0:idCmlIrVisualizar')
        tabla.click()
        time.sleep(5)

        self.pestanasVisualizar(driver, datos, row, identificacion, cnx)

    def pestanasVisualizar(self, driver, datos, row, identificacion, cnx):
        pestanas =  list(dict.fromkeys(re.findall('VisualizaVariacionPopup:nvPnDet:docum_\d|VisualizaOtrosDocsPopup:nvPnDet:docum_\d', driver.page_source)))



        conexion = sqlite3.connect("database.db")
        for pestana in pestanas:
            click = Click()
            click.click_by_id(driver, pestana )

            Compromiso = list(dict.fromkeys(re.findall('((?<="VisualizaOtrosDocsPopup:itAgrp:).*?(?=:idCmbConceptoInsumoCompromisoVisualizar:idPaboCombConcIns)|(?<=VisualizaVariacionPopup:itAgrp:).*?(?=:idCmbConceptoInsumoCompromisoVisualizar:idPaboCombConcIns))', driver.page_source)))
            for x in Compromiso:
                Compromiso_Presupuestario = driver.find_element_by_xpath("//*[@id='VisualizaVariacionPopup:itAgrp:"+str(x)+":idCmbConceptoInsumoCompromisoVisualizar:idPagrRequerimientoCompromisoVisualizar']/tbody/tr/td[2]/span|//*[@id='VisualizaOtrosDocsPopup:itAgrp:"+str(x)+":idCmbConceptoInsumoCompromisoVisualizar:idPagrRequerimientoCompromisoVisualizar']/tbody/tr/td[2]/span").text


                principal           = self.split(driver, datos["Principal"])
                OrdenCompra         = self.buscar_OC_by_xpath(driver, datos["Orden_Compra"])
                Factura             = self.buscar_element_by_xpath(driver, datos["Num_Factura"])
                Monto               = self.replace(driver, datos["Monto"])
                Fecha_Cumplimiento  = self.fecha(driver, datos["Fecha_Cumplimiento"])
                Tipo_Documento      = self.buscar_tipo_Documento(driver, datos["Tipo_Documento"])
                Titulo_Devengo      = self.buscar_element_by_xpath(driver, datos["Titulo_Devengo"])


                #print(">>>>>>>>> : ", principal, OrdenCompra, Factura, Monto, Fecha_Cumplimiento, Tipo_Documento, Titulo_Devengo, Compromiso_Presupuestario )

                print("========= Número Documento           : ", row['Número Documento'] )
                print(">>>>>>>>> Factura                    : ", Factura )

                #print("========= N_Concepto                 : ", row['N_Concepto'] )
                print("========= Rut                        : ", row['Rut'] )
                print(">>>>>>>>> principal                  : ", principal )

                print("========= Título                     : ", row['Título'] )
                print(">>>>>>>>> Titulo_Devengo             : ", Titulo_Devengo )



                print(">>>>>>>>> N_Concepto                 : ", row['N_Concepto'] )
                print(">>>>>>>>> OrdenCompra                : ", OrdenCompra )
                print(">>>>>>>>> Fecha_Cumplimiento         : ", Fecha_Cumplimiento )
                print(">>>>>>>>> Tipo_Documento             : ", Tipo_Documento )
                print(">>>>>>>>> Titulo_Devengo             : ", Titulo_Devengo )
                print(">>>>>>>>> Compromiso_Presupuestario  : ", Compromiso_Presupuestario )


                """
                print(">>>>>>>>> identificacion             : ", identificacion )
                print(">>>>>>>>> N_Concepto                 : ", row['N_Concepto'] )
                print(">>>>>>>>> principal                  : ", principal )
                print(">>>>>>>>> OrdenCompra                : ", OrdenCompra )
                print(">>>>>>>>> Factura                    : ", Factura )
                print(">>>>>>>>> Monto                      : ", Monto )
                print(">>>>>>>>> Fecha_Cumplimiento         : ", Fecha_Cumplimiento )
                print(">>>>>>>>> Tipo_Documento             : ", Tipo_Documento )
                print(">>>>>>>>> Titulo_Devengo             : ", Titulo_Devengo )
                print(">>>>>>>>> Compromiso_Presupuestario  : ", Compromiso_Presupuestario )
                """
                print(" ")









                cnx.execute('SELECT * FROM Asigfe WHERE Rut=? and Título=?', principal, Titulo_Devengo)

                print (cnx.fetchone())



                conexion.execute("""UPDATE Asigfe SET identificacion=?, Orden_de_Compra=?, Fecha_Cumplimiento=?, Compromiso_Presupuestario=? WHERE Numero_Documento=? and Rut=? and Título=? """, (identificacion, OrdenCompra, Fecha_Cumplimiento, Compromiso_Presupuestario, Factura, principal, Titulo_Devengo) )
                #conexion.execute("""UPDATE Asigfe SET identificacion = ?, Orden_de_Compra=?, Fecha_Cumplimiento=? WHERE Folio= ? and N_Concepto=? and Numero_Documento=? """, (identificacion, OrdenCompra, Fecha_Cumplimiento, row["Folio"], row['N_Concepto'], row['Número Documento']))
                conexion.commit()
                print("Table updated...... ")

        self.cerrarVisualizar(driver, datos)
        self.ingresar_ConceptoPresupuestarios(driver, datos)


    def cerrarVisualizar(self, driver, datos):
        click = Click()
        click.click_by_xpath(driver, datos['cerrarVisualizar'])
