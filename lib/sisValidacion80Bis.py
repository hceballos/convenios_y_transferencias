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

class SisValidacion80Bis(Fuente):


		# ===================================================================================
	def envioInfoProyecto(self, byID, numero):
		try:
			envioInforProyecto = Envio_Informacion()
			print(">>>>		Nº CDP")
			envioInforProyecto.envio_Informacion_by_id(driver, byID, numero)
		except Exception as e:
			envioInforProyecto = Envio_Informacion()
			print(">>>>		Nº CDP")
			envioInforProyecto.envio_Informacion_by_id(driver, byID, numero)

		# ===================================================================================
	def normalizeNumeric(self, string):
		string	= string.replace(".", "")
		x = pd.to_numeric(string)
		return int(x)

	def databaseUpateSinRegistros(self, driver, datos, row):
		conexion = sqlite3.connect("proyectos.db")
		conexion.execute("UPDATE CodProyectos SET Estatus=?, Diferencia=?  WHERE CodProyecto=? and MesAtencion=?", ("No se encontraron registros", "No se encontraron registros", row['CodProyecto'], row['MesAtencion']))
		conexion.commit()
		conexion.close()
		print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'], " No se encontraron registros" )

		try:
			WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='lnkLimpiar']"))).click()
		except Exception as e:
			WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnkLimpiar"))).click()

		self.ingresar_Validacion(driver, datos)

		# ===================================================================================
	def linkDetalle(self, driver, datos, row, cnx):
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "GV_Pendientes_lblDetalle_0"))).click() 		# BOTON DETALLE
		time.sleep(1)
		driver.find_element_by_tag_name('body').send_keys(Keys.END) 													# BAJAR EL SCROLL
		driver.find_element_by_tag_name('body').send_keys(Keys.ENTER) 													# TECLA ENTER

		return

		# ===================================================================================
	def extraeInformacion(self, driver, datos, row, cnx, num_rows):
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnValidarCdp")))		# esta disponible el boton de "Validar y enviar Pago"?
		driver.find_element_by_tag_name('body').send_keys(Keys.END)									# Scroll hacia abajo
		
		Proyecto		= driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[2]/tbody/tr[5]/td').text
		MesdeAtencion	= driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[2]/tbody/tr[6]/td[1]').text
		Convenidas		= self.normalizeNumeric(driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[4]/tbody/tr[6]/td[1]').text)
		MontoaPago		= self.normalizeNumeric(driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[4]/tbody/tr[6]/td[4]').text)

		print("__________________________________")
		#print("sentence" , 		row)
		print("__________________________________")
		print("Proyecto", 		Proyecto )
		print("MesdeAtencion", 	MesdeAtencion )
		print("Convenidas", 	Convenidas )
		print("MontoaPago", 	MontoaPago )
		print("__________________________________")

		self.analizaInformacion(driver, datos, row, cnx, Proyecto, MesdeAtencion, Convenidas, MontoaPago, num_rows)

	def analizaInformacion(self, driver, datos, row, cnx, Proyecto, MesdeAtencion, Convenidas, MontoaPago, num_rows):
		print("MontoaPago 				: ", MontoaPago)
		print("Row Monto Total 			: ", row['Monto Total'])
		diferenciaMonto = MontoaPago - row['Monto Total']
		print("diferenciaMonto 			: ", diferenciaMonto)

		print("Convenidas 				: ", Convenidas)
		print("Row Plazas Atendidas 			: ", row['Plazas Atendidas'])
		diferenciaPlazas = Convenidas - row['Plazas Atendidas']
		print("diferenciaPlazas 			: ", diferenciaPlazas)


		if str(row['Cod. Proyecto']) in Proyecto:
			print(">>>>>>>>>>> : if str(row['Cod. Proyecto']) in Proyecto:")
			if str(row['MesAtencion']) ==  MesdeAtencion:
				print(">>>>>>>>>>> : if str(row['MesAtencion']) ==  MesdeAtencion:")
				print("ANTES : if num_rows ==  1:", num_rows)
				if num_rows < 2:
					print("DESPUES : if num_rows ==  1:", num_rows)
					if row['Plazas Atendidas'] == Convenidas:
						print(">>>>>>>>>>>>>>>>>>>>>>>>>>> : ", MontoaPago - row['Monto Total'])
						if abs(MontoaPago - row['Monto Total']) < 100:
							print("abs(MontoaPago - row['Monto Total'])", abs(MontoaPago - row['Monto Total']))
							self.llenaInformacion(driver, datos, row, cnx)
							self.databaseUpate(driver, cnx, datos, row, "OK", "OK")
							WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnValidarCdp']"))).click()
							self.ingresar_Validacion(driver, datos)
						else:
							analisis = "Error en Monto a Pago"
							print(analisis)
							self.databaseUpate(driver, cnx, datos, row, analisis, diferenciaMonto)
							self.cerrarVentana(driver, datos, row, cnx)


					elif row['Plazas Atendidas'] < Convenidas:
						self.llenaInformacion(driver, datos, row, cnx)
						self.databaseUpate(driver, cnx, datos, row, "OK", "OK")
						WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnValidarCdp']"))).click()
						self.ingresar_Validacion(driver, datos)

					else:
						analisis = "Error en Plazas Atendidas"
						print(analisis)
						self.databaseUpate(driver, cnx, datos, row, analisis, diferenciaPlazas)
						self.cerrarVentana(driver, datos, row, cnx)
				else:
					analisis = "Pago en fraccion"
					print(analisis)
					self.databaseUpate(driver, cnx, datos, row, analisis, num_rows)
					self.cerrarVentana(driver, datos, row, cnx)
			else:
				analisis = "Error en Mes Atencion"
				print(analisis)
				#self.databaseUpate(driver, cnx, datos, row, analisis, "Mes no corresponde")
				self.cerrarVentana(driver, datos, row, cnx)
		else:
			analisis = "Error en Cod. Proyecto"
			print(analisis)
			#self.databaseUpate(driver, cnx, datos, row, analisis, "Proyecto no corresponde")
			self.cerrarVentana(driver, datos, row, cnx)

		# ===================================================================================
	def databaseUpate(self, driver, cnx, datos, row, analisis, diferencia):
		print("______________________ databaseUpate ________________________")
		cnx.execute("UPDATE CodProyectos SET Estatus=?, Diferencia=?  WHERE CodProyecto=? and MesAtencion=?", (analisis, str(diferencia), row['CodProyecto'], row['MesAtencion']))
		cnx.commit()
		cnx.close()
		print("Table updated...... OK")
		

		# ===================================================================================
	def llenaInformacion(self, driver, datos, row, cnx):
		a_dict = {'txtNroCDP': row['Nº CDP'], 'txtFechaCDP': row['AÑO CDP'], 'txtNroRes': row['Resolución'], 'txtFechaRes': row['Fecha'], 'txtObservacionRes': row['OBSERVACION']}

		for key in a_dict.keys():
			print(key, '->', a_dict[key])
			envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, key )))
			envio.click()
			envio.clear()
			envio.send_keys(a_dict[key])
		time.sleep(3)

		print("______________________ llenaInformacion ________________________")

		#self.cerrarVentana(driver, datos, row, cnx)

		# ===================================================================================
	def cerrarVentana(self, driver, datos, row, cnx):
		try:
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='btnClosePop2']" )))
			click.click()
		except Exception as e:
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "btnClosePop2" )))
			click.click()

		print("______________________ cerrarVentana ________________________")
		self.ingresar_Validacion(driver, datos)

		# ===================================================================================
	def plazasAtendidasSonMenoresPlazasConvenidas(self, driver, datos, row, cnx):
		self.llenaInformacion(driver, datos, row, cnx)
		self.databaseUpate(driver, cnx, datos, row, "OK", "OK")
		#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnValidarCdp']"))).click()
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnValidarCdp"))).click()
		time.sleep(3)

		self.ingresar_Validacion(driver, datos)

		# ===================================================================================

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
		#chrome_options.add_argument('--headless')
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
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_ValidacionPagosExtra.aspx")

		self.ingresar_Validacion(driver, datos)

	def ingresar_Validacion(self, driver, datos):
		driver.find_element_by_tag_name('body').send_keys(Keys.END) # Use send_keys(Keys.HOME) to scroll up to the top of page
		time.sleep(1)

		cnx = sqlite3.connect('proyectos.db')
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

		self.pendientes(cnx, query, driver, datos)

	def pendientes(self, cnx, query, driver, datos):

		driver.find_element_by_tag_name('body').send_keys(Keys.HOME) 													# SUBIR EL SCROLL


		for index, row in query.iterrows():
			envioInforProyecto = Envio_Informacion()
			print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'] )
			time.sleep(1.5)
			envioInforProyecto.envio_Informacion_by_name(driver, "txtPeriodoDesde", row['Mes Atención'])
			time.sleep(1.5)
			envioInforProyecto.envio_Informacion_by_name(driver, "txtPeriodoHasta", row['Mes Atención'])
			time.sleep(1.5)
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ddlTipoPago"))).click()
			time.sleep(1)
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddlTipoPago']/option[2]"))).click() 		# 80 Bis
			#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddlTipoPago']/option[3]"))).click()		# Urgencia

			self.ingresar_proyecto(driver, datos, row, cnx)

		# ===================================================================================
		cnx = sqlite3.connect('proyectos.db')
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
				and CodProyectos.'Estatus' != 'OK' \
			ORDER BY \
				CodProyectos.'Región' DESC, \
				CodProyectos.'Cod. Proyecto' ASC \
		"
		query = pd.read_sql_query(consulta, cnx)
		# self.pendientes(cnx, query, driver, datos)
		# =================================================================================== *************************** COMENTAR PARA GENERAR EL INFORME **********************************

		consulta  = " \
			SELECT CodProyectos.* FROM CodProyectos \
		"
		query = pd.read_sql_query(consulta, cnx)

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - Resumen Validados 80 Bis.xlsx', engine='xlsxwriter')
		query.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Todas las cuentas', index=False)
		writer.save()

	def ingresar_proyecto(self, driver, datos, row, cnx):

		try:
			driver.find_element_by_xpath("//*[@id='I_ProyectoCodigo_txtCodigo']").clear() # INPUT PROYECTO - LIMPIAR
			time.sleep(2.5)

			envioInforProyecto = Envio_Informacion()
			envioInforProyecto.envio_Informacion_by_name(driver, "I_ProyectoCodigo$txtCodigo", row['Cod. Proyecto']) 	# INPUT PROYECTO
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnBuscar']"))).click()		# BOTON BUSCAR	
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnBuscar"))).click()

		except Exception as e:
			driver.find_element_by_xpath("//*[@id='I_ProyectoCodigo_txtCodigo']").clear() # INPUT PROYECTO - LIMPIAR
			time.sleep(1)

			envioInforProyecto = Envio_Informacion()
			envioInforProyecto.envio_Informacion_by_name(driver, "I_ProyectoCodigo$txtCodigo", row['Cod. Proyecto']) 	# INPUT PROYECTO
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnBuscar']"))).click()		# BOTON BUSCAR	
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnBuscar"))).click()

		time.sleep(3)


		# Buscar todas las filas en la tabla
		rows = driver.find_elements_by_xpath("//*[@id='GV_Pendientes']") # //*[@id="GV_Pendientes_lblDetalle_0"] 

		# Contar el número de filas
		num_rows = len(rows)
		#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> El número de filas en la tabla es:", num_rows)



		try:
			No_se_encontraron_registros = driver.find_element(By.XPATH, '//*[@id="lblAlertError"]').text
			if No_se_encontraron_registros == 'No se encontraron registros':
				self.databaseUpateSinRegistros(driver, datos, row)
		except Exception as e:
			self.linkDetalle(driver, datos, row, cnx)
			self.extraeInformacion(driver, datos, row, cnx, num_rows)

			print(" ==================== FIN ====================")

		# ================================================================================================================================

