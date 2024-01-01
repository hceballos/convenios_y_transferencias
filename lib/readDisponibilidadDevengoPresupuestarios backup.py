from lib.database  import Database
from lib.readJson  import ReadJson
from datetime import datetime
from datetime import datetime, timedelta

import pandas as pd
import glob
import xlrd
import csv
import os


class ReadDisponibilidadDevengoPresupuestarios(ReadJson):

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

		disponibilidadDevengo = pd.DataFrame()
		for f in glob.glob(self.datos['DisponibilidadDeDevengo'], recursive=True):
			print('Procesando  : ', f)
			xlsls = pd.read_excel(f, index_col=0)  
			print(xlsls)

			
			writer = pd.ExcelWriter('xlsls.xlsx', engine='xlsxwriter')
			xlsls.to_excel(writer, sheet_name='Todas las cuentas')
			writer.save()
			break



			wb = xlrd.open_workbook(f)
			sheet_list = wb.sheet_names()
			sh = wb.sheet_by_name(sheet_list[0]) 
			disponibilidadDevengocsv = open('disponibilidadDevengo.csv', 'w')
			wr = csv.writer(disponibilidadDevengocsv, quoting=csv.QUOTE_ALL)
			for rownum in range(sh.nrows):
				wr.writerow(sh.row_values(rownum))
			disponibilidadDevengocsv.close()
			df1 = pd.read_csv('disponibilidadDevengo.csv', converters={ 'Número Documento': str}, encoding='utf8', skiprows=5, header=0)
			for x in df1['Fecha Documento'].astype(int):
				print(">>>> : ", type(x), x)



			#print("-------------------- : ", df1['Fecha Documento'])
			disponibilidadDevengo = disponibilidadDevengo.append(df1,ignore_index=True)


		disponibilidadDevengo['rut']				= disponibilidadDevengo['Principal'].str.split(' ', n = 1, expand = True)[0]
		disponibilidadDevengo['CodRegion']			= disponibilidadDevengo['Código Unidad Ejecutora'].str.split(' ', n = 1, expand = True)[0]
		disponibilidadDevengo['unico']				= disponibilidadDevengo['CodRegion'] + disponibilidadDevengo['rut']

		# ============================================================================================================






		disponibilidadDevengo['Fecha Documento01'] = disponibilidadDevengo['Fecha Documento'].astype(int)
		print("disponibilidadDevengo['Fecha Documento01']", type(disponibilidadDevengo['Fecha Documento01']), disponibilidadDevengo['Fecha Documento01'] )
		for x in disponibilidadDevengo['Fecha Documento01']:
			print( type(x), x)

			#timestamp = datetime.datetime.fromtimestamp(x)
			#print(x.strftime('%Y-%m-%d %H:%M:%S'))
			#print( type(x), datetimes.fromtimestamp(x / 1e3))



		#disponibilidadDevengo['InsertedDate'] = disponibilidadDevengo['Fecha Documento01'].apply(lambda x: pd.to_datetime(str(x),format='%Y%m%d'))

		"""
		print(type(disponibilidadDevengo['Fecha Documento01']), disponibilidadDevengo['Fecha Documento01'] )
		for x in disponibilidadDevengo['Fecha Documento01']:
			print(">>>> : ", type(x), x)
			print( pd.to_datetime(x, format='%Y%m%d') )

		disponibilidadDevengo['a'] = pd.to_numeric(disponibilidadDevengo['Fecha Documento01']).round(0).astype(int)
		"""





		#disponibilidadDevengo['b'] = pd.to_datetime(disponibilidadDevengo['Fecha Documento']).dt.date





		#disponibilidadDevengo['c'] = pd.to_datetime(disponibilidadDevengo['b'] )


		#print("===== ", type(disponibilidadDevengo['Fecha Documento']), disponibilidadDevengo['Fecha Documento'])
		#print("disponibilidadDevengo['a'] ", type(disponibilidadDevengo['a']), disponibilidadDevengo['a'])












		#disponibilidadDevengo['x0']					= str(disponibilidadDevengo['Fecha Documento'])

		#print(type(disponibilidadDevengo['x0']), disponibilidadDevengo['x0'])


		# ============================================================================================================


		#disponibilidadDevengo['Fecha2'] = pd.to_datetime(disponibilidadDevengo['Fecha Documento'])
		#disponibilidadDevengo['Fecha1']				= pd.to_datetime(disponibilidadDevengo['Fecha Documento']).dt.date
		#disponibilidadDevengo['Fecha2']	= self.normalizeDate(disponibilidadDevengo['Fecha1'])


		"""
		#disponibilidadDevengo['Tipo Vista']		= disponibilidadDevengo.drop( disponibilidadDevengo[ disponibilidadDevengo['Tipo Vista'] == 'Saldo Inicial' ].index , inplace=True )
		disponibilidadDevengo['Fecha Documento']	= self.normalizeDate(disponibilidadDevengo['Fecha Documento'])
		disponibilidadDevengo['Fecha Documento']	= pd.to_datetime(disponibilidadDevengo['Fecha Documento']).dt.date
		disponibilidadDevengo['Fecha Generación']	= self.normalizeDate(disponibilidadDevengo['Fecha Generación'])
		disponibilidadDevengo['Fecha Generación']	= pd.to_datetime(disponibilidadDevengo['Fecha Generación']).dt.date
		disponibilidadDevengo['rut']				= disponibilidadDevengo['Principal'].str.split(' ', n = 1, expand = True)[0]
		disponibilidadDevengo['CodConcepto']		= disponibilidadDevengo['Concepto'].str.split(' ', n = 1, expand = True)[0]
		disponibilidadDevengo['unico']			= disponibilidadDevengo['rut'] + disponibilidadDevengo['Número Documento']
		#disponibilidadDevengo['ordenDeCompra'] 	= "pendiente"
		#disponibilidadDevengo['status'] 			= "pendiente"
		disponibilidadDevengo['Monto Documento.1']= self.normalizeNumeric(disponibilidadDevengo['Monto Documento.1'])
		disponibilidadDevengo['Monto Documento']	= self.normalizeNumeric(disponibilidadDevengo['Monto Documento'])
		
		#del disponibilidadDevengo['Tipo Vista']
		disponibilidadDevengo['year']	= pd.DatetimeIndex(disponibilidadDevengo['Fecha Generación']).year
		disponibilidadDevengo['mes']	= pd.DatetimeIndex(disponibilidadDevengo['Fecha Generación']).month


		disponibilidadDevengo.rename(columns={'Concepto':'concepto', 'Principal':'principal', 'Monto Documento':'montoDocumento', 'Fecha Generación':'fechaGeneracion', 'Folio':'folio', 'Título':'titulo', 'Número Documento': 'numero', 'Fecha Documento':'fechaDocumento', 'Tipo Documento':'tipoDocumento','Monto Documento.1':'monto'}, inplace=True)
		"""

		
		writer = pd.ExcelWriter('disponibilidadDevengo.xlsx', engine='xlsxwriter')
		disponibilidadDevengo.to_excel(writer, sheet_name='Todas las cuentas')
		writer.save()
		
		#os.remove("disponibilidadDevengo.csv")

		database = Database()
		database.databaseDisponibilidadDevengo(disponibilidadDevengo)


