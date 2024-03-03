import pandas as pd
import glob
from lib.centralizacion.database.database import Database
from lib.centralizacion.lineasAccion.Linea2401001.linea2401001 import Linea2401001
from lib.centralizacion.lineasAccion.Linea2401002.linea2401002 import Linea2401002
from lib.centralizacion.lineasAccion.Linea2401003.linea2401003 import Linea2401003
from lib.centralizacion.lineasAccion.Linea2401004.linea2401004 import Linea2401004
from lib.centralizacion.lineasAccion.Linea2401005.linea2401005 import Linea2401005
from lib.centralizacion.lineasAccion.Linea2401006.linea2401006 import Linea2401006
import re
from datetime import date
#from lib.centralizacion.lineasAccion.Linea2401 import Linea2401


class ReadTransferencias:

	def calculate_estandar_monto(self, df, cuenta, tipo_pago, modelox, numero_plazas=False):
		filtro = (df['cuenta'] == cuenta) & (df['tipo_pago'] == tipo_pago) & (df['modelox'] == modelox)
		indice_filas = df[filtro].index
		
		# Y		plazas_convenidas
		# Z		plazas_atendidas
		# AA	factor_fijo
		# AB	factor_variable
		# AC	factor_edad
		# AD	factor_cobertura
		# AE	factor_discapacidad
		# AF	factor_complejidad
		# AG	factor_cvf
		# AH	asignacion_zona
		# AI	factor_uss
		# AJ	uss
		# AK	numero_plazas

		for indice_fila in indice_filas:
			if df.at[indice_fila, 'numero_plazas'] == 0:
				df.at[indice_fila, 'Estandar Monto Fijo'] 		= f"=AA{indice_fila}*(1+AD{indice_fila}+AH{indice_fila}+AG{indice_fila})*AJ{indice_fila}*BC{indice_fila}"
				df.at[indice_fila, 'Estandar Monto Variable']	= f"=AB{indice_fila}*(1+AC{indice_fila}+AF{indice_fila}+AE{indice_fila}+AE{indice_fila})*AJ{indice_fila}*AK{indice_fila}"
			else:
				df.at[indice_fila, 'Estandar Monto Fijo'] 		= f"=AA{indice_fila}*(1+AD{indice_fila}+AH{indice_fila}+AG{indice_fila})*AJ{indice_fila}*BC{indice_fila}"
				df.at[indice_fila, 'Estandar Monto Variable'] 	= f"=AB{indice_fila}*(1+AC{indice_fila}+AF{indice_fila}+AE{indice_fila}+AE{indice_fila})*AJ{indice_fila}*BC{indice_fila}"

			df.at[indice_fila, 'Estandar Monto Total'] 	= f"=BD{indice_fila} + BE{indice_fila}"
			df.at[indice_fila, 'Estandar Diferencia'] 	= f"=X{indice_fila} - BF{indice_fila}"

		df.reset_index(drop=True, inplace=True)
		df.index += 2
		
		return df


	def __init__(self, datos):
		#self.datos = datos

		transferencias = pd.DataFrame()
		for f in glob.glob('./input_excel/centralizacion/transferencias/*.xlsx', recursive=True):
			print('Procesando  : ', f)
			transferencias_actual = pd.read_excel(f, converters={'uss': int, 'CUENTA': str, 'Costo NNA': int, 'COD PROYECTO': str, 'MES ATENCION': str, 'NroPlazas': int, 'MONTO LIQUIDO PAGADO': int, 'Monto Convenio 2021': int, 'Monto Fijo': int, 'Monto Variable': int, 'Factor USS': int} )
			#print("El número total de filas es:", len(transferencias_actual))			
			transferencias = transferencias.append(transferencias_actual, ignore_index=True)


		transferencias.rename(columns={'MES ATENCION': 'mes_atencion', 'ID TIPO PAGO': 'id_tipo_pago', 'TIPO PAGO': 'tipo_pago', 'FOLIO': 'folio', 'COD REGION': 'cod_region', 'COD PROYECTO': 'cod_proyecto', 'PROYECTO': 'proyecto', 'COD INSTITUCION': 'cod_institucion', 'INSTITUCION': 'institucion', 'DEPARTAMENTO SENAME': 'departamento_sename', 'TIPO SUBVENCION_DES': 'tipo_subvencion_des', 'TIPO PROYECTO_DES': 'tipo_proyecto_des', 'MODELO INTERVENCION': 'modelo_intervencion', 'BANCO': 'banco', 'CUENTA CORRIENTE NUMERO': 'cuenta_corriente_numero', 'RUT PROYECTO': 'rut_proyecto', 'MONTO MAXIMO PAGO': 'monto_maximo_pago', 'MONTO PAGO FIJO': 'monto_pago_fijo', 'MONTO PAGO VARIABLE': 'monto_pago_variable', 'MONTO POR ATENCION': 'monto_por_atencion', 'MONTO DEUDA': 'monto_deuda', 'MONTO RELIQUIDACION': 'monto_reliquidacion', 'MONTO RETENCION': 'monto_retencion', 'MONTO LIQUIDO PAGADO': 'monto_liquido_pagado', 'PLAZAS CONVENIDAS': 'plazas_convenidas', 'PLAZAS ATENDIDAS': 'plazas_atendidas', 'FACTOR FIJO': 'factor_fijo', 'FACTOR VARIABLE': 'factor_variable', 'FACTOR EDAD': 'factor_edad', 'FACTOR COBERTURA': 'factor_cobertura', 'FACTOR DISCAPACIDAD': 'factor_discapacidad', 'FACTOR COMPLEJIDAD': 'factor_complejidad', 'FACTOR CVF': 'factor_cvf', 'ASIGNACION ZONA': 'asignacion_zona', 'FACTOR USS': 'factor_uss', 'USS': 'uss', 'NUMERO PLAZAS': 'numero_plazas', 'NRO DIAS': 'nro_dias', 'FECHA CIERRE PAGO ': 'fecha_cierre_pago_', 'NUMERO RESOLUCION': 'numero_resolucion', 'FECHA CREACION': 'fecha_creacion', 'FECHA TERMINO': 'fecha_termino', 'NUMERO CDP': 'numero_cdp', 'ANNO PRESUPUESTARIO': 'anno_presupuestario', 'NUMERO RESOLUCION CDP': 'numero_resolucion_cdp', 'FECHA RESOLUCION CDP': 'fecha_resolucion_cdp', 'DESCRIPCION CDP': 'descripcion_cdp'}, inplace=True)
		# transferencias['numero_mes'] = transferencias['mes_atencion'].apply(lambda x: str(x)[-2:] if pd.notnull(x) else None)
		transferencias['numero_mes'] = transferencias['mes_atencion'].apply(lambda x: '01' if pd.notnull(x) and str(x)[-2:] == '12' else f"{int(str(x)[-2:]) + 1:02d}" if pd.notnull(x) else None)
		transferencias.dropna(subset=['proyecto'], inplace=True)



		columnas_fecha = ['fecha_cierre_pago_', 'fecha_creacion', 'fecha_termino']
		for columna in columnas_fecha:
			transferencias[columna] = pd.to_datetime(transferencias[columna]).dt.date



		transferencias.loc[transferencias['proyecto'].str.contains('OFICINA'), 'modelox'] 	= 'OPD'
		transferencias.loc[transferencias['proyecto'].str.contains('ESCI'), 'modelox'] 	= 'PEE'
		transferencias['modelox'] = transferencias['proyecto'].str.split(r'\s|-').str[0]

		cambios_de_nombre 				 		= {'EMG': '2401004', 'PF': '2401003', 'AFT': '2401002', 'CLA': '2401004', 'CPE': '2401004', 'DAM': '2401001', 'DCE': '2401001', 'FAE': '2401004', 'FAS': '2401004', 'FPA': '2401002', 'OPD': '2401006', 'PAD': '2401002','PAS': '2401002','PDC': '2401002','PDE': '2401002','PEC': '2401002','PEE': '2401002','PER': '2401003',  'PIB': '2401002', 'PIE': '2401002', 'PPC': '2401002', 'PPE': '2401003', 'PPF': '2401002', 'PRD': '2401003', 'PRE': '2401003', 'PRI': '2401005', 'PRM': '2401002','PRO': '2401003','RAD': '2401004','RDD': '2401004','RDG': '2401004','RDS': '2401004','REM': '2401004','REN': '2401004', 'RLP': '2401004', 'RMA': '2401004', 'RPA': '2401004', 'RPE': '2401004', 'RPF': '2401004', 'RPL': '2401004', 'RPM': '2401004', 'RPP': '2401004', 'RSP': '2401004', 'RVA': '2401004', 'RVT': '2401004'}
		transferencias['cuenta'] 		 		= transferencias['modelox'].replace(cambios_de_nombre)
		transferencias['modificaciones'] 		= transferencias['folio'].str[-7]
		transferencias[['plazas_atendidas', 'factor_variable', 'asignacion_zona', 'numero_plazas', 'uss']] = transferencias[['plazas_atendidas', 'factor_variable', 'asignacion_zona', 'numero_plazas' ,'uss']].fillna(0)
		transferencias['uss'] 			 		= transferencias['uss'].astype(int)
		transferencias['plazas_convenidas']		= transferencias['plazas_convenidas'].astype(int)		
		transferencias['plazas_atendidas']		= transferencias['plazas_atendidas'].astype(int)
		transferencias['factor_fijo']			= transferencias['factor_fijo'].astype(float)		
		transferencias['asignacion_zona'] 		= transferencias['asignacion_zona'] / 100
		transferencias['factor_cobertura']		= transferencias['factor_cobertura'] / 100
		transferencias['factor_cvf']			= transferencias['factor_cvf'] / 100
		transferencias['factor_edad']			= transferencias['factor_edad'] / 100
		transferencias['factor_complejidad']	= transferencias['factor_complejidad'] / 100
		transferencias['factor_discapacidad']	= transferencias['factor_discapacidad'] / 100

		#transferencias['factor_variable']		= transferencias['factor_variable'] / 100
		#transferencias['factor_variable']		= transferencias['factor_variable']


		# Reemplazar comas por puntos en la columna 'factor_discapacidad'

		#columnas = ['factor_fijo', 'factor_variable', 'factor_complejidad', 'asignacion_zona']
		
		#print(transferencias.columns)
		#nuevo_orden_columnas = ['cuenta', 'tipo_pago', 'modelox', 'factor_fijo', 'factor_cobertura', 'asignacion_zona', 'factor_cvf', 'factor_uss', 'numero_plazas', 'Monto Fijo', 'nueva_columna']
		#df = df[nuevo_orden_columnas]
		# Iterar sobre las columnas y aplicar la transformación
		#for columna in columnas:
		#	transferencias[columna] = transferencias[columna].str.replace(',', '.')


		# Convertir las columnas relevantes a tipo numérico
		transferencias['factor_fijo'] = pd.to_numeric(transferencias['factor_fijo'], errors='coerce')
		transferencias['factor_cobertura'] = pd.to_numeric(transferencias['factor_cobertura'], errors='coerce')
		transferencias['asignacion_zona'] = pd.to_numeric(transferencias['asignacion_zona'], errors='coerce')
		transferencias['factor_cvf'] = pd.to_numeric(transferencias['factor_cvf'], errors='coerce')
		transferencias['factor_uss'] = pd.to_numeric(transferencias['factor_uss'], errors='coerce')
		transferencias['plazas_atendidas'] = pd.to_numeric(transferencias['plazas_atendidas'], errors='coerce')


		#for valor in transferencias['factor_discapacidad']:
		#	print(valor)

		# Realizar la operación de división
		#transferencias['factor_discapacidad'] 	= transferencias['factor_discapacidad'] / 100

		#transferencias['factor_discapacidad']	= transferencias['factor_discapacidad'] / 100
		transferencias['factor_uss']			= transferencias['factor_uss']
		#transferencias['factor_uss']			= transferencias['factor_uss'] / 100
		#transferencias['Deuda']				= 0	
		transferencias['Monto Convenio']		= 0
		transferencias['tipo_de_pago']			= transferencias['tipo_pago'].replace({'INDIVIDUAL NORMAL': 'SUBV', 'MASIVO NORMAL': 'SUBV', 'URGENCIA': 'SUBV', 'ANTICIPO': 'SUBV', '80 BIS': '80 BIS', 'EMERGENCIA': 'EMG'})

		transferencias.loc[	(transferencias['cod_region'] == 1), 'nombre_region']	=  "TARAPACÁ"
		transferencias.loc[	(transferencias['cod_region'] == 2), 'nombre_region']	=  "ANTOFAGASTA"
		transferencias.loc[	(transferencias['cod_region'] == 3), 'nombre_region']	=  "ATACAMA"
		transferencias.loc[	(transferencias['cod_region'] == 4), 'nombre_region']	=  "COQUIMBO"
		transferencias.loc[	(transferencias['cod_region'] == 5), 'nombre_region']	=  "VALPARAÍSO"
		transferencias.loc[	(transferencias['cod_region'] == 6), 'nombre_region']	=  "O'HIGGINGS"
		transferencias.loc[	(transferencias['cod_region'] == 7), 'nombre_region']	=  "MAULE"
		transferencias.loc[	(transferencias['cod_region'] == 8), 'nombre_region']	=  "BÍO BÍO"
		transferencias.loc[	(transferencias['cod_region'] == 9), 'nombre_region']	=  "ARAUCANÍA"
		transferencias.loc[	(transferencias['cod_region'] == 10), 'nombre_region']	=  "LOS LAGOS"
		transferencias.loc[	(transferencias['cod_region'] == 11), 'nombre_region']	=  "AYSEN"
		transferencias.loc[	(transferencias['cod_region'] == 12), 'nombre_region']	=  "MAGALLANES"
		transferencias.loc[	(transferencias['cod_region'] == 13), 'nombre_region']	=  "METROPOLITANA"
		transferencias.loc[	(transferencias['cod_region'] == 14), 'nombre_region']	=  "LOS RÍOS"
		transferencias.loc[	(transferencias['cod_region'] == 15), 'nombre_region']	=  "ARICA Y PARINACOTA"
		transferencias.loc[	(transferencias['cod_region'] == 16), 'nombre_region']	=  "ÑUBLE"
		transferencias.loc[	(transferencias['cod_region'] == 17), 'nombre_region']	=  "DIR NACIONAL"




		transferencias.loc[	(transferencias['plazas_convenidas'] >  transferencias['plazas_atendidas'] ) & (transferencias['modelox'] != 'OPD'), 'Estandar_Plazas']	=  transferencias['plazas_atendidas']
		transferencias.loc[	(transferencias['plazas_convenidas'] == transferencias['plazas_atendidas'] ) & (transferencias['modelox'] != 'OPD'), 'Estandar_Plazas']	=  transferencias['plazas_atendidas']
		transferencias.loc[	(transferencias['plazas_convenidas'] <  transferencias['plazas_atendidas'] ) & (transferencias['modelox'] != 'OPD'), 'Estandar_Plazas']	=  transferencias['plazas_convenidas']
		transferencias.loc[	(transferencias['plazas_atendidas'] == 0) & (transferencias['numero_plazas'] == 0) , 'Estandar_Plazas']	=  transferencias['plazas_convenidas']
		transferencias.loc[	(transferencias['modelox'] == 'OPD'), 'Estandar_Plazas']		=  transferencias['plazas_convenidas']
		transferencias.loc[	(transferencias['tipo_pago'] == '80 BIS'), 'Estandar_Plazas']	=  transferencias['numero_plazas']



		df = self.calculate_estandar_monto(transferencias, '2401001', 'MASIVO NORMAL', 	'DAM')
		df = self.calculate_estandar_monto(transferencias, '2401001', '80 BIS', 		'DAM')
		df = self.calculate_estandar_monto(transferencias, '2401001', 'URGENCIA', 		'DAM')
		df = self.calculate_estandar_monto(transferencias, '2401001', 'OTROS PAGOS', 	'DAM')

		df = self.calculate_estandar_monto(transferencias, '2401001', 'MASIVO NORMAL', 	'DCE')
		df = self.calculate_estandar_monto(transferencias, '2401001', '80 BIS', 		'DCE')
		df = self.calculate_estandar_monto(transferencias, '2401001', 'URGENCIA', 		'DCE')
		df = self.calculate_estandar_monto(transferencias, '2401001', 'OTROS PAGOS', 	'DCE')


		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PIE')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PIE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PIE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PIE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PRM')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PRM')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PRM')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PRM')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PPF')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PPF')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PPF')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PPF')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PER')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PER')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PER')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PER')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PAD')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PAD')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PAD')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PAD')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PEE')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PEE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PEE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PEE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PEC')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PEC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PEC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PEC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PDE')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PDE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PDE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PDE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PDC')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PDC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PDC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PDC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PAS')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PAS')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PAS')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PAS')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PPC')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PPC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PPC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PPC')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PIB')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PIB')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PIB')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PIB')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'FPA')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'FPA')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'FPA')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'FPA')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'MASIVO NORMAL', 	'AFT')
		df = self.calculate_estandar_monto(transferencias, '2401002', '80 BIS', 		'AFT')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'URGENCIA', 		'AFT')
		df = self.calculate_estandar_monto(transferencias, '2401002', 'OTROS PAGOS', 	'AFT')


		df = self.calculate_estandar_monto(transferencias, '2401003', 'MASIVO NORMAL', 	'PRO')
		df = self.calculate_estandar_monto(transferencias, '2401003', '80 BIS', 		'PRO')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'URGENCIA', 		'PRO')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'OTROS PAGOS', 	'PRO')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'MASIVO NORMAL', 	'PER')
		df = self.calculate_estandar_monto(transferencias, '2401003', '80 BIS', 		'PER')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'URGENCIA', 		'PER')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'OTROS PAGOS', 	'PER')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'MASIVO NORMAL', 	'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401003', '80 BIS', 		'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'URGENCIA', 		'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'OTROS PAGOS', 	'PRE')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'MASIVO NORMAL', 	'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401003', '80 BIS', 		'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'URGENCIA', 		'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'OTROS PAGOS', 	'PRD')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'MASIVO NORMAL', 	'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401003', '80 BIS', 		'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'URGENCIA', 		'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'OTROS PAGOS', 	'PPE')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'MASIVO NORMAL', 	'PF')
		df = self.calculate_estandar_monto(transferencias, '2401003', '80 BIS', 		'PF')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'URGENCIA', 		'PF')
		df = self.calculate_estandar_monto(transferencias, '2401003', 'OTROS PAGOS', 	'PF')


		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'FAE')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'FAE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'FAE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'FAE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RPM')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RPM')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RPM')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RPM')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'REM')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'REM')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'REM')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'REM')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RLP')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RLP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RLP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RLP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RSP')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RSP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RSP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RSP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RMA')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RMA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RMA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RMA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'CLA')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'CLA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'CLA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'CLA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RPP')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RPP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RPP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RPP')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RDG')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RDG')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RDG')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RDG')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RDS')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RDS')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RDS')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RDS')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RDD')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RDD')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RDD')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RDD')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RVA')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RVA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RVA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RVA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RPL')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RPL')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RPL')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RPL')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RPF')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RPF')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RPF')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RPF')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'CPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'CPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'CPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'CPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RPE')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RAD')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RAD')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RAD')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RAD')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'REN')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'REN')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'REN')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'REN')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'FAS')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'FAS')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'FAS')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'FAS')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RVT')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RVT')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RVT')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RVT')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'MASIVO NORMAL', 	'RPA')
		df = self.calculate_estandar_monto(transferencias, '2401004', '80 BIS', 		'RPA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'URGENCIA', 		'RPA')
		df = self.calculate_estandar_monto(transferencias, '2401004', 'OTROS PAGOS', 	'RPA')


		df = self.calculate_estandar_monto(transferencias, '2401005', 'MASIVO NORMAL', 	'PRI')
		df = self.calculate_estandar_monto(transferencias, '2401005', '80 BIS', 		'PRI')
		df = self.calculate_estandar_monto(transferencias, '2401005', 'URGENCIA', 		'PRI')
		df = self.calculate_estandar_monto(transferencias, '2401005', 'OTROS PAGOS', 	'PRI')


		df = self.calculate_estandar_monto(transferencias, '2401006', 'MASIVO NORMAL', 	'OPD')
		df = self.calculate_estandar_monto(transferencias, '2401006', '80 BIS', 		'OPD')
		df = self.calculate_estandar_monto(transferencias, '2401006', 'URGENCIA', 		'OPD')
		df = self.calculate_estandar_monto(transferencias, '2401006', 'OTROS PAGOS', 	'OPD')



		"""
		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - transferencias OK 2.xlsx', engine='xlsxwriter')
		df.to_excel(writer, sheet_name='2401 - Diferencias < 0', index = False)
		writer.save()
		"""

		# Obtener la fecha de hoy
		today = date.today()

		# Crear un escritor Excel
		writer = pd.ExcelWriter(today.strftime("output/" + "%d-%b-%Y") + ' - transferencias OK 2.xlsx', engine='xlsxwriter')

		# Escribir el marco de datos en una hoja de cálculo
		df.to_excel(writer, sheet_name='2401 - Diferencias < 0', index=False)

		# Obtener el objeto de la hoja de trabajo
		workbook = writer.book
		worksheet = writer.sheets['2401 - Diferencias < 0']

		# Configurar el formato para las celdas de la columna 'AA' (amarillo)
		yellow_format = workbook.add_format({'bg_color': '#7fcfff'})

		# Aplicar el formato a las celdas de la columna 'AA'
		worksheet.set_column('BC:BG', None, yellow_format)

		# Ocultar la columna 'AA'
		worksheet.set_column('B:B', None, None, {'hidden': True})
		worksheet.set_column('D:E', None, None, {'hidden': True})
		worksheet.set_column('G:W', None, None, {'hidden': True})
		worksheet.set_column('AI:AI', None, None, {'hidden': True})
		worksheet.set_column('AL:AV', None, None, {'hidden': True})
		worksheet.set_column('AX:BB', None, None, {'hidden': True})




		# Guardar el archivo Excel
		writer.save()




		database = Database()
		database.crear_transferencias(df)



		
		"""
		Linea2401002(transferencias)
		Linea2401003(transferencias)
		Linea2401004(transferencias)
		Linea2401005(transferencias)
		Linea2401006(transferencias)
		"""
		#Linea2401(transferencias)

		"""

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - transferencias TEST cerouno.xlsx', engine='xlsxwriter')
		cerouno.to_excel(writer, sheet_name='2401 - Diferencias < 0', index = False)
		writer.save()
		"""

		"""
		for indice_fila in transferencias[ (transferencias['cuenta'] == '2401001') & (transferencias['tipo_pago'] == '80 BIS') & (transferencias['modelox'] == 'DAM') ].index:
															# 	factor_fijo 		factor_cobertura		asignacion_zona		factor_cvf				uss				numero_plazas			
			transferencias.at[indice_fila, 'Estandar Monto Fijo'] 		= f"=AB{indice_fila + 2}*(1+AE{indice_fila + 2}+AI{indice_fila + 2}+AH{indice_fila + 2})*AK{indice_fila + 2}*AL{indice_fila + 2}"
															# 	factor_variable		factor_edad				factor_complejidad	factor_discapacidad	asignacion_zona		uss					numero_plazas			
			transferencias.at[indice_fila, 'Estandar Monto Variable'] 	= f"=AC{indice_fila + 2}*(1+AD{indice_fila + 2}+AG{indice_fila + 2}+AF{indice_fila + 2})*AK{indice_fila + 2}*AL{indice_fila + 2}"




		transferencias.reset_index(drop=True, inplace=True)

		# Establecer el índice del DataFrame en 2
		transferencias.index += 2
		df_sin_duplicados = transferencias.drop_duplicates()


		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - transferencias TEST.xlsx', engine='xlsxwriter')
		df_sin_duplicados.to_excel(writer, sheet_name='2401 - Diferencias < 0', index = False)
		writer.save()


		database = Database()
		database.crear_transferencias(df_sin_duplicados)
		"""

		#database = Database()
		#database.databaseScrapy(transferencias)

