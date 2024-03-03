import pandas as pd
import glob
from lib.centralizacion.database.database import Database
import re

class Linea2401005:

	def __init__(self, df):



		#PRI
		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRI'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRI'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRI'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRI'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRI'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRI'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRI'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401005') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRI'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df['Monto Convenio'] = df['Monto Fijo'] + df['Monto Variable']
		df['Diferencia'] 	 = df['monto_liquido_pagado'] - df['Monto Convenio']






		database = Database()
		database.crear_transferencias(df)