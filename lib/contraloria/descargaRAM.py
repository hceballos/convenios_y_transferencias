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
import codecs
import os
import pandas as pd
import re
import sqlite3
import sys
import time
import glob


class Descargas(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)

		datos = self.datos


		for f in glob.glob("C:\\Users\\hceballos\\Music\\desarrollo\\mejorninez\\output\\*Consolidado Retenciones*", recursive=True):
			print('Procesando  : ', f)


		descargas ={"PagosAprobados" : "\\input_excel\\calculoAFE\\PagosAprobados", "PagosRetenidos" : "\\input_excel\\calculoAFE\\PagosRetenidos"}
		for key in descargas.keys():
			chrome_options = webdriver.ChromeOptions()
			prefs = {
				'download.default_directory': os.path.join(os.getcwd()) +descargas[key] ,
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

			self.setUp(driver, datos, descargas[key] )

	def setUp(self, driver, datos, descargas):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Mejorninez")
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ingresar"))).click()
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Retenciones.aspx")

		self.ingresar_Validacion(driver, datos, descargas)

	def ingresar_Validacion(self, driver, datos, descargas):
		print("descargas : ", descargas)
		if "PagosAprobados" in descargas:
			self.descargar(driver, datos)
		else:
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='up_PresupuestoGeneral']/div[1]/div[1]/div/div/table/tbody/tr[6]/td/label[2]"))).click() 	# BOTON BUSCAR
			time.sleep(10)
			self.descargar(driver, datos)

	def descargar(self, driver, datos):
		WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='lnk_btn_buscar']"))).click() 	# BOTON BUSCAR
		time.sleep(10)

		WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='lnk_Descargar']"))).click() 	# BOTON BUSCAR	
		driver.find_element_by_tag_name('body').send_keys(Keys.END)														# Use send_keys(Keys.HOME) to scroll up to the top of page
		time.sleep(2)