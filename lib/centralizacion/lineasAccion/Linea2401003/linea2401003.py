import pandas as pd
import glob
from lib.centralizacion.database.database import Database
import re

class Linea2401003:

	def __init__(self, df):





		#PRO
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRO'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRO'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRO'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRO'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRO'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRO'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRO'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRO'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PER
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PER'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PER'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PER'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PER'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PER'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PER'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PER'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PER'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PRO
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRO'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRO'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRO'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRO'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRO'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRO'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRO'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRO'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
	
		#PER
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PER'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PER'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PER'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PER'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PER'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PER'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PER'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PER'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PRE
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PRD
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRD'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRD'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRD'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRD'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PPE
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401003') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']


		df['Monto Convenio'] = df['Monto Fijo'] + df['Monto Variable']
		df['Diferencia'] 	 = df['monto_liquido_pagado'] - df['Monto Convenio']





		database = Database()
		database.crear_transferencias(df)