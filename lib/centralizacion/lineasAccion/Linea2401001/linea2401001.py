import pandas as pd
import glob
from lib.centralizacion.database.database import Database
import re

class Linea2401001:



	def calculate_estandar_monto(self, df, cuenta, tipo_pago, modelox, numero_plazas=False):
		filtro = (df['cuenta'] == cuenta) & (df['tipo_pago'] == tipo_pago) & (df['modelox'] == modelox)
		indice_filas = df[filtro].index
		
		# Asignar las fórmulas a las columnas correspondientes
		for indice_fila in indice_filas:
			# Asignar la fórmula a la columna 'Estandar Monto Fijo'
			df.at[indice_fila, 'Estandar Monto Fijo'] = f"=AB{indice_fila}*(1+AE{indice_fila}+AI{indice_fila}+AH{indice_fila})*AK{indice_fila}*AA{indice_fila}"
			# Asignar la fórmula a la columna 'Estandar Monto Variable'
			df.at[indice_fila, 'Estandar Monto Variable'] = f"=AC{indice_fila}*(1+AD{indice_fila}+AG{indice_fila}+AF{indice_fila})*AK{indice_fila}*AA{indice_fila}"

		# Reiniciar el índice para que comience en 2
		df.reset_index(drop=True, inplace=True)
		df.index += 2
		
		return df


	def __init__(self, df):
		


		print("Linea2401001")




		# df = self.calculate_estandar_monto(df, '2401001', 'MASIVO NORMAL', 	'DAM')
		# df = self.calculate_estandar_monto(df, '2401001', '80 BIS', 		'DAM', numero_plazas=True)
		# df = self.calculate_estandar_monto(df, '2401001', 'URGENCIA', 		'DAM')
		# df = self.calculate_estandar_monto(df, '2401001', 'OTROS PAGOS', 	'DAM')

		# df = self.calculate_estandar_monto(df, '2401001', 'MASIVO NORMAL', 	'DCE')
		# df = self.calculate_estandar_monto(df, '2401001', '80 BIS', 		'DCE', numero_plazas=True)
		# df = self.calculate_estandar_monto(df, '2401001', 'URGENCIA', 		'DCE')
		# df = self.calculate_estandar_monto(df, '2401001', 'OTROS PAGOS', 	'DCE')

		return df


		"""
		# DAM
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'DAM'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'DAM'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'DAM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'DAM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'DAM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'DAM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'DAM'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'DAM'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		# CDE
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'DCE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'DCE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'DCE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'DCE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'DCE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'DCE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'DCE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401001') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'DCE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df['Monto Convenio'] = df['Monto Fijo'] + df['Monto Variable']
		df['Diferencia'] 	 = df['monto_liquido_pagado'] - df['Monto Convenio']

		return 
		"""

		# ===============================================================================================================================

		# df['factor_variable']*(1+df['factor_edad'] +df['factor_complejidad'] +df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss'] *df['plazas_atendidas']

		# =AB{indice_fila + 2}	*	(1+AE{indice_fila + 2}	+	AI{indice_fila + 2}	+	AH{indice_fila + 2})	*	AK{indice_fila + 2}	*	AA{indice_fila + 2}"


		"""
		for indice_fila in df[ (df['cuenta'] == '2401001') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'DAM') ].index:
															# 	factor_fijo 		factor_cobertura		asignacion_zona		factor_cvf				uss				plazas_atendidas
			df.at[indice_fila, 'Estandar Monto Fijo'] 		= f"=AB{indice_fila}*(1+AE{indice_fila}+AI{indice_fila}+AH{indice_fila})*AK{indice_fila}*AA{indice_fila}"
															# 	factor_variable		factor_edad				factor_complejidad	factor_discapacidad	asignacion_zona		uss					plazas_atendidas
			df.at[indice_fila, 'Estandar Monto Variable'] 	= f"=AC{indice_fila}*(1+AD{indice_fila}+AG{indice_fila}+AF{indice_fila}+AI{indice_fila})*AK{indice_fila}*AA{indice_fila}"



		for indice_fila in df[ (df['cuenta'] == '2401001') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'DAM') ].index:
															# 	factor_fijo 		factor_cobertura		asignacion_zona		factor_cvf				uss				numero_plazas			
			df.at[indice_fila, 'Estandar Monto Fijo'] 		= f"=AB{indice_fila}*(1+AE{indice_fila}+AI{indice_fila}+AH{indice_fila})*AK{indice_fila}*AL{indice_fila}"
															# 	factor_variable		factor_edad				factor_complejidad	factor_discapacidad	asignacion_zona		uss					numero_plazas			
			df.at[indice_fila, 'Estandar Monto Variable'] 	= f"=AC{indice_fila}*(1+AD{indice_fila}+AG{indice_fila}+AF{indice_fila})*AK{indice_fila}*AL{indice_fila}"
		"""



		"""
		for indice_fila in df[ (df['cuenta'] == '2401001') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'DCE') ].index:
								# 	factor_fijo 		factor_cobertura		asignacion_zona		factor_cvf				uss				plazas_atendidas			
			df.at[indice_fila, 'Estandar Monto Fijo'] 		= f"=AB{indice_fila}*(1+AE{indice_fila}+AI{indice_fila}+AH{indice_fila})*AK{indice_fila}*AA{indice_fila}"
															# 	factor_variable		factor_edad				factor_complejidad	factor_discapacidad	asignacion_zona		uss					numero_plazas			
			df.at[indice_fila, 'Estandar Monto Variable'] 	= f"=AC{indice_fila}*(1+AD{indice_fila}+AG{indice_fila}+AF{indice_fila})*AK{indice_fila}*AA{indice_fila}"
		"""















			#df.at[indice_fila, 'Estandar Monto Total'] 		= f"=BG{indice_fila} + BH{indice_fila}"
			#df.at[indice_fila, 'Estandar Diferencia'] 		= f"=Y{indice_fila}  - BI{indice_fila}"

		# print(df.columns)
		#df_sin_duplicados = df[~df.index.duplicated()]





		#database = Database()
		#database.crear_transferencias(df)

