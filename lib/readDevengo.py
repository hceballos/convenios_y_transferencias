from lib.database  import Database
from lib.readJson  import ReadJson
import pandas as pd
import glob
import xlrd
import csv
import os


class ReadDevengo(ReadJson):

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

		devengo = pd.DataFrame()
		for f in glob.glob(self.datos['DevengoCarteraFinanciera'], recursive=True):
			print('Procesando  : ', f)
			wb = xlrd.open_workbook(f)
			sh = wb.sheet_by_name('Sheet1')
			devengocsv = open('devengo.csv', 'w')
			wr = csv.writer(devengocsv, quoting=csv.QUOTE_ALL)
			for rownum in range(sh.nrows):
				wr.writerow(sh.row_values(rownum))
			devengocsv.close()
			df1 = pd.read_csv('devengo.csv', converters={ 'Número Documento': str }, encoding='utf8')
			devengo = devengo.append(df1,ignore_index=True)

		devengo['Tipo Vista']		= devengo.drop( devengo[ devengo['Tipo Vista'] == 'Saldo Inicial' ].index , inplace=True )
		devengo['Fecha Documento']	= self.normalizeDate(devengo['Fecha Documento'])
		devengo['Fecha Documento']	= pd.to_datetime(devengo['Fecha Documento']).dt.date
		devengo['Fecha Generación']	= self.normalizeDate(devengo['Fecha Generación'])
		devengo['Fecha Generación']	= pd.to_datetime(devengo['Fecha Generación']).dt.date
		devengo['rut']				= devengo['Principal'].str.split(' ', n = 1, expand = True)[0]
		devengo['CodConcepto']		= devengo['Concepto'].str.split(' ', n = 1, expand = True)[0]
		devengo['unico']			= devengo['rut'] + devengo['Número Documento']
		#devengo['ordenDeCompra'] 	= "pendiente"
		#devengo['status'] 			= "pendiente"
		devengo['Monto Documento.1']= self.normalizeNumeric(devengo['Monto Documento.1'])
		devengo['Monto Documento']	= self.normalizeNumeric(devengo['Monto Documento'])
		del devengo['Tipo Vista']

		devengo['year']	= pd.DatetimeIndex(devengo['Fecha Generación']).year
		devengo['mes']	= pd.DatetimeIndex(devengo['Fecha Generación']).month


		devengo.rename(columns={'Concepto':'concepto', 'Principal':'principal', 'Monto Documento':'montoDocumento', 'Fecha Generación':'fechaGeneracion', 'Folio':'folio', 'Título':'titulo', 'Número Documento': 'numero', 'Fecha Documento':'fechaDocumento', 'Tipo Documento':'tipoDocumento','Monto Documento.1':'monto'}, inplace=True)
	
		
		writer = pd.ExcelWriter('devengo.xlsx', engine='xlsxwriter')
		devengo.to_excel(writer, sheet_name='Todas las cuentas')
		writer.save()
		
		os.remove("devengo.csv")

		database = Database()
		database.databaseDevengo(devengo)


