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


class ReadPagoManual(object):

	def CampoCalculadoFechaActual(self):
		anio = datetime.datetime.now().year
		d = datetime.date.today()
		mes = '{:02d}'.format(d.month-1)
		merge = str(anio)+str(mes)
		return int(merge)

	def __init__(self, datos):
		self.datos = datos

		acepta = pd.DataFrame()
		for f in glob.glob(self.datos['readPagoManual'], recursive=True):
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



		del acepta['observacion']
		del acepta['OBSERVACIÓN']


		acepta['MesActual']	= self.CampoCalculadoFechaActual()

		# _______________________________________________________________________________
		database = Database()
		database.databasePagoManual(acepta)
		# _______________________________________________________________________________

		writer = pd.ExcelWriter(r'pagoManual.xlsx', engine='xlsxwriter')
		acepta.to_excel(writer, sheet_name='Detalle')
		writer.save()
		os.remove("acepta.csv")