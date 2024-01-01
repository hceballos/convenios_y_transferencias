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


class ReadRetencionesTemporal(object):

	def CampoCalculadoFechaActual(self):
		anio = datetime.datetime.now().year
		d = datetime.date.today()
		mes = '{:02d}'.format(d.month-1)
		merge = str(anio)+str(mes)
		return int(merge)

	def __init__(self, datos):
		self.datos = datos

		try:
			os.remove("consolidado Retenciones.xlsx")
		except Exception as e:
			pass

		acepta = pd.DataFrame()
		for f in glob.glob(self.datos['readRetenciones'], recursive=True):
			if "ruce" in f:
				pass
			else:
				print('Procesando  : ', f)
				wb = xlrd.open_workbook(f)
				pestania = wb.sheet_names()
				sh = wb.sheet_by_name(pestania[0])
				aceptacsv = open('acepta.csv', 'w')
				wr = csv.writer(aceptacsv, quoting=csv.QUOTE_ALL)
				for rownum in range(sh.nrows):
					wr.writerow(sh.row_values(rownum))
				aceptacsv.close()
				df = pd.read_csv('acepta.csv' ,encoding='utf-8')
				df.rename(columns={ 'Fecha de Recepción':'Fecha de recepción', 
									'Fecha Recepción'	:'Fecha de recepción',
									'Fecha de Recepción':'Fecha de recepción',
									'Fecha de recepción':'Fecha de recepción'
									}, inplace=True)
				acepta = acepta.append(df,ignore_index=True)

		acepta['Monto de la R.C.'] = acepta['Monto de la R.C.'].replace(np.nan, 0)
		#acepta["Fecha de recepción"] = pd.to_numeric(df["Fecha de recepción"])
		#print("acepta['Fecha de recepción']", type(acepta["Fecha de recepción"]), acepta["Fecha de recepción"])

		try:
			del acepta['Llave Unica']
			del acepta['LLAVE SI']
			del acepta['LLAVE NO']
			del acepta['Contar Llave Unica']
			del acepta['Cruce con Pago']
			del acepta['OBSERVACIÓN UPP']
			del acepta['Unnamed: 21']
			del acepta['Unnamed: 11']	
			del acepta['1.0']
		except Exception as e:
			pass

		acepta['MesActual']	= self.CampoCalculadoFechaActual()


		acepta.loc[acepta['MesActual'] == acepta['Periodo de Atención a Levantar o Retener'], 'equal_or_lower_than_4?'] = 'True'
		acepta.loc[acepta['MesActual'] != acepta['Periodo de Atención a Levantar o Retener'], 'equal_or_lower_than_4?'] = 'FALSO'



		print (df)


		#pestanas =  list(dict.fromkeys(re.findall('VisualizaVariacionPopup:nvPnDet:docum_\d|VisualizaOtrosDocsPopup:nvPnDet:docum_\d', driver.page_source)))


		# _______________________________________________________________________________
		database = Database()
		database.databaseRetenciones(acepta)
		# _______________________________________________________________________________

		acepta = acepta.sort_values('Fecha de recepción', ascending=False)

		writer = pd.ExcelWriter(r'consolidado Retenciones.xlsx', engine='xlsxwriter')
		acepta.to_excel(writer, sheet_name='Detalle')
		writer.save()
		os.remove("acepta.csv")