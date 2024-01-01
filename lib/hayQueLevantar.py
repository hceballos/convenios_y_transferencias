#! /bin/env python3
import os
import sys
import codecs

from lib.elementos import Envio_Informacion
from lib.elementos import Click
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from lib.fuente import Fuente
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sqlite3
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from pandas.io.html import read_html

class SisLevantar(Fuente):

	def __init__(self, json_path, final):
		Fuente.__init__(self, json_path)

		datos = self.datos

		options = Options()
		options.headless = True
		driver = webdriver.Chrome(executable_path=datos['webdriver_path'])
		driver.maximize_window()

		self.setUp(driver, datos, final)

	def setUp(self, driver, datos, final):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

		self.login(driver, datos, final)

	def login(self, driver, datos, final):
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Nna05")

		click = Click()
		click.click_by_id(driver, "ingresar")

		time.sleep(1)
		print("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Retenciones.aspx")
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Retenciones.aspx")

		self.levantarRetencion(driver, datos, final)

	def levantarRetencion(self, driver, datos, final):
		print(" =========================== PAGINA ===========================")

		time.sleep(5)

		###WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "rbAprobados"))).click()

		#time.sleep(10)
		driver.find_element_by_tag_name('body').send_keys(Keys.END)
		time.sleep(3)


		tabla = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GV_pago"]/tbody')))

		#tabla = driver.find_element(By.XPATH, '//*[@id="GV_pago"]/tbody')

		linea = tabla.text.split("Detalle")


		#print("linea : ", linea, type(linea))

		#print(" ============================== final ======================================= ")
		#print(final)


		posicion =0
		for x in linea[:-1]:
			self.rowTable(driver, x, posicion, final)
			posicion +=1
		time.sleep(100)



	def rowTable(self, driver, x, posicion, final):
		for index, row in final.iterrows():
			#print( row['Código '], row['Periodo de Atención a Levantar o Retener'] )
			if row['COD PROYECTO'] in x:
				print(x," 	",posicion)
				#time.sleep(0.5)

				WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "GV_pago_chkRow_"+str(posicion)))).click()
			else:
				pass
			#posicion +=1




		#print("final ===================================================================== ")


		"""
		posicion =0
		for x in linea[:-1]:
			if ('1050829' in x) and ('201812' in x):
				print("> ", x, ">>>>>>>>", posicion)
				WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "GV_pago_chkRow_"+str(posicion)))).click()
			else:
				pass
			posicion +=1
		time.sleep(15)
		"""

		"""
		posicion =0
		for x in linea[:-1]:
			print("> ", x, ">>>>>>>>", posicion)
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "GV_pago_chkRow_"+str(posicion)))).click()
			posicion +=1
		time.sleep(15)
		"""
