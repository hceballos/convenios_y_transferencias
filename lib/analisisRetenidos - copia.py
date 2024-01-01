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
import time
import re
import sqlite3
import pandas as pd
from selenium.webdriver.common.keys import Keys
from datetime import date
import io
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, String, MetaData, insert, update
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AnalisisRetenidos(Fuente):
 
	def eliminar_y_convertir(self, cadena):
		cadena_sin_simbolos = cadena.replace("$", "").replace(".", "")
		try:
			entero = int(cadena_sin_simbolos)
			return entero
		except ValueError:
			print("La cadena no se puede convertir a un número entero.")
			return None
 
	def login(self, driver, datos):
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Nna06")
 
		click = Click()
		click.click_by_id(driver, "ingresar")
 
		time.sleep(1)
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_InformePagos.aspx")
 
	def setUp(self, driver, datos):
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
 
	def extrae_info(self, cnx, query, driver, datos, clave, valor, row):
		elemento = []
		while len(elemento) < 1:
			valor = driver.find_element(By.ID, valor).text
			elemento.append(valor)
			time.sleep(0.5)
		time.sleep(0.5)
 
		return {clave : valor}
 
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
		#chrome_options.add_argument('--headless')  # Ejecutar Chrome en modo sin cabeza
		chrome_options.add_argument('--disable-gpu')  # Deshabilitar aceleración por hardware
		chrome_options.add_argument('--no-sandbox')  # Ejecutar sin el sandbox
		chrome_options.add_argument('--disable-dev-shm-usage')  # Evitar problemas de memoria compartida
 
		driver = webdriver.Chrome(executable_path=datos['webdriver_path'], options=chrome_options)
		driver.maximize_window()
 
		self.setUp(driver, datos)
		self.login(driver, datos)
		self.ingresar_Datos(driver, datos)
 
	def ingresar_Datos(self, driver, datos):
 
		driver.find_element_by_tag_name('body').send_keys(Keys.HOME) # Use send_keys(Keys.HOME) to scroll up to the top of page
 
		cnx = sqlite3.connect('AnalisisRetenidos.db')
		consulta  = " \
			SELECT \
				CodProyectos.'MES_ATENCION', \
				CodProyectos.'COD_PROYECTO', \
				CodProyectos.'unico' \
			FROM \
				CodProyectos \
			WHERE \
				TIPO_PAGO = '80 BIS' \
				and Analisis = 'Pendiente' \
				and CAST(Mes_Atencion AS INTEGER) > 202111 \
			ORDER BY \
				CodProyectos.'MES_ATENCION' DESC \
			LIMIT 1 \
		"
		# and Mes_Atencion LIKE '2023%' \
		query = pd.read_sql_query(consulta, cnx)
		print(query)
 
		for index, row in query.iterrows():
			envioInforProyecto = Envio_Informacion()
			time.sleep(1.5)
			envioInforProyecto.envio_Informacion_by_name(driver, "txtPeriodo", row['MES_ATENCION'])
			time.sleep(1.5)
			try:
				envioInforProyecto.envio_Informacion_by_name(driver, "I_ProyectoCodigo$txtCodigo", row['COD_PROYECTO'])
			except Exception as e:
				envioInforProyecto.envio_Informacion_by_name(driver, "I_ProyectoCodigo$txtCodigo", row['COD_PROYECTO'])
			#envioInforProyecto.envio_Informacion_by_name(driver, "I_ProyectoCodigo$txtCodigo", row['COD_PROYECTO'])
			time.sleep(1.5)
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnBuscarPagos"))).click() # BOTON BUSCAR
			time.sleep(2.5)
			self.tablaPagos(cnx, query, driver, datos, row)
 
		self.ingresar_Datos(driver, datos)

	def tablaPagos(self, cnx, query, driver, datos, row):
		print("# =============================== ===================================================")



		tiempo_espera = 10
		try:
			tabla = WebDriverWait(driver, tiempo_espera).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="GV_pago"]/tbody')))
			filas = tabla.find_elements_by_tag_name('tr')
			time.sleep(2)
		except Exception as e:
			tabla = WebDriverWait(driver, tiempo_espera).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="GV_pago"]/tbody')))
			filas = tabla.find_elements_by_tag_name('tr')
			time.sleep(1)
 
		tabla = WebDriverWait(driver, tiempo_espera).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="GV_pago"]/tbody')))
		filas = tabla.find_elements_by_tag_name('tr')
		time.sleep(1)

		informacion = []
		for fila in filas:
			columnas = fila.find_elements_by_tag_name('td')
			datos_fila = []
			for columna in columnas:
				datos_fila.append(columna.text)
			informacion.append(datos_fila)
		resultados = [sublista for sublista in informacion if len(sublista) > 0]
 
		for i in range(0, len(resultados)):
			link_xpath = "//*[@id='GV_pago_lblPeriodo_" + str(i) + "']"
 
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, link_xpath))).click()  # LINK DETALLE
			time.sleep(3)
 
			page_source = driver.page_source
			diccionario = {
 
				# ATENCION Y MONTOS
 
				"Tipo_de_Pago"							: r'(?<=id="UC_DetallePago_lblTipoPago" class="form-control input-sm">).*?(?=<\/span>)',
				"Plazas_Convenidas"						: r'(?<=id="UC_DetallePago_lblPlazasConvenida" class="form-control input-sm">).*?(?=<\/span>)',
				"Plazas_Atendidas"						: r'(?<=id="UC_DetallePago_lblPlazasAtendidas" class="form-control input-sm">).*?(?=<\/span>)',
				"Plazas_Normales_Atendidas"				: r'(?<=id="UC_DetallePago_lblPlazasNormAten" class="form-control input-sm">).*?(?=<\/span>)',
				"Dias_Atendidos"						: r'(?<=id="UC_DetallePago_lblDiasAtendidos" class="form-control input-sm">).*?(?=<\/span>)',
				"Liquido_Pagado"						: r'(?<=id="UC_DetallePago_lblLiquidoPagar" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Convenido_Fijo"					: r'(?<=id="UC_DetallePago_lblMontoConvFijo" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Convenido_Variable"				: r'(?<=id="UC_DetallePago_lblMontoConvVariable" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Convenido_Total"					: r'(?<=id="UC_DetallePago_llblMontoConvTotal" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Atencion_Fijo"					: r'(?<=id="UC_DetallePago_lblMontoAtencionFijo" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Atencion_Variable"				: r'(?<=id="UC_DetallePago_lblMontoAtencionVariable" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Atencion_Total"					: r'(?<=id="UC_DetallePago_lblMontoAtencionTotal" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Normal_Fijo"						: r'(?<=id="UC_DetallePago_lblMontoNormalFijo" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Normal_Variable"					: r'(?<=id="UC_DetallePago_lblMontoNormalVariable" class="form-control input-sm">).*?(?=<\/span>)',
				"Monto_Normal_Total"					: r'(?<=id="UC_DetallePago_lblMontoNormalTotal" class="form-control input-sm">).*?(?=<\/span>)',
				"Nro_dias_Mes"							: r'(?<=id="UC_DetallePago_lblNroDiasMes" class="form-control input-sm">).*?(?=<\/span>)',
				"Estado"								: r'(?<=id="UC_DetallePago_lblEstadoPago" class="form-control input-sm">).*?(?=<\/span>)',
 
				# PAGO EXTRAORDINARIO
 
				"Urgencia_Plazas"						: r'(?<=id="UC_DetallePago_lblPlazasUrg" class="form-control input-sm">).*?(?=<\/span>)',							
				"Urgencia_Monto_a_Pago_fijo"			: r'(?<=id="UC_DetallePago_lblMontoFijoUrg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_Monto_a_Pago_variable"		: r'(?<=id="UC_DetallePago_lblMontoVariableUrg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_Monto_a_Pago_total"			: r'(?<=id="UC_DetallePago_lblMontoTotalUrg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_NRO"							: r'(?<=id="UC_DetallePago_lblCDPnroUrg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_ANIO"							: r'(?<=id="UC_DetallePago_lblCDPanoUrg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_resolucion_pago"				: r'(?<=id="UC_DetallePago_lblResolPagoUrg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_fecha"						: r'(?<=id="UC_DetallePago_lblFechaPagoUrg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_Observacion"					: r'(?<=id="UC_DetallePago_lblObservCDPUrg" class="form-control input-sm- text-uppercase">).*?(?=<\/textarea>)',
				"Urgencia_Estado_CDP"					: r'(?<=id="UC_DetallePago_lblEstadoCDPURG" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_Estado_Transferencia"			: r'(?<=id="UC_DetallePago_lblEstadoTransfurg" class="form-control input-sm">).*?(?=<\/span>)',
				"Urgencia_Fecha_Transferencia"			: r'(?<=id="UC_DetallePago_lblFechaTransfUrg" class="form-control input-sm">).*?(?=<\/span>)',
 
				"80B_Bis_Plazas"						: r'(?<=id="UC_DetallePago_lblPlazas80bis1" class="form-control input-sm">).*?(?=<\/span>)',							
				"80B_Bis_Monto_a_Pago_fijo"				: r'(?<=id="UC_DetallePago_lblMontoFijo80bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_Monto_a_Pago_variable"			: r'(?<=id="UC_DetallePago_lblMontoVariable80bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_Monto_a_Pago_total"			: r'(?<=id="UC_DetallePago_lblMontoTotal80bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_NRO"							: r'(?<=id="UC_DetallePago_lblCDPnro80bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_ANIO"							: r'(?<=id="UC_DetallePago_lblCDPano80bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_resolucion_pago"				: r'(?<=id="UC_DetallePago_lblResolPago80bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_fecha"							: r'(?<=id="UC_DetallePago_lblFechaPago80Bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_Observacion"					: r'(?<=id="UC_DetallePago_lblObservCDP80bis" class="form-control input-sm- text-uppercase">).*?(?=<\/textarea>)',
				"80B_Bis_Estado_CDP"					: r'(?<=id="UC_DetallePago_lblEstadoCDP80bis" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_Estado_Transferencia"			: r'(?<=id="UC_DetallePago_lblEstadoTransf80bis1" class="form-control input-sm">).*?(?=<\/span>)',
				"80B_Bis_Fecha_Transferencia"			: r'(?<=id="UC_DetallePago_lblFechaTransf80bis" class="form-control input-sm">).*?(?=<\/span>)',
 
				"Sobre_Atencion_Plazas"					: r'(?<=id="UC_DetallePago_lblPlazasSobreA" class="form-control input-sm">).*?(?=<\/span>)',							
				"Sobre_Atencion_Monto_a_Pago_fijo"		: r'(?<=id="UC_DetallePago_lblMontoFijoSobreA" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_Monto_a_Pago_variable"	: r'(?<=id="UC_DetallePago_lblMontoVariableSobreA" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_Monto_a_Pago_total"		: r'(?<=id="UC_DetallePago_lblMontoTotalSobreA" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_NRO"					: r'(?<=id="UC_DetallePago_lblCDPnroSobrea" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_ANIO"					: r'(?<=id="UC_DetallePago_lblCDPanoSobrea" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_resolucion_pago"		: r'(?<=id="UC_DetallePago_lblResolPagoSA" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_fecha"					: r'(?<=id="UC_DetallePago_lblFechaPagoSA" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_Observacion"			: r'(?<=id="UC_DetallePago_lblObservCDPSA" class="form-control input-sm- text-uppercase">).*?(?=<\/textarea>)',
				"Sobre_Atencion_Estado_CDP"				: r'(?<=id="UC_DetallePago_lblEstadoCDPSA" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_Estado_Transferencia"	: r'(?<=id="UC_DetallePago_lblEstadoTransfSA1" class="form-control input-sm">).*?(?=<\/span>)',
				"Sobre_Atencion_Fecha_Transferencia"	: r'(?<=id="UC_DetallePago_lblFechaTransf80SA" class="form-control input-sm">).*?(?=<\/span>)',
			}
 

			data = [ 
				{"ID_Pago"			: resultados[i][0]},
				{"Region"			: resultados[i][1]},
				{"Fecha_Pago"		: resultados[i][2]},
				{"Cod_Proyecto"		: resultados[i][3]},
				{"Nombre_Proyecto"	: resultados[i][4]},
				{"Monto"			: resultados[i][5]},
				{"Estado" 			: resultados[i][6]},
				{"Plazas"			: resultados[i][7]},
				{"Mes_Atencion"		: resultados[i][8]},
				{"Folio"			: resultados[i][9]},
				{"80B_Bis_Plazas_Analisis" : 'Pendiente'},
				{"80B_Bis_Monto_a_Pago_fijo_Analisis" : 'Pendiente'},
				{"80B_Bis_Monto_a_Pago_variable_Analisis" : 'Pendiente'},
				{"80B_Bis_Monto_a_Pago_total_Analisis" : 'Pendiente'},
			]

			#print(data)

 
			data1 = []
			for clave, valor in diccionario.items():
				resultado1 = re.search(valor, page_source)
				if resultado1:
					cadena = resultado1.group(0)
					if '$' in cadena or '.' in cadena:
						try:
							numero = int(cadena.replace('$', '').replace('.', ''))
							data1.append({clave: int(numero)})
						except ValueError:
							data1.append({clave: None})
					else:
						data1.append({clave: cadena})
				else:
					data1.append({clave: None})
 
			dataFinal = []
			dataFinal.extend(data)
			dataFinal.extend(data1)
 
			print("dataFinal : ", dataFinal)
			print(" ")
 
			data_merged = {}
			for d in dataFinal:
				data_merged.update(d)
 
			df = pd.DataFrame([data_merged])
 
			data_merged = {}
			for d in dataFinal:
				data_merged.update(d)
			df = pd.DataFrame([data_merged])
 
			#dataFinal['80B_Bis_Plazas_Analisis'] = 'Pendiente'
			#dataFinal['80B_Bis_Monto_a_Pago_fijo_Analisis'] = 'Pendiente'
			#dataFinal['80B_Bis_Monto_a_Pago_variable_Analisis'] = 'Pendiente'
			#dataFinal['80B_Bis_Monto_a_Pago_total_Analisis'] = 'Pendiente'
 
 
			metadata = MetaData()
			data_table = Table('data_table', metadata,
								Column('ID_Pago', String),
								Column('Region', String),
								Column('Fecha_Pago', String),
								Column('Cod_Proyecto', String),
								Column('Nombre_Proyecto', String),
								Column('Monto', String),
								Column('Estado', String),
								Column('Plazas', String),
								Column('Mes_Atencion', String),
								Column('Folio', String),
								Column('Tipo_de_Pago', String),
								Column('Plazas_Convenidas', String),
								Column('Plazas_Atendidas', String),
								Column('Plazas_Normales_Atendidas', String),
								Column('Dias_Atendidos', String),
								Column('Liquido_Pagado', String),
								Column('Monto_Convenido_Fijo', String),
								Column('Monto_Convenido_Variable', String),
								Column('Monto_Convenido_Total', String),
								Column('Monto_Atencion_Fijo', String),
								Column('Monto_Atencion_Variable', String),
								Column('Monto_Atencion_Total', String),
								Column('Monto_Normal_Fijo', String),
								Column('Monto_Normal_Variable', String),
								Column('Monto_Normal_Total', String),
								Column('Nro_dias_Mes', String),
								Column('Estado', String),
								Column('Urgencia_Plazas', String),
								Column('Urgencia_Monto_a_Pago_fijo', String),
								Column('Urgencia_Monto_a_Pago_variable', String),
								Column('Urgencia_Monto_a_Pago_total', String),
								Column('Urgencia_NRO', String),
								Column('Urgencia_ANIO', String),
								Column('Urgencia_resolucion_pago', String),
								Column('Urgencia_fecha', String),
								Column('Urgencia_Observacion', String),
								Column('Urgencia_Estado_CDP', String),
								Column('Urgencia_Estado_Transferencia', String),
								Column('Urgencia_Fecha_Transferencia', String),
								Column('80B_Bis_Plazas', String),
								Column('80B_Bis_Monto_a_Pago_fijo', String),
								Column('80B_Bis_Monto_a_Pago_variable', String),
								Column('80B_Bis_Monto_a_Pago_total', String),
								Column('80B_Bis_NRO', String),
								Column('80B_Bis_ANIO', String),
								Column('80B_Bis_resolucion_pago', String),
								Column('80B_Bis_fecha', String),
								Column('80B_Bis_Observacion', String),
								Column('80B_Bis_Estado_CDP', String),
								Column('80B_Bis_Estado_Transferencia', String),
								Column('80B_Bis_Fecha_Transferencia', String),
								Column('Sobre_Atencion_Plazas', String),
								Column('Sobre_Atencion_Monto_a_Pago_fijo', String),
								Column('Sobre_Atencion_Monto_a_Pago_variable', String),
								Column('Sobre_Atencion_Monto_a_Pago_total', String),
								Column('Sobre_Atencion_NRO', String),
								Column('Sobre_Atencion_ANIO', String),
								Column('Sobre_Atencion_resolucion_pago', String),
								Column('Sobre_Atencion_fecha', String),
								Column('Sobre_Atencion_Observacion', String),
								Column('Sobre_Atencion_Estado_CDP', String),
								Column('Sobre_Atencion_Estado_Transferencia', String),
								Column('Sobre_Atencion_Fecha_Transferencia', String),
								Column('80B_Bis_Plazas_Analisis', String),
								Column('80B_Bis_Monto_a_Pago_fijo_Analisis', String),
								Column('80B_Bis_Monto_a_Pago_variable_Analisis', String),
								Column('80B_Bis_Monto_a_Pago_total_Analisis', String)
					)
 
			engine = create_engine('sqlite:///AnalisisRetenidos.db')
			metadata.create_all(engine)
 
			combined_dict = {}
			for diccionario in dataFinal:
				combined_dict.update(diccionario)
 
			CodProyectos = Table('CodProyectos', metadata,
						Column('id', String, primary_key=True),
						Column('Analisis', String),
						#Column('FOLIO', String))
						Column('ID_Pago', String))

 
			"""
			if int(combined_dict['Plazas_Convenidas']) < int(combined_dict['Plazas_Atendidas']):
				menor = int(combined_dict['Plazas_Convenidas'])
			else:
				menor = int(combined_dict['Plazas_Atendidas'])
			print("La variable menor es:", menor)
 
 
			print( "80B_Bis_Plazas : ", int(combined_dict['80B_Bis_Plazas']) )
			print( "Monto_Convenido_Fijo : ", int(combined_dict['Monto_Convenido_Fijo']) )
			print( "Plazas_Convenidas : ", (combined_dict['Plazas_Convenidas']) )
			print( "Plazas_Convenidas new : ", plazas_convenidas )
			"""
 
			plazas_convenidas 			= int(combined_dict['Plazas_Convenidas']) if combined_dict['Plazas_Convenidas'] else 0
			Monto_Convenido_Fijo 		= int(combined_dict['Monto_Convenido_Fijo']) if combined_dict['Monto_Convenido_Fijo'] else 0
			Monto_Convenido_Variable 	= int(combined_dict['Monto_Convenido_Variable']) if combined_dict['Monto_Convenido_Variable'] else 0
			Monto_Convenido_Total 		= int(combined_dict['Monto_Convenido_Total']) if combined_dict['Monto_Convenido_Total'] else 0
 
			print("plazas_convenidas : ", plazas_convenidas)
			print("Monto_Convenido_Fijo : ", Monto_Convenido_Fijo)
			print("Monto_Convenido_Variable : ", Monto_Convenido_Variable)
			print("Monto_Convenido_Total : ", Monto_Convenido_Total)
 
			#combined_dict['80B_Bis_Monto_a_Pago_fijo_Analisis'] 	= int( Monto_Convenido_Fijo		/ plazas_convenidas) * int(combined_dict['80B_Bis_Plazas'])
			#combined_dict['80B_Bis_Monto_a_Pago_variable_Analisis'] = int( Monto_Convenido_Variable	/ plazas_convenidas) * int(combined_dict['80B_Bis_Plazas'])
			#combined_dict['80B_Bis_Monto_a_Pago_total_Analisis'] 	= int( Monto_Convenido_Total	/ plazas_convenidas) * int(combined_dict['80B_Bis_Plazas'])

			print("combined_dict : ", combined_dict)
 
			conn = sqlite3.connect('AnalisisRetenidos.db')
			cursor = conn.cursor()
 
			cursor.execute("SELECT * FROM data_table WHERE ID_Pago = ?", (df['ID_Pago'][0],))
			resultado = cursor.fetchone()
 
			# Verificar si se encontró el dato
			if resultado is not None:
				print(" ================= El dato "+df['ID_Pago'][0]+" está en la tabla. ================= ")
			else:
				print(" ================= El dato "+df['ID_Pago'][0]+" NO está en la tabla, se agrega ahora ================= ")
				# ======== INSERTAR LINEA ========
				with engine.connect() as connection:
					connection.execute(data_table.insert().values(combined_dict))
				engine.dispose()
				# ======== INSERTAR LINEA ========
			conn.close()
 
			# ======== ACTUALIZAR OK ========
			with engine.connect() as connection:
				update_query = update(CodProyectos).where(CodProyectos.c.unico == row['unico']).values(Analisis='ok')
				connection.execute(update_query)
			engine.dispose()
			# ======== ACTUALIZAR OK ========