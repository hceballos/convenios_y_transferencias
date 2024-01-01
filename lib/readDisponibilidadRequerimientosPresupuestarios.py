from lib.database  import Database
from lib.readJson  import ReadJson
import pandas as pd
import glob
import xlrd
import csv
import os
import sqlite3
from datetime import datetime
from datetime import date

class ReadDisponibilidadRequerimientosPresupuestarios(ReadJson):

	def normalizeDateConta(self, dateString):
		return dateString.replace(['(\d{2}).(\d{2}).(\d{2})?(\d{2})'], ['\g<4>-\g<2>-\g<1>'], regex=True)

	def normalizeDate(self, dateString):
		return dateString.replace(['(\d{2})\/(\d{2})\/(\d{4})'], ['\g<3>-\g<2>-\g<1>'], regex=True)

	def normalizeNumeric(self, string):
		string	= [w.replace(',00', '' ) for w in string ]
		string	= [w.replace(' ', '' ) for w in string ]
		string	= [w.replace('$', '' ) for w in string ]
		string	= [w.replace('.', '' ) for w in string ]
		string	= [w.replace('(', '-' ) for w in string ]
		string	= [w.replace(')', '' ) for w in string ]
		return pd.to_numeric(string)

	def normalizeFloat64ToString(self, numero):
		print(type(numero))
		numeroInString = numero.astype(str)
		print(type(numeroInString))
		return numero

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		"""
		clasificador = pd.DataFrame()
		for f in glob.glob(self.datos['clasificador'], recursive=True):
			df = pd.read_excel(f, converters={ 'codigo': str } )
			print('Procesando  : ', f)
			clasificador = clasificador.append(df,ignore_index=True)

		database = Database()
		database.databaseClasificador(clasificador)
		"""
		region_mapping = { '2111001': 0, '2111002': 1, '2111003': 2, '2111004': 3, '2111005': 4, '2111006': 5, '2111007': 6, '2111008': 7, '2111009': 8, '2111010': 9, '2111011': 10, '2111012': 11, '2111013': 12, '2111014': 13, '2111015': 15, '2111016': 14, '2111017': 16}
		tipo_de_pago_mapping = { 	'MetasAdicionales - 00 No Aplica' : 'SUBV', 
									'MetasAdicionales - 01 META 80 BIS' : '80 BIS', 'MetasAdicionales - 02 EMERGENCIA' : 'EMG'}

		disponibilidadRequerimientos = pd.DataFrame()
		for f in glob.glob(self.datos['DisponibilidadRequerimientos'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f, skiprows=4, header=0)  
			#print(df.columns)
			#df['rut']				= df['Principal'].str.split(' ', n = 1, expand = True)[0]
			df['CodRegion']			= df['Unidad Ejecutora'].str.split(' ', n = 1, expand = True)[0]
			df['cuenta']			= df['Concepto Presupuesto'].str.split(' ', n = 1, expand = True)[0]
			df['tipo_de_pago'] 		= df['Catálogo 05'].map(tipo_de_pago_mapping)
			df['region']			= df['CodRegion'].map(region_mapping)
			df['unico']				= df['CodRegion'] + df['cuenta']

			disponibilidadRequerimientos = disponibilidadRequerimientos.append(df,ignore_index=True)

		database = Database()
		database.databaseDisponibilidadRequerimientos(disponibilidadRequerimientos)

		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				disponibilidadRequerimientos.* \
			FROM \
				disponibilidadRequerimientos \
			WHERE \
				disponibilidadRequerimientos.'Concepto Presupuesto' like '2401%' \
		"
		query = pd.read_sql_query(consulta, cnx)

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - DisponibilidadRequerimientosPresupuestarios.xlsx', engine='xlsxwriter')
		query.to_excel(writer, sheet_name='2401 - Todas las coberturas', index = False)
		writer.save()