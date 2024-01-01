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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import datetime

class SisDescargasPagosAprobados(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		chrome_options = webdriver.ChromeOptions()
		prefs = {
			'download.default_directory': 'C:\\Users\\hceballos\\Music\\desarrollo\\mejorninez\\input_excel\\retencionesLevantamientos\\pagosAprobados',
			"download.prompt_for_download": False,
			"download.directory_upgrade": True,
			"safebrowsing_for_trusted_sources_enabled": False,
			"safebrowsing.enabled": False
		}
		chrome_options.add_experimental_option('prefs', prefs)
		driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=chrome_options)
		driver.maximize_window()

		self.setUp(driver, datos)

	def setUp(self, driver, datos):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

		self.login(driver, datos)

	def login(self, driver, datos):
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Nna05")

		click = Click()
		click.click_by_id(driver, "ingresar")

		time.sleep(1)
		print("url : https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Retenciones.aspx")
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Retenciones.aspx")

		self.ingresar_Validacion(driver, datos)

	def ingresar_Validacion(self, driver, datos):
		print("Descarga Pagos aprobados")
		WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnk_btn_buscar"))).click()
		WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnk_Descargar"))).click()
		time.sleep(5)
		driver.quit()


class SisDescargasPagosRetenidos(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		chrome_options = webdriver.ChromeOptions()
		prefs = {
			'download.default_directory': 'C:\\Users\\hceballos\\Music\\desarrollo\\mejorninez\\input_excel\\retencionesLevantamientos\\pagosRetenidos',
			"download.prompt_for_download": False,
			"download.directory_upgrade": True,
			"safebrowsing_for_trusted_sources_enabled": False,
			"safebrowsing.enabled": False
		}
		chrome_options.add_experimental_option('prefs', prefs)
		driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=chrome_options)
		driver.maximize_window()

		self.setUp(driver, datos)

	def setUp(self, driver, datos):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

		self.login(driver, datos)

	def login(self, driver, datos):
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Nna05")

		click = Click()
		click.click_by_id(driver, "ingresar")

		time.sleep(1)
		print("url : https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Retenciones.aspx")
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Retenciones.aspx")

		self.ingresar_Validacion(driver, datos)

	def ingresar_Validacion(self, driver, datos):
		print("Descarga retenidos")
		WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "rbRetenidos"))).click()
		time.sleep(5)
		WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnk_Descargar"))).click()
		time.sleep(5)
		driver.quit()



class SisDescargasTransferencias(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		chrome_options = webdriver.ChromeOptions()
		prefs = {
			'download.default_directory': 'C:\\Users\\hceballos\\Music\\desarrollo\\mejorninez\\input_excel\\retencionesLevantamientos\\transferencias',
			"download.prompt_for_download": False,
			"download.directory_upgrade": True,
			"safebrowsing_for_trusted_sources_enabled": False,
			"safebrowsing.enabled": False
		}
		chrome_options.add_experimental_option('prefs', prefs)
		driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=chrome_options)
		driver.maximize_window()

		self.setUp(driver, datos)

	def setUp(self, driver, datos):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

		self.login(driver, datos)

	def login(self, driver, datos):
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Nna05")

		click = Click()
		click.click_by_id(driver, "ingresar")

		time.sleep(1)
		print("url : https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Transferencias.aspx")
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_Transferencias.aspx")

		self.ingresar_Validacion(driver, datos)

	def ingresar_Validacion(self, driver, datos):
		print("Transferencias")

		anio = str(datetime.datetime.today().year)
		mes = str(datetime.datetime.today().month-1)
		print(anio+mes, " 	", anio+mes)


		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "txtPeriodo", anio+mes)
		click = Click()
		click.click_by_id(driver, "ingresar")


		time.sleep(5)
		click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "lnk_btn_buscar")))
		click.click()




		time.sleep(5)
		WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnk_Descargar"))).click()
		time.sleep(5)

		driver.quit()