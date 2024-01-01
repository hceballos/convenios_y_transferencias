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


class AnalisisRetenidos(Fuente):

	def to_Excel(self):
		cnx = sqlite3.connect('AnalisisRetenidos.db')
		consulta  = " \
			SELECT \
				scrapy.* \
			FROM \
				scrapy \
		"
		query = pd.read_sql_query(consulta, cnx)

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("%b-%d-%Y")+' - Analisis Retenidos Report 80 BIS.xlsx', engine='xlsxwriter')
		query.to_excel(writer, sheet_name='Todas las cuentas')
		writer.save()


	def database(self, df):
		engine = create_engine('sqlite:///AnalisisRetenidos.db')
		nombre_de_tabla = 'scrapy'
		existing_ids = pd.read_sql(f"SELECT ID_Pago FROM {nombre_de_tabla}", engine)['ID_Pago'].tolist()
		df_filtered = df[~df['ID_Pago'].isin(existing_ids)]
		df_filtered.to_sql(nombre_de_tabla, engine, index=False, if_exists='append')

	def get_data(self, driver, datos, resultados):
		print("resultados : ", resultados, len(resultados) )
		for i in range(0, len(resultados)):
			print("i : ", i)
			time.sleep(3.5)

			link_xpath = "//*[@id='GV_pago_lblPeriodo_" + str(i) + "']"
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, link_xpath))).click()  # LINK DETALLE
			time.sleep(3.5)

			page_source = driver.page_source
			diccionario = {

				# FACTORES DE PAGO
				"Factor_Numero_Plaza"					: r'(?<=id="UC_DetallePago_lblNumeroPlaza" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Fijo"							: r'(?<=id="UC_DetallePago_lblFactorFijo" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Edad"							: r'(?<=id="UC_DetallePago_lblFactorEdad" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Discapacidad"					: r'(?<=id="UC_DetallePago_lblFactorDiscapacidad" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_CVF"							: r'(?<=id="UC_DetallePago_lblFactorCVF" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Tipo_USS"						: r'(?<=id="UC_DetallePago_lblFactorUSS" class="form-control input-sm">).*?(?=<\/span>)',

				"Factor_Dias_del_Mes"					: r'(?<=id="UC_DetallePago_lblDiasMes" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Factor_Variable"				: r'(?<=id="UC_DetallePago_lblFactorVariable" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Cobertura"						: r'(?<=id="UC_DetallePago_lblFactorCobertura" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Complejidad"					: r'(?<=id="UC_DetallePago_lblFactorComplejidad" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_Porcentaje_Zona"				: r'(?<=id="UC_DetallePago_lblPorcentajeZona" class="form-control input-sm">).*?(?=<\/span>)',
				"Factor_USS"							: r'(?<=id="UC_DetallePago_lblUSS" class="form-control input-sm">).*?(?=<\/span>)',


	
	
	



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

				#"Sobre_Atencion_Plazas"					: r'(?<=id="UC_DetallePago_lblPlazasSobreA" class="form-control input-sm">).*?(?=<\/span>)',							
				#"Sobre_Atencion_Monto_a_Pago_fijo"		: r'(?<=id="UC_DetallePago_lblMontoFijoSobreA" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_Monto_a_Pago_variable"	: r'(?<=id="UC_DetallePago_lblMontoVariableSobreA" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_Monto_a_Pago_total"		: r'(?<=id="UC_DetallePago_lblMontoTotalSobreA" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_NRO"					: r'(?<=id="UC_DetallePago_lblCDPnroSobrea" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_ANIO"					: r'(?<=id="UC_DetallePago_lblCDPanoSobrea" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_resolucion_pago"		: r'(?<=id="UC_DetallePago_lblResolPagoSA" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_fecha"					: r'(?<=id="UC_DetallePago_lblFechaPagoSA" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_Observacion"			: r'(?<=id="UC_DetallePago_lblObservCDPSA" class="form-control input-sm- text-uppercase">).*?(?=<\/textarea>)',
				#"Sobre_Atencion_Estado_CDP"				: r'(?<=id="UC_DetallePago_lblEstadoCDPSA" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_Estado_Transferencia"	: r'(?<=id="UC_DetallePago_lblEstadoTransfSA1" class="form-control input-sm">).*?(?=<\/span>)',
				#"Sobre_Atencion_Fecha_Transferencia"	: r'(?<=id="UC_DetallePago_lblFechaTransf80SA" class="form-control input-sm">).*?(?=<\/span>)',
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

			data_merged = {}
			for d in dataFinal:
				data_merged.update(d)

			df = pd.DataFrame([data_merged])

			data_merged = {}
			for d in dataFinal:
				data_merged.update(d)
			df = pd.DataFrame([data_merged])

			for index, row in df.iterrows():
				print(index, row)

			driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
			self.database(df)



	def tablaPagos(self, driver, datos):
		print("# =============================== ===================================================")
		print("ENTRANDO EN DETALLE 1")
		time.sleep(3.5)
		try:
			tabla = driver.find_element_by_xpath('//*[@id="GV_pago"]/tbody')
			filas = tabla.find_elements_by_tag_name('tr')
			time.sleep(1)
		except Exception as e:
			tabla = driver.find_element_by_xpath('//*[@id="GV_pago"]/tbody')
			filas = tabla.find_elements_by_tag_name('tr')
			time.sleep(1)
		print("ENTRANDO EN DETALLE 2")
		tabla = driver.find_element_by_xpath('//*[@id="GV_pago"]/tbody')
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
		self.get_data(driver, datos, resultados)

	def query(self, driver, datos):
		driver.find_element_by_tag_name('body').send_keys(Keys.HOME) # Use send_keys(Keys.HOME) to scroll up to the top of page
		cnx = sqlite3.connect('AnalisisRetenidos.db')
		cursor = cnx.cursor()
		consulta  = " \
			SELECT \
				CodProyectos.'MES_ATENCION', \
				CodProyectos.'COD_PROYECTO', \
				CodProyectos.'unico' \
			FROM \
				CodProyectos \
			WHERE \
				Analisis = 'Pendiente' \
			ORDER BY \
				CodProyectos.'MES_ATENCION' DESC \
			LIMIT 1 \
		"
		query = pd.read_sql_query(consulta, cnx)
		print(query)

		try:
			
			unico_value = query['unico'].iloc[0]  # obten el primer valor de la serie
			update_query = f"""
				UPDATE CodProyectos
				SET Analisis = 'OK'
				WHERE unico = {unico_value}
			"""
			cursor.execute(update_query)
			cnx.commit()

			cursor.close()
			cnx.close()
			print("Actualización exitosa de la tabla CodProyectos.")

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
				print("BOTON BUSCAR 1")
				WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnBuscarPagos"))).click() # BOTON BUSCAR
				time.sleep(2.5)
				print("BOTON BUSCAR 2")


				self.tablaPagos(driver, datos)	
		except IndexError:
			self.to_Excel()



	def login(self, driver, datos):
		envioInformacion = Envio_Informacion()
		envioInformacion.envio_Informacion_by_name(driver, "usuario", "hceballos@mejorninez.cl")
		envioInformacion.envio_Informacion_by_name(driver, "password", "Mejorninez")
		click = Click()
		click.click_by_id(driver, "ingresar")
		time.sleep(1)
		driver.get("https://a1.sis.mejorninez.cl/mod_financiero/Pagos/wf_InformePagos.aspx")

	def setUp(self, datos):
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
		chrome_options.add_argument('--headless')  # Ejecutar Chrome en modo sin cabeza
		chrome_options.add_argument('--disable-gpu')  # Deshabilitar aceleración por hardware
		chrome_options.add_argument('--no-sandbox')  # Ejecutar sin el sandbox
		chrome_options.add_argument('--disable-dev-shm-usage')  # Evitar problemas de memoria compartida

		driver = webdriver.Chrome(executable_path=datos['webdriver_path'], options=chrome_options)
		driver.maximize_window()
		
		driver.switch_to.window(driver.window_handles[0])
		driver.get(datos['url_mejorninez'])
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
		return driver

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
 
		datos = self.datos
		driver = self.setUp(datos)
		self.login(driver, datos)

		contador = 0
		while contador < 5:
			self.query(driver, datos)



		time.sleep(5)