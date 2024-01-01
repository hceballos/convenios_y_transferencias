import sqlalchemy
import pandas as pd
import numpy as np
from datetime import datetime

class Analisis(object):

	def calcular_dias_transcurridos(self, df):
		df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
		hoy = datetime.now()
		df['dias_transcurridos'] = (hoy - df['fecha_creacion']).dt.days
		return df['dias_transcurridos']

	def analisis_Rendiciones(self, df):
		df['dias_transcurridos'] = self.calcular_dias_transcurridos(df)







		opd = (df['modelox'].str.startswith('OPD'))
		BIS = (df['tipo_pago'] == '80 BIS')
		def calcular_plazas(row):
			plazas = []
			if ( (opd[row.name]) ):
				if (row['plazas_convenidas'] > row['plazas_atendidas']):
					plazas.append(row['plazas_convenidas'])
				else:
					plazas.append(row['plazas_atendidas'])

			elif ( (BIS[row.name]) ):
				plazas.append(row['numero_plazas'])

			elif ( ~(opd[row.name]) ):

				if (row['plazas_convenidas'] > row['plazas_atendidas']):
					plazas.append(row['plazas_atendidas'])
				else:
					plazas.append(row['plazas_convenidas'])

			return plazas

		df['plazas_a_calculo'] = df.apply(calcular_plazas, axis=1)


		return df
