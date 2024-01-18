import pandas as pd
import glob
from lib.centralizacion.database.database import Database
import re

class Linea2401002:

	def __init__(self, df):

		#PIE
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PIE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PIE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PIE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PIE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PIE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PIE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PIE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PIE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PRM
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRM'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRM'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRM'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRM'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PPF
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPF'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPF'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPF'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPF'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPF'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPF'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPF'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPF'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PER
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PER'), 'Monto Fijo']		=  "Error Clasificacion"
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PER'), 'Monto Variable']	=  "Error Clasificacion"

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PER'), 'Monto Fijo']				=  "Error Clasificacion"
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PER'), 'Monto Variable']			=  "Error Clasificacion"

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PER'), 'Monto Fijo']				=  "Error Clasificacion"
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PER'), 'Monto Variable']			=  "Error Clasificacion"

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PER'), 'Monto Fijo']			=  "Error Clasificacion"
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PER'), 'Monto Variable']		=  "Error Clasificacion"

		#PAD
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PAD'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PAD'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PAD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PAD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PAD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PAD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PAD'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PAD'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PEE
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PEE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PEE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PEE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PEE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PEE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PEE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PEE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PEE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PEC
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PEC'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PEC'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PEC'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PEC'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PEC'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PEC'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PEC'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PEC'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PDE
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PDE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PDE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PDE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PDE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PDE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PDE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PDE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PDE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PDC
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PDC'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PDC'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PDC'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PDC'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PDC'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PDC'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PDC'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PDC'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#PAS
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PAS'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PAS'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PAS'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PAS'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PAS'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PAS'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PAS'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PAS'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PPC
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPC'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPC'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPC'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPC'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPC'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPC'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPC'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPC'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PIB
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PIB'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PIB'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PIB'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PIB'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PIB'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PIB'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PIB'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PIB'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PRE
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PRD
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRD'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PRD'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PRD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PRD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRD'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PRD'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#FPA
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'FPA'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'FPA'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'FPA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'FPA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'FPA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'FPA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'FPA'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'FPA'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#PPE
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'PPE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'PPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'PPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'PPE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#AFT	
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'AFT'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'AFT'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'AFT'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'AFT'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'AFT'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'AFT'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'AFT'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								  ) *df['factor_uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401002') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'AFT'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		#AFT

		df['Monto Convenio'] = df['Monto Fijo'] + df['Monto Variable']
		df['Diferencia'] 	 = df['monto_liquido_pagado'] - df['Monto Convenio']

		database = Database()
		database.crear_transferencias(df)