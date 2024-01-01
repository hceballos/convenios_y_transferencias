#! /bin/env python3
from datetime import date
from lib.elementos import Click
from lib.elementos import Envio_Informacion
from lib.fuente import Fuente
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine, Table, Column, String, MetaData, insert, update, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import re
import sqlite3
import time


class ApruebaConvenio(Fuente):

	def extraer_fecha(self, dataframe, columna_original):
		"""
		Convierte el formato de la fecha de 'YYYY-MM-DD' a 'DD-MM-YYYY'.

		Parameters:
		- dataframe (pd.DataFrame): El DataFrame que contiene la columna de fechas.
		- columna_original (str): El nombre de la columna que contiene fechas en formato 'YYYY-MM-DD'.

		Returns:
		- pd.Series: Una nueva serie con las fechas en formato 'DD-MM-YYYY'.
		"""
		# Clonar el DataFrame para evitar modificar el original
		df = dataframe.copy()

		# Convertir la columna a formato datetime
		df[columna_original] = pd.to_datetime(df[columna_original])

		# Formatear la fecha en 'DD-MM-YYYY'
		fecha_formateada = df[columna_original].dt.strftime('%d-%m-%Y')

		return fecha_formateada








	def __init__(self, json_path):
		Fuente.__init__(self, json_path)

		datos = self.datos

		chrome_options = webdriver.ChromeOptions()
		prefs = {
			'download.default_directory': 'C:\\Users\\hceballos\\Downloads',
			"download.prompt_for_download": False,
			"download.directory_upgrade": True,
			"safebrowsing_for_trusted_sources_enabled": False,
			"safebrowsing.enabled": False
		}
		chrome_options.add_experimental_option('prefs', prefs)
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=chrome_options)
		driver.maximize_window()

		self.setUp(driver, datos)

	def setUp(self, driver, datos):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Mejorninez")
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ingresar"))).click()
		self.query(driver)


	def query(self, driver):
		cnx = sqlite3.connect('ApruebaConvenio.db')
		cursor = cnx.cursor()
		consulta  = " \
			SELECT \
				apruebaConvenio.* \
			FROM \
				apruebaConvenio \
			WHERE \
				Analisis = 'Pendiente' \
			LIMIT 1 \
		"
		query = pd.read_sql_query(consulta, cnx)
		print(query)



		for index, row in query.iterrows():
			print(row['Proyecto'])
			driver.get("https://a1.sis.mejorninez.cl/mod_proyectos/proyectoadjudicadoenejecucion.aspx?sw=4&codinst="+row['Proyecto'])
			time.sleep(3)
			#self.ingresar_Validacion(driver, datos)

			envioInformacion = Envio_Informacion()
			envioInformacion.envio_Informacion_by_name(driver, "txtNumResol", row['Resolucion']) # 1) Número de Resolución OK
			time.sleep(2)
			# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ddown003"))).click() # 2) Tipo de Resolución OK
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddown003']/option[2]"))).click()
			time.sleep(2)
			envioInformacion.envio_Informacion_by_name(driver, "txtFecResol", row['FechaResolucion']) # 3) Fecha de Resolución (VER FORMATO)
			time.sleep(2)




			envioInformacion.envio_Informacion_by_name(driver, "txtFecConvenio", row['FechaConvenio']) #****
			time.sleep(2)

			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ddown003"))).click() # 2) Tipo de Resolución OK
			time.sleep(2)
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddown003']/option[2]"))).click() # 2) Tipo de Resolución OK
			time.sleep(2)







			envioInformacion.envio_Informacion_by_name(driver, "txtFecInicio", row['FechaConvenio'])
			time.sleep(2)
			envioInformacion.envio_Informacion_by_name(driver, "txtFecTermino", "01-10-2024")
			time.sleep(2)
			envioInformacion.envio_Informacion_by_name(driver, "txtMateria", row['Materia'])
			time.sleep(2)
			envioInformacion.envio_Informacion_by_name(driver, "txtFecInicio", "01-10-2023")
			time.sleep(2)
			envioInformacion.envio_Informacion_by_name(driver, "txtCoberturas", row['Cobertura(N Plazas)'])



			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ddown008"))).click()
			time.sleep(2)
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddown008']/option[4]"))).click()
			time.sleep(2)


			time.sleep(330)





