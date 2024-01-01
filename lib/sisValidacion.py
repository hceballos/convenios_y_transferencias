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

class SisValidacion(Fuente):


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

	def databaseUpateSinRegistros(self, driver, datos, row, No_se_encontraron_registros):
		conexion = sqlite3.connect("proyectos.db")
		conexion.execute("UPDATE CodProyectos SET Estatus=?, Diferencia=?  WHERE CodProyecto=? and MesAtencion=?", (No_se_encontraron_registros, No_se_encontraron_registros, row['CodProyecto'], row['MesAtencion']))
		conexion.commit()
		conexion.close()
		#print("Table updated...... OK")
		print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'], " No se encontraron registros" )
		#print("No se encontraron registros")

		try:
			WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='lnkLimpiar']"))).click()
		except Exception as e:
			WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnkLimpiar"))).click()

		self.ingresar_Validacion(driver, datos)


	def __init__(self, json_path):
		Fuente.__init__(self, json_path)

		datos = self.datos

		options = Options()
		options.headless = True
		#driver = webdriver.Chrome(executable_path=datos['webdriver_path'], chrome_options=options)

		options.add_experimental_option('excludeSwitches', ['enable-logging'])


		driver = webdriver.Chrome(executable_path=datos['webdriver_path'])
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
		print("url : https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_ValidacionPagosExtra.aspx")
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_ValidacionPagosExtra.aspx")

		self.ingresar_Validacion(driver, datos)

	def ingresar_Validacion(self, driver, datos):
		driver.find_element_by_tag_name('body').send_keys(Keys.END) # Use send_keys(Keys.HOME) to scroll up to the top of page

		#Por Validar
		#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='rbtListEstado_1']"))).click()

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
		for index, row in query.iterrows():
			envioInforProyecto = Envio_Informacion()
			print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'] )
			#time.sleep(1)
			envioInforProyecto.envio_Informacion_by_name(driver, "txtPeriodoDesde", row['Mes Atención'])
			#time.sleep(0.5)
			envioInforProyecto.envio_Informacion_by_name(driver, "txtPeriodoHasta", row['Mes Atención'])

			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ddlTipoPago"))).click()

			# Tipo de Pago	80 Bis   : /option[2]
			# Tipo de Pago	URGENCIA : /option[3]
			if row['Tipo'] == '80 BIS':
				WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddlTipoPago']/option[2]"))).click()
			else: 
				WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ddlTipoPago']/option[3]"))).click()

			self.ingresar_proyecto(driver, datos, row, cnx)

		consulta  = " \
			SELECT \
				CodProyectos.* \
			FROM \
				CodProyectos \
		"
		query = pd.read_sql_query(consulta, cnx)


		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - Resumen Validados 80 Bis.xlsx', engine='xlsxwriter')
		query.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Todas las cuentas', index=False)
		writer.save()

	def ingresar_proyecto(self, driver, datos, row, cnx):
		# INPUT PROYECTO - LIMPIAR
		driver.find_element_by_xpath("//*[@id='I_ProyectoCodigo_txtCodigo']").clear()
		time.sleep(0.5)

		# INPUT PROYECTO
		envioInforProyecto = Envio_Informacion()
		envioInforProyecto.envio_Informacion_by_name(driver, "I_ProyectoCodigo$txtCodigo", row['Cod. Proyecto'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

		#time.sleep(3)

		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnBuscar']"))).click()
		#print( " btnBuscar")


		#time.sleep(4)

		#print(" Boton Buscar ")
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnBuscar"))).click()
		"""
		click = Click()
		click.click_by_id(driver, "btnBuscar")
		time.sleep(3)
		"""
		time.sleep(3)


		try:
			No_se_encontraron_registros = driver.find_element(By.XPATH, '//*[@id="lblAlertError"]').text
			if No_se_encontraron_registros == 'No se encontraron registros':
				#print("No se encontraron registros")
				self.databaseUpateSinRegistros(driver, datos, row, No_se_encontraron_registros)
		except Exception as e:
			self.continuar(driver, datos, row, cnx)


	def continuar(self, driver, datos, row, cnx):
		click = Click()
		click.click_by_id(driver, "GV_Pendientes_lblDetalle_0")
		time.sleep(1)
		#print("click_by_id - Solicitudes CDP pendientes de aprobar - Detalle")


		
		#print(">>>> 	Antecedentes Solicitud")
		#time.sleep(1)
		driver.find_element_by_tag_name('body').send_keys(Keys.END) # Use send_keys(Keys.HOME) to scroll up to the top of page


		#cdp = self.dato(driver, datos, row, cnx)

		# ===================================================================================
		#numero_CDP 	= self.envioInfoProyecto(driver, "txtNroCDP", row['Nº CDP'])
		#anio_CDP 		= self.envioInfoProyecto(driver, "txtFechaCDP", row['AÑO CDP'])
		#resolucion 	= self.envioInfoProyecto(driver, "txtNroRes", row['Resolución'])
		#fecha 			= self.envioInfoProyecto(driver, "txtFechaRes", row['Fecha'])
		#observacion 	= self.envioInfoProyecto(driver, "txtObservacionRes", row['OBSERVACION'])
		# ===================================================================================
		try:
			envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "txtNroCDP" )))
			envio.click()
			envio.clear()
			envio.send_keys(row['Nº CDP'])
			time.sleep(1)

		except Exception as e:
			time.sleep(1)
			#print("Exception >>>>>>>>>>>>>>", e)
			envioInforProyecto = Envio_Informacion()
			#print(">>>>		Nº CDP")
			envioInforProyecto.envio_Informacion_by_id(driver, "txtNroCDP", row['Nº CDP'])
			try:
				envioInforProyecto.envio_Informacion_by_id(driver, "txtNroCDP", row['Nº CDP'])
			except Exception as e:
				envioInforProyecto.envio_Informacion_by_id(driver, "txtNroCDP", row['Nº CDP'])



		# ===================================================================================
		try:
			#print(">>>>		AÑO CDP")


			envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "txtFechaCDP" )))
			envio.click()
			envio.clear()
			envio.send_keys(row['AÑO CDP'])
			time.sleep(1)



		except Exception as e:
			#print("Exception >>>>>>>>>>>>>>", e)
			#print(">>>>		AÑO CDP")
			envioInforProyecto.envio_Informacion_by_id(driver, "txtFechaCDP", row['AÑO CDP'])
		# ===================================================================================
		try:
			#print(">>>>		Resolución")

			envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "txtNroRes" )))
			envio.click()
			envio.clear()
			envio.send_keys(row['Resolución'])
			time.sleep(1)




		except Exception as e:
			#print("Exception >>>>>>>>>>>>>>", e)
			#print(">>>>		Resolución")
			envioInforProyecto.envio_Informacion_by_id(driver, "txtNroRes", row['Resolución'])
		# ===================================================================================
		try:
			#print(">>>>		FECHA")
			envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "txtFechaRes" )))
			envio.click()
			envio.clear()
			envio.send_keys(row['Fecha'])
			time.sleep(1)


		except Exception as e:
			#print("Exception >>>>>>>>>>>>>>", e)
			#print(">>>>		FECHA")
			envioInforProyecto.envio_Informacion_by_id(driver, "txtFechaRes", row['Fecha'])
		# ===================================================================================
		try:
			#print(">>>>		OBSERVACION")

			envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "txtObservacionRes" )))
			envio.click()
			envio.clear()
			envio.send_keys(row['OBSERVACION'])
			time.sleep(1)


		except Exception as e:
			#print("Exception >>>>>>>>>>>>>>", e)
			#print(">>>>		OBSERVACION")
			envioInforProyecto.envio_Informacion_by_id(driver, "txtObservacionRes", row['OBSERVACION'])
		# ===================================================================================

		#print(driver.page_source)

		#print("BASE DE DATOS : ", row['Monto Total'])
		Pago_Por_Reliquidacion	= driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[4]/tbody/tr[6]/td[4]').text
		Pago_Por_Reliquidacion = self.normalizeNumeric(Pago_Por_Reliquidacion)

		Mes_de_Atencion = driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[2]/tbody/tr[6]/td[1]').text
		#print("Mes_de_Atencion : ", Mes_de_Atencion)

		plazasAtendidas = driver.find_element(By.XPATH, '//*[@id="panel_Calculo"]/div[2]/table[4]/tbody/tr[6]/td[1]').text
		#print("plazasAtendidas : ", plazasAtendidas)

		#print(row['Monto Total'], type(row['Monto Total']), Pago_Por_Reliquidacion, type(Pago_Por_Reliquidacion))
		#Pago_Por_Reliquidacion = self.normalizeNumeric(Pago_Por_Reliquidacion)
		#print(row['Monto Total'], Pago_Por_Reliquidacion, type(Pago_Por_Reliquidacion))
		#print( int(row['Monto Total']), type(int(row['Monto Total'])) , " /// " , Pago_Por_Reliquidacion, type(Pago_Por_Reliquidacion))


		diferencia = int(int(Pago_Por_Reliquidacion) - int(row['Monto Total']) )
		print("diferencia : ", type(diferencia), diferencia)

		if int(diferencia) > 100:
			conexion = sqlite3.connect("proyectos.db")
			conexion.execute("UPDATE CodProyectos SET Estatus=?, Diferencia=?  WHERE CodProyecto=? and MesAtencion=?", ("Con Diferencia", str(diferencia), row['CodProyecto'], row['MesAtencion']))
			conexion.commit()
			conexion.close()
			#print("Table updated...... OK REGISTRA DIFERECIA Y CIERRA POP UP")
			print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'],  diferencia, " REGISTRA DIFERECIA Y CIERRA POP UP" )

			#time.sleep(10)

			# CERRAR VENTANA 
			try:
				click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='btnClosePop2']" )))
				click.click()
			except Exception as e:
				click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "btnClosePop2" )))
				click.click()

			self.ingresar_Validacion(driver, datos)

		# Urgencia
		#if int(diferencia) < 100 and str(row['Mes Atención']) == Mes_de_Atencion:

		# 80 bis
		if int(diferencia) < 100 and str(row['Mes Atención']) == Mes_de_Atencion and str(row['Plazas Atendidas']) == str(plazasAtendidas) :
			self.databaseUpate(driver, datos, row, diferencia)

		else:
			print(" ==================== DIFERENCIA NEGATIVA ============================ ")
			conexion = sqlite3.connect("proyectos.db")
			conexion.execute("UPDATE CodProyectos SET Estatus=?, Diferencia=?  WHERE CodProyecto=? and MesAtencion=?", ("Diferencia negativa", diferencia, row['CodProyecto'], row['MesAtencion']))
			conexion.commit()
			conexion.close()
			#print("Table updated...... ok - Sin diferencia")
			print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'], "Diferencia negativa" )


	def databaseUpate(self, driver, datos, row, diferencia):
		conexion = sqlite3.connect("proyectos.db")
		conexion.execute("UPDATE CodProyectos SET Estatus=?, Diferencia=?  WHERE CodProyecto=? and MesAtencion=?", ("ok", diferencia, row['CodProyecto'], row['MesAtencion']))
		conexion.commit()
		conexion.close()
		#print("Table updated...... ok - Sin diferencia")
		print("Processing Proyecto  : ", row['Cod. Proyecto'], " " ,row['Mes Atención'], " " , row['Tipo'], " " , row['Mes Atención'], " " , row['Plazas Atendidas'], " " , row['Monto Total'], " ok - Sin diferencia" )

		#time.sleep(4)


		try:
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='btnValidarCdp']")))
			click.click()
			#time.sleep(10)
		except Exception as e:
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "btnValidarCdp" )))
			click.click()
			#time.sleep(10)

		"""
		# limpiar
		try:
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='lnkLimpiar']")))
			click.click()
			time.sleep(10)
		except Exception as e:
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "lnkLimpiar" )))
			click.click()
			time.sleep(10)
		# limpiar


		# CERRAR VENTANA 
		try:
			#print("CERRAR ventanta - inicio")
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='btnClosePop2']" )))
			click.click()
			#print("CERRAR ventanta - fin")
			#time.sleep(4)
		except Exception as e:
			#print("CERRAR ventanta - inicio")
			click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "btnClosePop2" )))
			click.click()
			#print("CERRAR ventanta - fin")
			#time.sleep(4)
		# CERRAR VENTANA 


		print("CERRAR ventanta - fin")
		"""
		time.sleep(4)
		self.ingresar_Validacion(driver, datos)

	# =================================================================================================





