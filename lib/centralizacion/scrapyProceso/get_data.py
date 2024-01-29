import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
import re
import platform
import time
import sqlite3
import re
import platform
import pandas as pd
import glob
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from PyPDF2 import PdfReader
from lib.fuente import Fuente
from lib.elementos import Envio_Informacion, Click
from sqlalchemy import create_engine, text

class Get_data():

	def __init__(self, driver, resultados):


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
			print("resultados Get_data FIN : ", resultados, len(resultados) )

			self.database_scrapy(df)

		self.actualiza_CodProyectos_Ok(resultados)



	def database_scrapy(self, df):
		try:
			engine = create_engine('sqlite:///contraloria.db')
		except Exception as e:
			print(f"Error al crear la conexión con la base de datos: {e}")
			return
		nombre_de_tabla = 'scrapy'

		try:
			existing_ids = pd.read_sql(f"SELECT ID_Pago FROM {nombre_de_tabla}", engine)['ID_Pago'].tolist()
		except Exception as e:
			print(f"Error al leer datos existentes desde la base de datos: {e}")
			return

		df_filtered = df[~df['ID_Pago'].isin(existing_ids)]
		try:
			df_filtered.to_sql(nombre_de_tabla, engine, index=False, if_exists='append')
		except Exception as e:
			print(f"Error al escribir en la base de datos: {e}")
			return



	def actualiza_CodProyectos_Ok(self, resultados):
		conexion = sqlite3.connect("contraloria.db")
		conexion.execute("UPDATE CodProyectos SET Analisis=? WHERE COD_PROYECTO=? and MES_ATENCION=?", ("OK", resultados[0][3], resultados[0][8]))
		conexion.commit()
		conexion.close()
		print("Table updated...... OK")
