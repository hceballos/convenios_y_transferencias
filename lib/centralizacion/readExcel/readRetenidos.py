import pandas as pd
import glob
from lib.centralizacion.database.database import Database
from lib.centralizacion.lineasAccion.Linea2401001.linea2401001 import Linea2401001
from lib.centralizacion.lineasAccion.Linea2401002.linea2401002 import Linea2401002
from lib.centralizacion.lineasAccion.Linea2401003.linea2401003 import Linea2401003
from lib.centralizacion.lineasAccion.Linea2401004.linea2401004 import Linea2401004
from lib.centralizacion.lineasAccion.Linea2401005.linea2401005 import Linea2401005
from lib.centralizacion.lineasAccion.Linea2401006.linea2401006 import Linea2401006

#from lib.centralizacion.lineasAccion.Linea2401003 import linea2401003
#from lib.centralizacion.lineasAccion.Linea2401004 import linea2401004
#from lib.centralizacion.lineasAccion.Linea2401005 import linea2401005
#from lib.centralizacion.lineasAccion.Linea2401006 import linea2401006
import re

class ReadRetenidos:

	def __init__(self, datos):
		self.datos = datos

		transferencias = pd.DataFrame()
		for f in glob.glob('./input_excel/centralizacion/retenidos/*.xlsx', recursive=True):
			print('Procesando  : ', f)
			transferencias_actual = pd.read_excel(f, converters={'uss': int, 'CUENTA': str, 'Costo NNA': int, 'COD PROYECTO': str, 'MES ATENCION': str, 'NroPlazas': int, 'MONTO LIQUIDO PAGADO': int, 'Monto Convenio 2021': int, 'Monto Fijo': int, 'Monto Variable': int, 'Factor USS': int} )
			#print("El número total de filas es:", len(transferencias_actual))			
			transferencias = transferencias.append(transferencias_actual, ignore_index=True)

		transferencias.rename(columns={'MES ATENCION': 'mes_atencion', 'ID TIPO PAGO': 'id_tipo_pago', 'TIPO PAGO': 'tipo_pago', 'FOLIO': 'folio', 'COD REGION': 'cod_region', 'COD PROYECTO': 'cod_proyecto', 'PROYECTO': 'proyecto', 'COD INSTITUCION': 'cod_institucion', 'INSTITUCION': 'institucion', 'DEPARTAMENTO SENAME': 'departamento_sename', 'TIPO SUBVENCION_DES': 'tipo_subvencion_des', 'TIPO PROYECTO_DES': 'tipo_proyecto_des', 'MODELO INTERVENCION': 'modelo_intervencion', 'BANCO': 'banco', 'CUENTA CORRIENTE NUMERO': 'cuenta_corriente_numero', 'RUT PROYECTO': 'rut_proyecto', 'MONTO MAXIMO PAGO': 'monto_maximo_pago', 'MONTO PAGO FIJO': 'monto_pago_fijo', 'MONTO PAGO VARIABLE': 'monto_pago_variable', 'MONTO POR ATENCION': 'monto_por_atencion', 'MONTO DEUDA': 'monto_deuda', 'MONTO RELIQUIDACION': 'monto_reliquidacion', 'MONTO RETENCION': 'monto_retencion', 'MONTO LIQUIDO PAGADO': 'monto_liquido_pagado', 'PLAZAS CONVENIDAS': 'plazas_convenidas', 'PLAZAS ATENDIDAS': 'plazas_atendidas', 'FACTOR FIJO': 'factor_fijo', 'FACTOR VARIABLE': 'factor_variable', 'FACTOR EDAD': 'factor_edad', 'FACTOR COBERTURA': 'factor_cobertura', 'FACTOR DISCAPACIDAD': 'factor_discapacidad', 'FACTOR COMPLEJIDAD': 'factor_complejidad', 'FACTOR CVF': 'factor_cvf', 'ASIGNACION ZONA': 'asignacion_zona', 'FACTOR USS': 'factor_uss', 'USS': 'uss', 'NUMERO PLAZAS': 'numero_plazas', 'NRO DIAS': 'nro_dias', 'FECHA CIERRE PAGO ': 'fecha_cierre_pago_', 'NUMERO RESOLUCION': 'numero_resolucion', 'FECHA CREACION': 'fecha_creacion', 'FECHA TERMINO': 'fecha_termino', 'NUMERO CDP': 'numero_cdp', 'ANNO PRESUPUESTARIO': 'anno_presupuestario', 'NUMERO RESOLUCION CDP': 'numero_resolucion_cdp', 'FECHA RESOLUCION CDP': 'fecha_resolucion_cdp', 'DESCRIPCION CDP': 'descripcion_cdp'}, inplace=True)
		transferencias['numero_mes'] = transferencias['mes_atencion'].apply(lambda x: str(x)[-2:] if pd.notnull(x) else None)

		columnas_fecha = ['fecha_cierre_pago_', 'fecha_creacion', 'fecha_termino']
		for columna in columnas_fecha:
			transferencias[columna] = pd.to_datetime(transferencias[columna]).dt.date

		transferencias.loc[transferencias['proyecto'].str.contains('OFICINA'), 'proyecto'] 	= 'OPD'
		transferencias.loc[transferencias['proyecto'].str.contains('ESCI'), 'proyecto'] 	= 'PEE'
		transferencias['modelox'] = transferencias['proyecto'].str.split(r'\s|-').str[0]

		cambios_de_nombre 				 = {'EMG': '2401004', 'CLA': '2401004', 'CPE': '2401004', 'DAM': '2401001', 'DCE': '2401001', 'FAE': '2401004', 'FAS': '2401004', 'FPA': '2401002', 'OPD': '2401006', 'PAD': '2401002','PAS': '2401002','PDC': '2401002','PDE': '2401002','PEC': '2401002','PEE': '2401002','PER': '2401003',  'PIB': '2401002', 'PIE': '2401002', 'PPC': '2401002', 'PPE': '2401003', 'PPF': '2401002', 'PRD': '2401003', 'PRE': '2401003', 'PRI': '2401005', 'PRM': '2401002','PRO': '2401003','RAD': '2401004','RDD': '2401004','RDG': '2401004','RDS': '2401004','REM': '2401004','REN': '2401004', 'RLP': '2401004', 'RMA': '2401004', 'RPA': '2401004', 'RPE': '2401004', 'RPF': '2401004', 'RPL': '2401004', 'RPM': '2401004', 'RPP': '2401004', 'RSP': '2401004', 'RVA': '2401004', 'RVT': '2401004'}
		transferencias['cuenta'] 		 = transferencias['modelox'].replace(cambios_de_nombre)
		transferencias['modificaciones'] = transferencias['folio'].str[-7]
		transferencias[['plazas_atendidas', 'factor_variable', 'asignacion_zona', 'numero_plazas', 'uss']] = transferencias[['plazas_atendidas', 'factor_variable', 'asignacion_zona', 'numero_plazas' ,'uss']].fillna(0)
		transferencias['uss'] 			 = transferencias['uss'].astype(int)		
		#print("El número total de filas es:", len(transferencias))


		database = Database()
		database.crear_retenidos(transferencias)


		# Linea2401001(transferencias[transferencias['cuenta'] == '2401001'])
		# Linea2401002(transferencias[transferencias['cuenta'] == '2401002'])
		# Linea2401003(transferencias[transferencias['cuenta'] == '2401003'])
		# Linea2401004(transferencias[transferencias['cuenta'] == '2401004'])
		# Linea2401005(transferencias[transferencias['cuenta'] == '2401005'])
		# Linea2401006(transferencias[transferencias['cuenta'] == '2401006'])


		"""
		mask01 = transferencias['cuenta'] == '2401001'
		transferencias.loc[mask01, 'Recalculado'] = (transferencias[mask01]['plazas_atendidas'] * transferencias[mask01]['factor_variable'] * (1 + transferencias[mask01]['asignacion_zona'] / 100) * transferencias[mask01]['uss']).round().astype(int)
		transferencias.loc[mask01, 'diferencia'] = transferencias[mask01]['monto_liquido_pagado'] - round(transferencias[mask01]['plazas_atendidas'] * transferencias[mask01]['factor_variable'] * (1 + transferencias[mask01]['asignacion_zona'] / 100.0) * transferencias[mask01]['uss'])
		

		#mask02 = transferencias['cuenta'] == '2401002'
		mask02 = (transferencias['cuenta'] == '2401002') & transferencias['tipo_pago'].str.contains('80 BIS')
		if any(transferencias.loc[mask02, 'tipo_pago'].str.contains('80 BIS').values):
			transferencias.loc[mask02, 'Recalculado'] = (transferencias[mask02]['numero_plazas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss']).round().astype(int)
			transferencias.loc[mask02, 'diferencia'] = transferencias[mask02]['monto_liquido_pagado'] - round((transferencias[mask02]['plazas_atendidas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss']))
		else:
			transferencias.loc[mask02, 'Recalculado'] = (transferencias[mask02]['plazas_atendidas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss']).round().astype(int)
			transferencias.loc[mask02, 'diferencia'] = transferencias[mask02]['monto_liquido_pagado'] - round((transferencias[mask02]['plazas_atendidas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss']))


		mask02 = (transferencias['cuenta'] == '2401002') & transferencias['tipo_pago'].str.contains('80 BIS')

		if any(mask02):
			print("SI ")
			transferencias.loc[mask02, 'Recalculado'] = "si"

			# transferencias.loc[mask02, 'Recalculado'] = ((transferencias[mask02]['numero_plazas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss'])).round().astype(int)
			# transferencias.loc[mask02, 'diferencia'] = transferencias[mask02]['monto_liquido_pagado'] - round((transferencias[mask02]['plazas_atendidas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss']))
		

		else:
			transferencias.loc[mask02, 'Recalculado'] = "else"
			# transferencias.loc[mask02, 'Recalculado'] = ((transferencias[mask02]['plazas_atendidas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss'])).round().astype(int)
			# transferencias.loc[mask02, 'diferencia'] = transferencias[mask02]['monto_liquido_pagado'] - round((transferencias[mask02]['plazas_atendidas'] * transferencias[mask02]['factor_variable'] * (1 + transferencias[mask02]['asignacion_zona'] / 100) * transferencias[mask02]['uss']))

		"""
		
		# nuevo_df = transferencias[transferencias['cuenta'] == '2401001']





		# print(nuevo_df)

		# Aplicar la condición y asignar valores a la columna 'Recalculado'
		# transferencias.loc[(transferencias['cuenta'] == '2401002') & (transferencias['tipo_pago'] == 'ANTICIPO'), 'Recalculado'] = 'ANTICIPO'
		# transferencias.loc[(transferencias['cuenta'] == '2401002') & (transferencias['tipo_pago'] == '80 BIS'), 'Recalculado'] = '80 BIS'
		# transferencias.loc[(transferencias['cuenta'] == '2401002') & (transferencias['tipo_pago'] == 'URGENCIA'), 'Recalculado'] = 'URGENCIA'
		# transferencias.loc[(transferencias['cuenta'] == '2401002') & (transferencias['tipo_pago'] == 'EMERGENCIA'), 'Recalculado'] = 'EMERGENCIA'
		# transferencias.loc[(transferencias['cuenta'] == '2401002') & (transferencias['tipo_pago'] == 'OTROS PAGOS'), 'Recalculado'] = 'OTROS PAGOS'




		# transferencias['Analisis']      = 'Pendiente'

		# database = Database()
		# database.crear_transferencias(nuevo_df)