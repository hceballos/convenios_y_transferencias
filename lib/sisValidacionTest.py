#! /bin/env python3
import time
import sys
import sqlite3
import re
import pandas as pd
import os
import codecs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from lib.fuente import Fuente
from lib.elementos import Envio_Informacion
from lib.elementos import Click
from datetime import date

class SisValidacionTest(Fuente):


	def driver(self, datos):
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

		return driver

		# ===================================================================================
	def setUp(self, driver, datos):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

		envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "usuario" )))
		envio.click()
		envio.clear()
		envio.send_keys("hceballos@mejorninez.cl")

		envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "password" )))
		envio.click()
		envio.clear()
		envio.send_keys("Nna06")

		click = Click()
		click.click_by_id(driver, "ingresar")

		time.sleep(1)
		#print("url : https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_ValidacionPagosExtra.aspx")
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_ValidacionPagosExtra.aspx")

		# ===================================================================================
	def readDataBase(self, driver, datos, cnx):
		driver.find_element_by_tag_name('body').send_keys(Keys.END) # Use send_keys(Keys.HOME) to scroll up to the top of page
		consulta  = " \
			SELECT \
				CodProyectos.'Mes Atención', \
				CodProyectos.'Región', \
				CodProyectos.'Cod. Proyecto', \
				CodProyectos.'Monto Total', \
				CodProyectos.'Nº CDP', \
				CodProyectos.'AÑO CDP', \
				CodProyectos.'Resolución', \
				CodProyectos.'Fecha', \
				CodProyectos.'OBSERVACION', \
				CodProyectos.'Tipo', \
				CodProyectos.'CodProyecto', \
				CodProyectos.'MesAtencion', \
				CodProyectos.'Estatus', \
				CodProyectos.'Plazas Atendidas' \
			FROM \
				CodProyectos \
			WHERE \
				CodProyectos.'Tipo' = '80 BIS' \
				and CodProyectos.'Estatus' = 'Pendiente' \
			ORDER BY \
				CodProyectos.'Región' DESC, \
				CodProyectos.'Cod. Proyecto' ASC \
			LIMIT 1 \
		"
		query = pd.read_sql_query(consulta, cnx)
		return query

		# ===================================================================================
	def busqueda(self, driver, datos, row):
		envioInforProyecto = Envio_Informacion()
		print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'] )

		envioInforProyecto.envio_Informacion_by_name(driver, "I_ProyectoCodigo$txtCodigo", row['Cod. Proyecto'])					# Proyecto
		driver.find_element_by_name("I_ProyectoCodigo$txtCodigo").send_keys(Keys.ENTER)
		time.sleep(2)				

		i = 0
		while i < 2:
			envioInforProyecto.envio_Informacion_by_name(driver, "txtPeriodoDesde", row['Mes Atención'])							# Mes Atención
			envioInforProyecto.envio_Informacion_by_name(driver, "txtPeriodoHasta", row['Mes Atención'])							# Mes Atención
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ddlTipoPago"))).click()								# Tipo de Pago
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddlTipoPago']/option[2]"))).click()		# 80 Bis
			time.sleep(1)
			i += 1

		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnBuscar']"))).click()						# Buscar
		time.sleep(3)
		driver.find_element_by_tag_name('body').send_keys(Keys.END)	
		# ===================================================================================

	def databaseUpDateSinRegistros(self, driver, datos, row, cnx):
		cnx.execute("UPDATE CodProyectos SET Estatus=?, Diferencia=?  WHERE CodProyecto=? and MesAtencion=?", ("No se encontraron registros", "No se encontraron registros", row['CodProyecto'], row['MesAtencion']))
		cnx.commit()
		cnx.close()
		print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'], "Table updated...... OK - ", "No se encontraron registros" )
		
		try:
			WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='lnkLimpiar']"))).click()
		except Exception as e:
			WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnkLimpiar"))).click()

		#self.readDataBase(driver, datos, cnx)

		# ===================================================================================


	def __init__(self, json_path):
		Fuente.__init__(self, json_path)

		datos = self.datos

		driver = self.driver(datos)
		self.setUp(driver, datos)
		cnx = sqlite3.connect('proyectos.db')
		query = self.readDataBase(driver, datos, cnx)
		print(len(query), query)


		if len(query) == 1:
			for index, row in query.iterrows():
				self.busqueda(driver, datos, row)
				try:
					No_se_encontraron_registros = driver.find_element(By.XPATH, '//*[@id="lblAlertError"]').text 										# No se encontraron registros
					if No_se_encontraron_registros == 'No se encontraron registros':
						print("No se encontraron registros")
						self.databaseUpDateSinRegistros(driver, datos, row, cnx)
						#time.sleep(10)
				except:
					self.analizaInformacion(driver, datos, row, cnx)																					# si hay informacion
				else:				
					self.busqueda(driver, datos, row)
		else:
			consulta  = " \
				SELECT CodProyectos.* FROM CodProyectos \
			"
			query = pd.read_sql_query(consulta, cnx)

			today = date.today()
			writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - TEEESSSSSSTTTT Resumen Validados 80 Bis.xlsx', engine='xlsxwriter')
			query.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Todas las cuentas', index=False)
			writer.save()



	def analizaInformacion(self, driver, datos, row, cnx):

			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "GV_Pendientes_lblDetalle_0"))).click()								# Click en Detalle
			driver.find_element_by_tag_name('body').send_keys(Keys.END)

			try:
				self.extraeInformacion(driver, datos, row)
			except Exception as e:
				self.extraeInformacion(driver, datos, row)


	def extraeInformacion(self, driver, datos, row):

			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnValidarCdp")))													# esta disponible el boton de "Validar y enviar Pago"?
		
			Proyecto	= driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[2]/tbody/tr[5]/td').text
			print("Proyecto", 	Proyecto )

			MesdeAtencion	= driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[2]/tbody/tr[6]/td[1]').text
			print("MesdeAtencion", 	MesdeAtencion )

			PlazasaPago	= driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[4]/tbody/tr[6]/td[1]').text
			print("PlazasaPago", 	PlazasaPago )

			MontoaPago	= driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[4]/tbody/tr[6]/td[4]').text
			print("MontoaPago", 	MontoaPago )
			driver.find_element_by_tag_name('body').send_keys(Keys.END)																				# Scroll hacia abajo

			print("sentence" , row)


			if str(row['Cod. Proyecto']) in Proyecto:
				print("Si existe Cod. Proyecto")
			else:
				print("No existe Cod. Proyecto")

			if str(row['MesAtencion']) in MesdeAtencion:
				print("Si existe MesAtencion", row['MesAtencion'], type(str(row['MesAtencion'])), MesdeAtencion, type(MesdeAtencion) )
			else:
				print("No existe MesAtencion")

			if str(row['Plazas Atendidas']) in PlazasaPago:
				print("Si existe Plazas Atendidas", row['Plazas Atendidas'], type(str(row['Plazas Atendidas'])), PlazasaPago, type(PlazasaPago) )
			else:
				print("No existe Plazas Atendidas")





				time.sleep(10)

	# =================================================================================================





