from lib.centralizacion.database.database import Database
import pandas as pd
import glob
import sqlite3
import os
from datetime import date


class ReadRendicionDeCuentas(object):

	def __init__(self, datos):
		self.datos = datos

		try:
			os.remove("consolidado Retenciones.xlsx")
		except Exception as e:
			pass

		rendicionDeCuentas = pd.DataFrame()
		for f in glob.glob("./input_excel/centralizacion/rendicionDeCuentas/*", recursive=True):
			print('Procesando  : ', f)
			if "ruce" in f:
				pass
			else:
				df = pd.read_excel(f, converters={ 'Fecha de Recepción': str, 'codigo': str, 'Region': str, 'Periodo de Atención a Levantar o Retener': str, 'Código ': str} , usecols = ['Fecha de Recepción', 'Region',  'Periodo de Atención a Levantar o Retener', 'Código ', 'SI Presenta Rend. De Cuenta', 'NO Presenta Rend. De Cuenta'])
				rendicionDeCuentas = rendicionDeCuentas.append(df,ignore_index=True)

		rendicionDeCuentas.rename(columns={'Código ': 'codigo', 'Fecha de Recepción' : 'Fecha_de_Recepcion', 'Periodo de Atención a Levantar o Retener' : 'Periodo de Atencion a Levantar o Retener'}, inplace=True)





		rendicionDeCuentas=rendicionDeCuentas.dropna(how='all')
		rendicionDeCuentas['Fecha_de_Recepcion'] = pd.to_datetime(rendicionDeCuentas['Fecha_de_Recepcion'])
		rendicionDeCuentas.rename(columns={'Periodo de Atencion a Levantar o Retener': 'MES ATENCION'}, inplace=True)
		rendicionDeCuentas['unico'] = rendicionDeCuentas['codigo'].astype(str) + rendicionDeCuentas['MES ATENCION']
		rendicionDeCuentas = rendicionDeCuentas.reset_index(drop=True)
		rendicionDeCuentas['Fecha_de_Recepcion'] = pd.to_datetime(rendicionDeCuentas['Fecha_de_Recepcion'])
		rendicionDeCuentas['Fecha_de_Recepcion'] = rendicionDeCuentas['Fecha_de_Recepcion'].dt.date


		#print(rendicionDeCuentas.columns)

		database = Database()
		database.crear_rendicionDeCuentas(rendicionDeCuentas)

		cnx = sqlite3.connect('centralizacion.db')
		consulta = " \
			SELECT \
				rendicionDeCuentas.* \
			FROM \
				rendicionDeCuentas \
			ORDER BY \
				rendicionDeCuentas.'Fecha_de_Recepcion' DESC \
		"
		rendicionDeCuentas = pd.read_sql_query(consulta, cnx)

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - Consolidado rendicion De Cuentas.xlsx', engine='xlsxwriter')
		rendicionDeCuentas.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Retenciones', index = False)
		writer.save()