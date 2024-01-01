from lib.database  import Database
from lib.readJson  import ReadJson
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


class ReadCompromiso(ReadJson):


	def normalizeDateConta(self, dateString):
		return dateString.replace(['(\d{2}).(\d{2}).(\d{2})?(\d{2})'], ['\g<4>-\g<2>-\g<1>'], regex=True)

	def normalizeDate(self, dateString):
		return dateString.replace(['(\d{2})\/(\d{2})\/(\d{4})'], ['\g<3>-\g<2>-\g<1>'], regex=True)

	def normalizeNumeric(self, string):
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

		compromiso = pd.DataFrame()
		for f in glob.glob(self.datos['CompromisoCarteraFinanciera'], recursive=True):
			print('Procesando  : ', f)
			wb = xlrd.open_workbook(f)
			sh = wb.sheet_by_name('Sheet1')
			compromisocsv = open('compromiso.csv', 'w')
			wr = csv.writer(compromisocsv, quoting=csv.QUOTE_ALL)
			for rownum in range(sh.nrows):
				wr.writerow(sh.row_values(rownum))
			compromisocsv.close()
			df1 = pd.read_csv('compromiso.csv', converters={ 'Número Documento': str }, encoding='utf8')
			compromiso = compromiso.append(df1,ignore_index=True)

		compromiso['Tipo Vista']		= compromiso.drop( compromiso[ compromiso['Tipo Vista'] == 'Saldo Inicial' ].index , inplace=True )
		#compromiso['FechaDocumento']	= self.normalizeDate(compromiso['Fecha Documento'])
		#compromiso['FechaDocumento']	= pd.to_datetime(compromiso['FechaDocumento']).dt.date
		#compromiso['Fecha']			= self.normalizeDate(compromiso['Fecha'])
		#compromiso['Fecha']			= pd.to_datetime(compromiso['Fecha']).dt.date
		compromiso['rut']				= compromiso['Principal'].str.split(' ', n = 1, expand = True)[0]
		compromiso['CodConcepto']		= compromiso['Concepto'].str.split(' ', n = 1, expand = True)[0]
		compromiso['NombreConcepto']	= compromiso['Concepto'].str.split(' ', n = 1, expand = True)[1]
		compromiso['unico']				= compromiso['rut'] + compromiso['Número Documento']
		#compromiso['ordenDeCompra'] 	= "pendiente"
		#compromiso['status'] 			= "pendiente"
		compromiso['Monto Documento.1']	= self.normalizeNumeric(compromiso['Monto Documento.1'])
		compromiso['Monto Documento']	= self.normalizeNumeric(compromiso['Monto Documento'])

		compromiso['Fecha']	= self.normalizeDate(compromiso['Fecha'])
		compromiso['Fecha Documento']	= self.normalizeDate(compromiso['Fecha Documento'])

		del compromiso['Tipo Vista']

		compromiso.rename(columns={'Concepto':'concepto', 'Principal':'principal', 'Monto Documento':'montoDocumento', 'Fecha':'fechaGeneracion', 'Folio':'folio', 'Título':'titulo', 'Número Documento': 'numero', 'FechaDocumento':'fechaDocumento', 'Tipo Documento':'tipoDocumento','Monto Documento.1':'monto'}, inplace=True)
	
		writer = pd.ExcelWriter('compromiso.xlsx', engine='xlsxwriter')
		compromiso.to_excel(writer, sheet_name='Todas las cuentas')
		writer.save()

		os.remove("compromiso.csv")

		database = Database()
		database.databaseCompromiso(compromiso)


