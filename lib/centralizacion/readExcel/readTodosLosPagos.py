import pandas as pd
import glob
from lib.centralizacion.database.database import Database

class ReadTodosLosPagos:
	def __init__(self, datos):
		self.datos = datos

		todosLosPagos = pd.DataFrame()
		for f in glob.glob('./input_excel/centralizacion/todosLosPagos/*.xlsx', recursive=True):
			print('Procesando  : ', f)

			todosLosPagos_actual = pd.read_excel(f, converters={ 	'Fecha de Recepción': str,
																	'codigo': str,
																	'Region': str,
																	'Periodo de Atención a Levantar o Retener': str,
																	'Código ': str}, 


				usecols = [
					'MES ATENCION', 
					'ID TIPO PAGO', 
					'TIPO PAGO', 
					'FOLIO', 
					'COD REGION', 
					'COD PROYECTO', 
					'PROYECTO', 
					'COD INSTITUCION', 
					'INSTITUCION', 
					'DEPARTAMENTO SENAME', 
					'TIPO SUBVENCION_DES', 
					'TIPO PROYECTO_DES', 
					'MODELO INTERVENCION', 
					'BANCO', 
					'CUENTA CORRIENTE NUMERO', 
					'RUT PROYECTO', 
					'MONTO MAXIMO PAGO', 
					'MONTO PAGO FIJO', 
					'MONTO PAGO VARIABLE', 
					'MONTO POR ATENCION', 
					'MONTO DEUDA', 
					'MONTO RELIQUIDACION', 
					'MONTO RETENCION', 
					'MONTO LIQUIDO PAGADO', 
					'PLAZAS CONVENIDAS', 
					'PLAZAS ATENDIDAS', 
					'FACTOR FIJO', 
					'FACTOR VARIABLE', 
					'FACTOR EDAD', 
					'FACTOR COBERTURA', 
					'FACTOR DISCAPACIDAD', 
					'FACTOR COMPLEJIDAD', 
					'FACTOR CVF', 
					'ASIGNACION ZONA', 
					'FACTOR USS', 
					'USS', 
					'NUMERO PLAZAS', 
					'NRO DIAS', 
					'FECHA CIERRE PAGO ', 
					'NUMERO RESOLUCION', 
					'FECHA CREACION', 
					'FECHA TERMINO', 
					'NUMERO CDP', 
					'ANNO PRESUPUESTARIO', 
					'NUMERO RESOLUCION CDP', 
					'FECHA RESOLUCION CDP', 
					'DESCRIPCION CDP',
					'FECHA DE PAGO'
					])



			todosLosPagos = todosLosPagos.append(todosLosPagos_actual, ignore_index=True)
		todosLosPagos.rename(columns={'MES ATENCION': 'mes_atencion', 'ID TIPO PAGO': 'id_tipo_pago', 'TIPO PAGO': 'tipo_pago', 'FOLIO': 'folio', 'COD REGION': 'cod_region', 'COD PROYECTO': 'cod_proyecto', 'PROYECTO': 'proyecto', 'COD INSTITUCION': 'cod_institucion', 'INSTITUCION': 'institucion', 'DEPARTAMENTO SENAME': 'departamento_sename', 'TIPO SUBVENCION_DES': 'tipo_subvencion_des', 'TIPO PROYECTO_DES': 'tipo_proyecto_des', 'MODELO INTERVENCION': 'modelo_intervencion', 'BANCO': 'banco', 'CUENTA CORRIENTE NUMERO': 'cuenta_corriente_numero', 'RUT PROYECTO': 'rut_proyecto', 'MONTO MAXIMO PAGO': 'monto_maximo_pago', 'MONTO PAGO FIJO': 'monto_pago_fijo', 'MONTO PAGO VARIABLE': 'monto_pago_variable', 'MONTO POR ATENCION': 'monto_por_atencion', 'MONTO DEUDA': 'monto_deuda', 'MONTO RELIQUIDACION': 'monto_reliquidacion', 'MONTO RETENCION': 'monto_retencion', 'MONTO LIQUIDO PAGADO': 'monto_liquido_pagado', 'PLAZAS CONVENIDAS': 'plazas_convenidas', 'PLAZAS ATENDIDAS': 'plazas_atendidas', 'FACTOR FIJO': 'factor_fijo', 'FACTOR VARIABLE': 'factor_variable', 'FACTOR EDAD': 'factor_edad', 'FACTOR COBERTURA': 'factor_cobertura', 'FACTOR DISCAPACIDAD': 'factor_discapacidad', 'FACTOR COMPLEJIDAD': 'factor_complejidad', 'FACTOR CVF': 'factor_cvf', 'ASIGNACION ZONA': 'asignacion_zona', 'FACTOR USS': 'factor_uss', 'USS': 'uss', 'NUMERO PLAZAS': 'numero_plazas', 'NRO DIAS': 'nro_dias', 'FECHA CIERRE PAGO ': 'fecha_cierre_pago_', 'NUMERO RESOLUCION': 'numero_resolucion', 'FECHA CREACION': 'fecha_creacion', 'FECHA TERMINO': 'fecha_termino', 'NUMERO CDP': 'numero_cdp', 'ANNO PRESUPUESTARIO': 'anno_presupuestario', 'NUMERO RESOLUCION CDP': 'numero_resolucion_cdp', 'FECHA RESOLUCION CDP': 'fecha_resolucion_cdp', 'DESCRIPCION CDP': 'descripcion_cdp'}, inplace=True)

		todosLosPagos['Analisis']      = 'Pendiente'

		todosLosPagos['numero_mes'] = todosLosPagos['mes_atencion'].apply(lambda x: str(x)[-2:] if pd.notnull(x) else None)
		todosLosPagos['proyecto'].fillna('', inplace=True)  # Rellenar los valores NaN con una cadena vacía


		todosLosPagos.loc[todosLosPagos['proyecto'].str.contains('OFICINA'), 'proyecto'] 	= 'OPD'
		todosLosPagos.loc[todosLosPagos['proyecto'].str.contains('ESCI'), 'proyecto'] 	= 'PEE'
		todosLosPagos['modelox'] = todosLosPagos['proyecto'].str.split(r'\s|-').str[0]

		cambios_de_nombre 				 = {'EMG': '2401004', 'CLA': '2401004', 'CPE': '2401004', 'DAM': '2401001', 'DCE': '2401001', 'FAE': '2401004', 'FAS': '2401004', 'FPA': '2401002', 'OPD': '2401006', 'PAD': '2401002','PAS': '2401002','PDC': '2401002','PDE': '2401002','PEC': '2401002','PEE': '2401002','PER': '2401003',  'PIB': '2401002', 'PIE': '2401002', 'PPC': '2401002', 'PPE': '2401003', 'PPF': '2401002', 'PRD': '2401003', 'PRE': '2401003', 'PRI': '2401005', 'PRM': '2401002','PRO': '2401003','RAD': '2401004','RDD': '2401004','RDG': '2401004','RDS': '2401004','REM': '2401004','REN': '2401004', 'RLP': '2401004', 'RMA': '2401004', 'RPA': '2401004', 'RPE': '2401004', 'RPF': '2401004', 'RPL': '2401004', 'RPM': '2401004', 'RPP': '2401004', 'RSP': '2401004', 'RVA': '2401004', 'RVT': '2401004'}
		todosLosPagos['cuenta'] 		 = todosLosPagos['modelox'].replace(cambios_de_nombre)
		todosLosPagos['modificaciones'] = todosLosPagos['folio'].str[-7]
		todosLosPagos[['plazas_atendidas', 'factor_variable', 'asignacion_zona', 'numero_plazas', 'uss']] = todosLosPagos[['plazas_atendidas', 'factor_variable', 'asignacion_zona', 'numero_plazas' ,'uss']].fillna(0)
		todosLosPagos['uss'] 			 = todosLosPagos['uss'].astype(int)
		
		database = Database()
		database.crear_todosLosPagos(todosLosPagos)