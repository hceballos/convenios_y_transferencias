import pandas as pd
import glob
from lib.centralizacion.database.database import Database

class ReadtodasLasFES:
	def __init__(self, datos):
		self.datos = datos

		fes = pd.DataFrame()
		for f in glob.glob('./input_excel/centralizacion/FES/*.xlsx', recursive=True):
			print('Procesando  : ', f)

			fes_actual = pd.read_excel(f)
			fes = fes.append(fes_actual, ignore_index=True)

		# print(fes.columns)
		fes['Fechaactualizacion']	= pd.to_datetime(fes['Fechaactualizacion'])
		fes['ultimo_dia_del_mes'] 	= fes['Fechaactualizacion'] + pd.offsets.MonthEnd(0)
		fes['nro_dias_Mes'] 		= (fes['ultimo_dia_del_mes'] - fes['Fechaactualizacion']).dt.days
		fes['Analisis']      		= 'Pendiente'

		database = Database()
		database.crear_Fes(fes)