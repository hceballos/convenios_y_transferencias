import sqlalchemy
import pandas as pd
import numpy as np
from datetime import datetime

class Analisis(object):


	def analisis_Rendiciones(self, df):
		df['Analisis']      = 'Pendiente'
		#print(df.columns)
		df.loc[ (df['PLAZAS'] == df['plazasAtendidas']) & 
				(df['PLAZAS'] == df['plazas_convenidas']), 'Analisis'] = 'Okey'


		#df.loc[	(df['plazas_atendidas']) > (df['plazasAtendidas']), 'Analisis'] = df['plazasAtendidas']




		print(df)
		return df