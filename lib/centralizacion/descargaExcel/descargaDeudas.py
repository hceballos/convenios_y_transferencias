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
import openpyxl
import xlrd


class Deudas(object):
	def __init__(self):

		for f in glob.glob('/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/centralizacion/reporteDeuda/*', recursive=True):
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
			'download.default_directory': os.getcwd()+'/input_excel/centralizacion/reporteDeuda/',
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

		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Consultas/wf_ReportesFinancieroConsulta.aspx")
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='gvReportes']/tbody/tr[7]/td[2]"))).click()  # BOTON BUSCAR
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "lnkGenerar"))).click()  # BOTON BUSCAR
		time.sleep(20)
		driver.quit()

		# Define la función para eliminar etiquetas HTML
		def eliminar_etiquetas_html(texto_html):
			texto_limpio = texto_html.replace('<tr>', '').replace('</tr>', '').replace('<td>', '').replace('</td>', '').replace('</Td><Td>', '').replace('</TR><Td>', '').replace('</Td>', '').replace('<TR><Td>', '')
			return texto_limpio
	
		# Ruta al archivo Excel
		for f in glob.glob('/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/centralizacion/reporteDeuda/Reporte_Deudas*.xls', recursive=True):
			# print('Procesando  : ', f)
			# Leer el archivo .xls y convertirlo a .xlsx
			try:
				wb = openpyxl.Workbook()
				ws = wb.active
				
				with open(f, 'rb') as x:
					content = x.read().decode('utf-16')
					for row in content.split('\n'):
						row_data = row.strip().split('\t')
						ws.append(row_data)
				
				# Guardar el archivo .xlsx
				archivo_salida = '/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/centralizacion/reporteDeuda/Deudas.xlsx'
				wb.save(archivo_salida)
				# print('El archivo se ha convertido a .xlsx correctamente')
				
				# Leer el archivo .xlsx en un DataFrame
				df = pd.read_excel(archivo_salida)
				df = df.drop(df.index[-1])

				nombres_columnas =  ['Id Deuda', 'Id Cuota', 'Tipo Deuda', 'Código Proyecto', 'Nombre Proyecto', 'Fecha Deuda', 'Fecha Actualización', 'Usuario',
				'Observación', 'Tipo', 'Monto Total', 'Cantidad Cuotas', 'N° Cuota', 'Fecha Vencimiento', 'Monto Cuota', 'Estado Cuota','a','s','r'
				]

				df.columns = nombres_columnas
				#df['Monto Total']          = df['Monto Total'].astype(int)
				#df['Monto Cuota']          = df['Monto Cuota'].astype(int)

				# Aplicar la función para eliminar etiquetas HTML a todas las celdas del DataFrame
				df = df.applymap(lambda x: eliminar_etiquetas_html(str(x)) if isinstance(x, str) else x)

				# Guardar el DataFrame modificado en el mismo archivo .xlsx
				df.to_excel(archivo_salida, index=False)
				# print('Se han eliminado las etiquetas HTML del archivo .xlsx')
			
			except Exception as e:
				print(f"Error al procesar el archivo: {e}")


			# Verificar si el archivo existe antes de intentar eliminarlo
			if os.path.exists(f):
				# Eliminar el archivo
				os.remove(f)
				# print("El archivo se ha eliminado exitosamente.")
			else:
				print("El archivo no existe.")



