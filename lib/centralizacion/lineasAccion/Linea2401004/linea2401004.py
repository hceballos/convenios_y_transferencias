import pandas as pd
import glob
from lib.centralizacion.database.database import Database
import re

class Linea2401004:

	def __init__(self, df):

		#FAE
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'FAE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'FAE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'FAE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'FAE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'FAE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'FAE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'FAE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'FAE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#RPM
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPM'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPM'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPM'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPM'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#REM ============================================================================================================================================================================================================================================================================================================
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'REM'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'REM'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'REM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'REM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		#df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'REM'), 'Estandar Monto Fijo']	=  "=AB60*(1+AE60+AI60+AH60)*AK60*Z60"
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'REM'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'REM'), 'Estandar Monto Variable'] =  "=AC60*(1+AD60+AG60+AF60)*AK60*Z60"				
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'REM'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'REM'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'REM'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		#REM ============================================================================================================================================================================================================================================================================================================


		#RLP		
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RLP'), 'Monto Fijo']		=  df['factor_edad']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RLP'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RLP'), 'Monto Fijo']				=  df['factor_edad']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RLP'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RLP'), 'Estandar Monto Fijo']	=  "=AB121*(1+AE121+AI121+AH121)*AK121*Z121"
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RLP'), 'Monto Fijo']				=  df['factor_edad']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RLP'), 'Estandar Monto Variable'] =  "=AC123*(1+AD123+AG123+AF123+AI123)*AK123*Z123"		
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RLP'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RLP'), 'Monto Fijo']			=  df['factor_edad']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_convenidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RLP'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#RSP
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RSP'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RSP'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RSP'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RSP'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RSP'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RSP'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RSP'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RSP'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RMA
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RMA'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RMA'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RMA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RMA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RMA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RMA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RMA'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RMA'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#CLA
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'CLA'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'CLA'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'CLA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'CLA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'CLA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'CLA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'CLA'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'CLA'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#RPP
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPP'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPP'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPP'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPP'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPP'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPP'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPP'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPP'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RDG
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RDG'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RDG'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RDG'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RDG'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RDG'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RDG'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RDG'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RDG'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RDS
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RDS'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RDS'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RDS'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RDS'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RDS'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RDS'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RDS'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RDS'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RDD
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RDD'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RDD'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RDD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RDD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RDD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RDD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RDD'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RDD'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RVA
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RVA'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RVA'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RVA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RVA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RVA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RVA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RVA'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RVA'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RPL
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPL'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPL'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPL'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPL'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPL'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPL'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPL'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPL'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RPF
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPF'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPF'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPF'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPF'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPF'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPF'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPF'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPF'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#CPE
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'CPE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'CPE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'CPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'CPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'CPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'CPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'CPE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'CPE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RPE
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPE'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPE'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPE'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPE'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPE'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPE'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		#RAD
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RAD'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RAD'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RAD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RAD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RAD'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RAD'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RAD'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RAD'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#REN
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'REN'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'REN'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'REN'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'REN'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'REN'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'REN'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'REN'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'REN'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#FAS
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'FAS'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'FAS'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'FAS'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'FAS'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'FAS'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'FAS'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'FAS'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'FAS'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RVT
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RVT'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RVT'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RVT'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RVT'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RVT'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RVT'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RVT'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RVT'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']
		
		#RPA
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPA'), 'Monto Fijo']		=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'MASIVO NORMAL') & (df['modelox'] == 'RPA'), 'Monto Variable']	=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['numero_plazas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == '80 BIS') & (df['modelox'] == 'RPA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['numero_plazas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPA'), 'Monto Fijo']				=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'URGENCIA') & (df['modelox'] == 'RPA'), 'Monto Variable']			=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPA'), 'Monto Fijo']			=  df['factor_fijo']	*(1+df['factor_cobertura']	+df['asignacion_zona']		+df['factor_cvf']								) *df['uss']	*df['plazas_atendidas']
		df.loc[	(df['cuenta'] == '2401004') & (df['tipo_pago'] == 'OTROS PAGOS') & (df['modelox'] == 'RPA'), 'Monto Variable']		=  df['factor_variable']*(1+df['factor_edad']		+df['factor_complejidad']	+df['factor_discapacidad']	+df['asignacion_zona'])	*df['uss']			*df['plazas_atendidas']

		df['Monto Convenio'] = df['Monto Fijo'] + df['Monto Variable']
		df['Diferencia'] 	 = df['monto_liquido_pagado'] - df['Monto Convenio']



		database = Database()
		database.crear_transferencias(df)