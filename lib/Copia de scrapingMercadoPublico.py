from lib.elementos import Envio_Informacion
from lib.elementos import Click
from lib.elementos import Buscar_Elemento
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from lib.fuente import Fuente
from sqlalchemy import create_engine
import time
import re
from xlsxwriter.utility import xl_rowcol_to_cell
import pandas as pd
import sqlalchemy
import sqlite3
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from pandas.io.html import read_html


class ScrapingMercadoPublico(Fuente):

    def buscar_monto_by_id(self, driver, primero):
        string = driver.find_element_by_id(primero).text
        remove_characters = [".", "$", " "]

        for character in remove_characters:
            string = string.replace(character, "")
        return pd.to_numeric(string)

    def buscar_monto_dataframe_by_id(self, primero):
        primero      = [w.replace(',00', '' ) for w in primero ]
        primero      = [w.replace(' ', '' ) for w in primero ]
        primero      = [w.replace('$', '' ) for w in primero ]
        primero      = [w.replace('.', '' ) for w in primero ]
        return pd.to_numeric(primero)


    def __init__(self, json_path):
        Fuente.__init__(self, json_path)

        datos = self.datos

        driver = webdriver.Chrome(executable_path=r'/Users/Hector/Desktop/automaton3/webdriver/chromedriver' )
        driver.get(datos['url_mercado_publico'])

        cnx = sqlite3.connect('database.db')
        consulta  = " \
        SELECT \
            Asigfe.'Orden_de_Compra' \
        FROM \
            Asigfe \
        WHERE \
            Asigfe.'Orden_de_Compra' IS NOT NULL \
        "
        ordenes = pd.read_sql_query(consulta, cnx)

        self.buscadorAvanzado(driver, datos, ordenes)

    def buscadorAvanzado(self, driver, datos, ordenes):
        for index, row in ordenes.iterrows():
            print("orden_de_compra                  : ", row['Orden_de_Compra'])
            buscadorAvanzado = driver.find_element_by_name('txtSearch').send_keys(row['Orden_de_Compra'])
            buscar = driver.find_element_by_name('btnBusqueda').click()
            time.sleep(5)

            filename = re.findall(r"(?<=PurchaseOrder).*?(?=',')", driver.page_source)
            url_base= 'http://www.mercadopublico.cl/PurchaseOrder/' + filename[0]

            driver.execute_script("window.open('');")
            time.sleep(4)
            ResultadoBusqueda = driver.switch_to.window(driver.window_handles[1])
            driver.get(url_base)
            time.sleep(4)

            self.resultadoBusqueda(driver, row, url_base)

    def resultadoBusqueda(self, driver, row, url_base):
        df = read_html(url_base,  attrs={"id":"gv"})[0]

        df.rename(columns={
            'CÃ³digo ONU': 'codigo_onu',
            'CÃ³digo ONU / LC-CM':'codigo_onu',
            'Producto / Servicio':'producto',
            'Cant.':'cantidad',
            'Esp. Comprador':'especificacion_comprador',
            'Esp. Proveedor':'especificacion_proveedor',
            'Precio Unit.':'precio_unitario',
            'Desc.':'descuento',
            'Total Unit.':'total_unitario',
            'Valor Total':'valor_total',
            'Cargos':'cargos',
            'Medida':'medida'
            }, inplace=True)


        print(" >>>> data.columns : ", df.columns)

        df['orden_de_Compra']               = row['Orden_de_Compra']
        df['nombre_orden_de_compra']        = driver.find_element_by_id("lblNamePOValue").text
        df['estado']                        = driver.find_element_by_id("lblStatusPOValue").text
        df['precio_unitario']               = self.buscar_monto_dataframe_by_id(df['precio_unitario'])
        df['descuento']                     = self.buscar_monto_dataframe_by_id(df['descuento'])
        df['cargos']                        = self.buscar_monto_dataframe_by_id(df['cargos'])
        df['total_unitario']                = self.buscar_monto_dataframe_by_id(df['total_unitario'])
        df['valor_total']                   = self.buscar_monto_dataframe_by_id(df['valor_total'])
        df['total_neto']                    = self.buscar_monto_by_id(driver, 'lblAmountShow')
        # df['Cargos']                        = self.buscar_monto_by_id(driver, 'lblChargesShow')
        df['iva']                           = self.buscar_monto_by_id(driver, 'lblTaxesShow')
        df['total_oc']                      = self.buscar_monto_by_id(driver, 'lblTotalAmountShow')

        print(" >>>> DESPUES data.columns : ", df.columns)

        engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
        df.to_sql('mercadoPublico', engine, if_exists='append')
        print("Table updated...... ")
        print(" ")

        """
        writer = pd.ExcelWriter('mainMercadoPublico.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Pandas')
        writer.save()
        """

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        volver =  driver.find_element_by_id("ImageButton1").click()
