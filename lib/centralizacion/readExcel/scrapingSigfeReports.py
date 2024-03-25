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
import platform
from lib.centralizacion.readExcel.readDisponibilidadRequerimientosPresupuestarios import ReadDisponibilidadRequerimientosPresupuestarios
from lib.centralizacion.readExcel.readDisponibilidadCompromisoPresupuestarios import ReadDisponibilidadCompromisoPresupuestarios
from lib.centralizacion.readExcel.readDisponibilidadDevengoPresupuestarios import ReadDisponibilidadDevengoPresupuestarios


class ScrapingSigfeReports(object):

	def getMac(self):
		chrome_options = webdriver.ChromeOptions()
		prefs = {
			'download.default_directory': '/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/centralizacion/sigfe/',
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

		self.datos = datos
		sistema_operativo = platform.system()
		if sistema_operativo == 'Darwin':
			print("Estás utilizando un sistema Mac")
			driver = self.getMac()
		elif sistema_operativo == 'Windows':
			print("Estás utilizando un sistema Windows.")
		self.setUp(driver, datos)

	def setUp(self, driver, datos):
		fecha_desde = "2023-01-01"
		fecha_hasta = "2023-12-31"
		ejercicio   = "2023"
		coberturas = ["2111001", "2111002", "2111003", "2111004", "2111005", "2111006", "2111007", "2111008", "2111009", "2111010", "2111011", "2111012", "2111013", "2111014", "2111015", "2111016", "2111017"]

		for i in range(1):
			print(f"Iteración {i + 1}")

			#self.devengo(driver, datos, fecha_desde, fecha_hasta, ejercicio, coberturas)
			self.compromiso(driver, datos, fecha_desde, fecha_hasta, ejercicio, coberturas)
			#self.requerimiento(driver, datos, fecha_desde, fecha_hasta, ejercicio, coberturas)

		ReadDisponibilidadRequerimientosPresupuestarios(datos)
		ReadDisponibilidadCompromisoPresupuestarios(datos)
		ReadDisponibilidadDevengoPresupuestarios(datos)

	def devengo(self, driver, datos, fecha_desde, fecha_hasta, ejercicio, coberturas):
		i = 0
		for cobertura in coberturas:
			driver.execute_script("window.open('');")
			ResultadoBusqueda = driver.switch_to.window(driver.window_handles[i])
			urlDestino = "https://asin.sigfe.gob.cl/jasperserver-pro/flow.html?_flowId=viewReportFlow&reportUnit=/SIGFE2/Reportes/SB_DisponibilidadDevengoPresupuestario&pp=u=hceballos2111&fecha_desde="+fecha_desde+"&ejercicio="+ejercicio+"&codigo_moneda=CLP&TITLESUBTITULOREPORTE="+ cobertura +"%20Direcci%C3%B3n%20Nacional&TITLETIPOMONEDAREPORTE=Gasto%20-%20Nacional&TITLETITULOREPORTE=Disponibilidad%20de%20Devengos%20Presupuestarios&ambiente=SIGFE2&codigo_presupuesto=02&fecha_hasta="+fecha_hasta+"&unidad_ejecutora="+ cobertura +"&ambiente=SIGFE2&site=SB&standAlone=true&decorate=no&readOnly=true&userLocale=es"
			driver.get(urlDestino)
			i += 1
		time.sleep(10)


	def compromiso(self, driver, datos, fecha_desde, fecha_hasta, ejercicio, coberturas):
		i = 0
		for cobertura in coberturas:
			driver.execute_script("window.open('');")
			ResultadoBusqueda = driver.switch_to.window(driver.window_handles[i])
			urlDestino = "https://asin.sigfe.gob.cl/jasperserver-pro/flow.html?_flowId=viewReportFlow&reportUnit=/SIGFE2/Reportes/SB_ListadoDisponibilidadCompromiso&pp=u=hceballos2111&fecha_desde="+fecha_desde+"&ejercicio="+ejercicio+"&codigo_moneda=CLP&TITLESUBTITULOREPORTE="+ cobertura +"%20Direcci%C3%B3n%20Nacional&TITLETIPOMONEDAREPORTE=Gasto%20-%20Nacional&TITLETITULOREPORTE=Disponibilidad%20de%20Compromiso%20Presupuestarios&ambiente=SIGFE2&codigo_presupuesto=02&fecha_hasta="+fecha_hasta+"&unidad_ejecutora="+ cobertura +"&ambiente=SIGFE2&site=SB&standAlone=true&decorate=no&readOnly=true&userLocale=es"
			driver.get(urlDestino)
			i += 1
			time.sleep(10)
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "export"))).click()
			time.sleep(2)
			#WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "menuList_simpleAction_16"))).click()


		time.sleep(10)


	def requerimiento(self, driver, datos, fecha_desde, fecha_hasta, ejercicio, coberturas):
		i = 0
		for cobertura in coberturas:
			driver.execute_script("window.open('');")
			ResultadoBusqueda = driver.switch_to.window(driver.window_handles[i])
			urlDestino = "https://sb.sigfe.gob.cl/jasperserver-pro/flow.html?_flowId=viewReportFlow&reportUnit=/SIGFE2/Reportes/SB_ListadoDisponibilidadRequerimiento&pp=u=hceballos2111&fecha_desde="+fecha_desde+"&ejercicio="+ejercicio+"&codigo_moneda=CLP&TITLESUBTITULOREPORTE="+ cobertura +"%20Direcci%C3%B3n%20Nacional&TITLETITULOREPORTE=Disponibilidad%20de%20Requerimientos%20Presupuestarios&ambiente=SIGFE2&codigo_presupuesto=02&fecha_hasta="+fecha_hasta+"&unidad_ejecutora="+ cobertura +"&ambiente=SIGFE2&site=SB&standAlone=true&decorate=no&readOnly=true&userLocale=es"
			driver.get(urlDestino)
			i += 1
		time.sleep(10)
