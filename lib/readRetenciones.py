from lib.database  import Database
import sqlalchemy
import pandas as pd
import numpy as np
import glob
import sqlite3
import xlrd
import csv
import os
import re
import sys
import datetime
from datetime import date
from datetime import datetime


class ReadRetenciones(object):

	def __init__(self, datos):
		self.datos = datos

		try:
			os.remove("consolidado Retenciones.xlsx")
		except Exception as e:
			pass

		retenciones = pd.DataFrame()
		for f in glob.glob(self.datos['readRetenciones'], recursive=True):
			print(f)
			if "ruce" in f:
				pass
			else:
				df = pd.read_excel(f, converters={ 'Fecha de Recepción': str, 'codigo': str, 'Region': str, 'Periodo de Atención a Levantar o Retener': str, 'Código ': str} , usecols = ['Fecha de Recepción', 'Region',  'Periodo de Atención a Levantar o Retener', 'Código ', 'SI Presenta Rend. De Cuenta', 'NO Presenta Rend. De Cuenta'])
				retenciones = retenciones.append(df,ignore_index=True)

		retenciones=retenciones.dropna(how='all')

		retenciones['Fecha de Recepción'] = pd.to_datetime(retenciones['Fecha de Recepción'])


		df.rename(columns={
			'Periodo de Atención a Levantar o Retener': 'MES ATENCION'
			}, inplace=True)


		#retenciones['SI Presenta Rend. De Cuenta'] 	= retenciones['SI Presenta Rend. De Cuenta'].str.replace(r'\w+', r'X')
		#retenciones['NO Presenta Rend. De Cuenta'] 	= retenciones['NO Presenta Rend. De Cuenta'].str.replace(r'\w+', r'X')
		#retenciones['SI Presenta Rend. De Cuenta'] 	= retenciones['SI Presenta Rend. De Cuenta'].replace(to_replace=r'^.*$', value='X', regex=True)
		#retenciones['NO Presenta Rend. De Cuenta'] 	= retenciones['NO Presenta Rend. De Cuenta'].replace(to_replace=r'^.*$', value='X', regex=True)
		#retenciones['Fecha de Recepción'] 				= retenciones['Fecha de Recepción'].replace(to_replace=r' 00:00:00.000000', value='', regex=True)

		retenciones = retenciones.reset_index(drop=True)

		database = Database()
		database.databaseRetenciones(retenciones)
		database.databaseRetencionesCalculoPago(retenciones)

		cnx = sqlite3.connect('database.db')
		consulta = " \
			SELECT \
				retenciones.* \
			FROM \
				retenciones \
			ORDER BY \
				retenciones.'Fecha de Recepción' DESC \
		"
		retenciones = pd.read_sql_query(consulta, cnx)


		consulta = " \
			SELECT \
				DATE(retenciones.'Fecha de Recepción') AS 'Fecha de Recepción', \
				retenciones.'Region', \
				retenciones.'Periodo de Atención a Levantar o Retener', \
				retenciones.'Código ', \
			    retenciones.'Código ' || retenciones.'Periodo de Atención a Levantar o Retener' AS 'unico', \
				retenciones.'SI Presenta Rend. De Cuenta' \
			FROM \
			    retenciones \
			WHERE \
			    retenciones.'SI Presenta Rend. De Cuenta' IS NOT NULL \
			ORDER BY \
			    retenciones.'Fecha de Recepción' DESC \
		"
		retenciones_SI = pd.read_sql_query(consulta, cnx)


		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - Consolidado Retenciones.xlsx', engine='xlsxwriter')
		retenciones_SI.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='retenciones_SI', index = False)
		retenciones.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Retenciones detallado', index = False)
		writer.save()