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

class DescargaRAM(Fuente):

	def getMac(self):
		chrome_options = webdriver.ChromeOptions()
		prefs = {
			'download.default_directory': '/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/resolucionesUrgencia/pdfs',
			"download.prompt_for_download": False,
			"download.directory_upgrade": True,
			"safebrowsing_for_trusted_sources_enabled": False,
			"safebrowsing.enabled": False
		}
		chrome_options.add_experimental_option('prefs', prefs)
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
		chrome_options.binary_location = '..//convenios_y_transferencias//webdriver//chrome-mac//Chromium.app//Contents//MacOS//Chromium'  # Ruta a la versión de Chromium 114.0.5735.90
		#chrome_options.add_argument('--headless')
		driver = webdriver.Chrome(executable_path='..//convenios_y_transferencias//webdriver//chromedriver', chrome_options=chrome_options)
		driver.maximize_window()
		return driver

	def __init__(self, datos):

		sistema_operativo = platform.system()
		if sistema_operativo == 'Darwin':
			print("Estás utilizando un sistema Mac")
			driver = self.getMac()
		elif sistema_operativo == 'Windows':
			print("Estás utilizando un sistema Windows.")

		driver.get('https://www.sis.mejorninez.cl/')
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@servicioproteccion.gob.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Mejorninez")
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ingresar"))).click()
		driver.get("https://a1.sis.mejorninez.cl/mod_ninos/cierre_movmensual.aspx")

		cnx = sqlite3.connect('resolucionesUrgencia.db')
		consulta  = " \
			SELECT \
				resolucionesExentas.proyecto, \
				resolucionesExentas.mesAtencion, \
				resolucionesExentas.mes, \
				resolucionesExentas.anio \
			FROM \
				resolucionesExentas \
		"
		query = pd.read_sql_query(consulta, cnx)

		self.pendientes(cnx, query, driver, datos)

		def pendientes(self, cnx, query, driver, datos):
			print(query)
			print("====================== pendientes")
			for index, row in query.iterrows():
				print("==== ", row )
				envioInforProyecto = Envio_Informacion()
				driver.get(f"https://a1.sis.mejorninez.cl/mod_ninos/cierre_resumenatencion.aspx?sw=4&codinst={row['proyecto']}&M={row['mes']}&A={row['anio']}")
				WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "Imb002"))).click()
			driver.quit()






