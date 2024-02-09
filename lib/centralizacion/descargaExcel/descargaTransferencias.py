import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
import re
import platform
import time
import sqlite3
import re
import platform
import pandas as pd
import glob
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from PyPDF2 import PdfReader
from lib.fuente import Fuente
from lib.elementos import Envio_Informacion, Click
from lib.contraloria.scrapyProceso.tablaPagos import TablaPagos
import os


# Nuevo
class Transferencias(object):
	def __init__(self):

		for f in glob.glob(os.getcwd()+'/input_excel/centralizacion/transferencias/*', recursive=True):
			# print('Procesando  : ', f)
			# Verificar si el archivo existe antes de intentar eliminarlo
			if os.path.exists(f):
				# Eliminar el archivo
				os.remove(f)
				# print("El archivo se ha eliminado exitosamente.")
			else:
				print("El archivo no existe.")


		chrome_options = webdriver.ChromeOptions()
		prefs = {
			'download.default_directory': os.getcwd()+'/input_excel/centralizacion/transferencias/',
			"download.prompt_for_download": False,
			"download.directory_upgrade": True,
			"safebrowsing_for_trusted_sources_enabled": False,
			"safebrowsing.enabled": False
		}

		sistema_operativo = platform.system()
		if sistema_operativo == 'Darwin':
			print("Estás utilizando un sistema Mac")
			chrome_options.add_experimental_option('prefs', prefs)
			chrome_options.add_argument('--ignore-certificate-errors')
			chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
			chrome_options.binary_location = '..//convenios_y_transferencias//webdriver//chrome-mac//Chromium.app//Contents//MacOS//Chromium'  # Ruta a la versión de Chromium 114.0.5735.90
			#chrome_options.add_argument('--headless')
			driver = webdriver.Chrome(executable_path='..//convenios_y_transferencias//webdriver//chromedriver', chrome_options=chrome_options)
			driver.maximize_window()

		elif sistema_operativo == 'Windows':
			print("Estás utilizando un sistema Windows.")
			chrome_options.add_experimental_option('prefs', prefs)
			chrome_options.add_argument('--ignore-certificate-errors')
			chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
			#chrome_options.add_argument('--headless')
			driver = webdriver.Chrome(executable_path='..//convenios_y_transferencias//webdriver//chromedriver', chrome_options=chrome_options)
			driver.maximize_window()
		
		driver.get('https://www.sis.mejorninez.cl/')
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@servicioproteccion.gob.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Mejorninez")
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ingresar"))).click()

		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Transferencias.aspx")
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "lnk_btn_buscar"))).click()  # BOTON BUSCAR
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "lnk_Descargar"))).click()  # BOTON BUSCAR

		time.sleep(20)
		driver.quit()

		# Ruta al archivo Excel
		for f in glob.glob(os.getcwd()+'/input_excel/centralizacion/transferencias/*.xls', recursive=True):
			# print('Procesando  : ', f)
			archivo_entrada = f
			archivo_salida = os.getcwd()+'/input_excel/centralizacion/transferencias/transferencias.xlsx'

			# Utilizar pandas para leer el archivo .xls y luego guardarlo como .xlsx
			df = pd.read_csv(archivo_entrada, delimiter='\t', encoding='utf-16')

			# Eliminar la última fila
			df = df.drop(df.index[-1])

			# Reemplazar el nombre de las columnas
			nombres_columnas =  ['MES ATENCION', 'ID TIPO PAGO', 'TIPO PAGO', 'FOLIO', 'COD REGION', 'COD PROYECTO', 'PROYECTO', 'COD INSTITUCION', 'INSTITUCION',
			'DEPARTAMENTO SENAME', 'TIPO SUBVENCION_DES', 'TIPO PROYECTO_DES', 'MODELO INTERVENCION', 'BANCO', 'CUENTA CORRIENTE NUMERO', 
			'RUT PROYECTO', 'MONTO MAXIMO PAGO', 'MONTO PAGO FIJO', 'MONTO PAGO VARIABLE', 'MONTO POR ATENCION', 'MONTO DEUDA',
			'MONTO RELIQUIDACION', 'MONTO RETENCION', 'MONTO LIQUIDO PAGADO', 'PLAZAS CONVENIDAS', 'PLAZAS ATENDIDAS', 'FACTOR FIJO',
			'FACTOR VARIABLE', 'FACTOR EDAD', 'FACTOR COBERTURA', 'FACTOR DISCAPACIDAD', 'FACTOR COMPLEJIDAD', 'FACTOR CVF',
			'ASIGNACION ZONA', 'FACTOR USS', 'USS', 'NUMERO PLAZAS', 'NRO DIAS', 'FECHA CIERRE PAGO ', 'NUMERO RESOLUCION',
			'FECHA CREACION', 'FECHA TERMINO', 'NUMERO CDP', 'ANNO PRESUPUESTARIO', 'NUMERO RESOLUCION CDP', 'FECHA RESOLUCION CDP', 'DESCRIPCION CDP']

			df.columns = nombres_columnas

			# Función para eliminar etiquetas HTML específicas de una cadena
			def eliminar_etiquetas_html(texto_html):
				texto_limpio = texto_html.replace('<tr>', '').replace('</tr>', '').replace('<td>', '').replace('</td>', '').replace('</Td><Td>', '').replace('</TR><Td>', '').replace('</Td>', '').replace('<TR><Td>', '')
				return texto_limpio

			# Aplicar la función a todas las celdas del DataFrame
			df = df.applymap(lambda x: eliminar_etiquetas_html(str(x)) if isinstance(x, str) else x)

			"""
			df['PlzAtendidas']			= df['PlzAtendidas'].astype(int)
			df['DiasAtencion']			= df['DiasAtencion'].astype(int)
			df['Diferencia_Plazas']		= df['Diferencia_Plazas'].astype(int)
			df['OrdenRegion']			= df['OrdenRegion'].astype(int)
			df['Plazas_80Bis_APago']	= df['Plazas_80Bis_APago'].astype(int)
			df['Plazas_Convenidas']		= df['Plazas_Convenidas'].astype(int)
			"""

			# Guardar el DataFrame en un nuevo archivo Excel
			df.to_excel(archivo_salida, index=False, engine='openpyxl')

			# Ruta del archivo que deseas eliminar
			archivo_a_eliminar = f

			# Verificar si el archivo existe antes de intentar eliminarlo
			if os.path.exists(archivo_a_eliminar):
				# Eliminar el archivo
				os.remove(archivo_a_eliminar)
				# print("El archivo se ha eliminado exitosamente.")
			else:
				print("El archivo no existe.")
