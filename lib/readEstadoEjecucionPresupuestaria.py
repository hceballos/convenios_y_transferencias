from lib.database  import Database
from lib.readJson  import ReadJson
import pandas as pd
import glob
import xlrd
import csv
import os


class ReadEstadoEjecucionPresupuestaria(ReadJson):

	def normalizeDateConta(self, dateString):
		return dateString.replace(['(\d{2}).(\d{2}).(\d{2})?(\d{2})'], ['\g<4>-\g<2>-\g<1>'], regex=True)

	def normalizeDate(self, dateString):
		return dateString.replace(['(\d{2})\/(\d{2})\/(\d{4})'], ['\g<3>-\g<2>-\g<1>'], regex=True)

	def normalizeNumeric(self, string):
		string	= [w.replace(',0', '' ) for w in string ]
		return pd.to_numeric(string)

	def normalizeFloat64ToString(self, numero):
		print(type(numero))
		numeroInString = numero.astype(str)
		print(type(numeroInString))
		return numero

	def normalizeStringToInt(self, numero):
		print(type(numero))
		numeroInString = numero.astype(int)
		print(type(numeroInString))
		return numero

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		clasificador = pd.DataFrame()
		for f in glob.glob(self.datos['clasificador'], recursive=True):
			df = pd.read_excel(f, converters={ 'NumeroRegion': str } )
			print('Procesando  : ', f)
			clasificador = clasificador.append(df,ignore_index=True)

		database = Database()
		database.databaseClasificador(clasificador)



		estadoEjecucionPresupuestaria = pd.DataFrame()
		for f in glob.glob(self.datos['EstadoEjecucionPresupuestaria'], recursive=True):
			print('Procesando  : ', f)
			wb = xlrd.open_workbook(f)
			sheet_list = wb.sheet_names()
			sh = wb.sheet_by_name(sheet_list[0]) 
			estadoEjecucionPresupuestariacsv = open('estadoEjecucionPresupuestaria.csv', 'w')
			wr = csv.writer(estadoEjecucionPresupuestariacsv, quoting=csv.QUOTE_ALL)
			for rownum in range(sh.nrows):
				wr.writerow(sh.row_values(rownum))
			estadoEjecucionPresupuestariacsv.close()
			df1 = pd.read_csv('estadoEjecucionPresupuestaria.csv', converters={ 'Número Documento': str }, encoding='utf8', skiprows=7, header=0)
			estadoEjecucionPresupuestaria = estadoEjecucionPresupuestaria.append(df1,ignore_index=True)
		
		writer = pd.ExcelWriter('estadoEjecucionPresupuestaria.xlsx', engine='xlsxwriter')
		estadoEjecucionPresupuestaria.to_excel(writer, sheet_name='Todas las cuentas')
		writer.save()
		os.remove("estadoEjecucionPresupuestaria.csv")
		database = Database()
		database.databaseEstadoEjecucionPresupuestaria(estadoEjecucionPresupuestaria)

		# ===========================================================================================

		estadoEjecucionPresupuestariaAvanzado = pd.DataFrame()
		for f in glob.glob(self.datos['EstadoEjecucionPresupuestariaAvanzado'], recursive=True):
			print('Procesando  : ', f)
			wb = xlrd.open_workbook(f)
			sheet_list = wb.sheet_names()
			sh = wb.sheet_by_name(sheet_list[0]) 
			estadoEjecucionPresupuestariaAvanzadocsv = open('estadoEjecucionPresupuestariaAvanzado.csv', 'w')
			wr = csv.writer(estadoEjecucionPresupuestariaAvanzadocsv, quoting=csv.QUOTE_ALL)
			for rownum in range(sh.nrows):
				wr.writerow(sh.row_values(rownum))
			estadoEjecucionPresupuestariaAvanzadocsv.close()
			df1 = pd.read_csv('estadoEjecucionPresupuestariaAvanzado.csv', converters={ 'Número Documento': str }, encoding='utf8', skiprows=7, header=0)
			estadoEjecucionPresupuestariaAvanzado = estadoEjecucionPresupuestariaAvanzado.append(df1,ignore_index=True)

		estadoEjecucionPresupuestariaAvanzado['CodRegion'] = estadoEjecucionPresupuestariaAvanzado['Concepto Presupuestario'].str.split(' ', n = 1, expand = True)[0]



		#numero =  estadoEjecucionPresupuestariaAvanzado['Unidades Demandantes'].str.split(' ', n = 1, expand = True)[0] 

		#estadoEjecucionPresupuestariaAvanzado['NumeroRegion0'] = pd.to_numeric(numero, downcast='integer').astype('int64')

		estadoEjecucionPresupuestariaAvanzado['NumeroRegion'] = estadoEjecucionPresupuestariaAvanzado['Unidades Demandantes'].str.split(' ', n = 1, expand = True)[0] 


		writer = pd.ExcelWriter('estadoEjecucionPresupuestariaAvanzado.xlsx', engine='xlsxwriter')
		estadoEjecucionPresupuestariaAvanzado.to_excel(writer, sheet_name='Todas las cuentas')
		writer.save()
		os.remove("estadoEjecucionPresupuestariaAvanzado.csv")
		database = Database()
		database.databaseEstadoEjecucionPresupuestariaAvanzado(estadoEjecucionPresupuestariaAvanzado)

