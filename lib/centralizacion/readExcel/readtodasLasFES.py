import pandas as pd
import glob
from lib.centralizacion.database.database import Database

class ReadtodasLasFES:
	def __init__(self, datos):
		self.datos = datos

		todosLosPagos = pd.DataFrame()
		for f in glob.glob('./input_excel/centralizacion/todasLasFES/*.xlsx', recursive=True):
			print('Procesando  : ', f)

			todosLosPagos_actual = pd.read_excel(f)
			todosLosPagos = todosLosPagos.append(todosLosPagos_actual, ignore_index=True)


		print(todosLosPagos.columns)
		todosLosPagos['Analisis']      = 'Pendiente'

