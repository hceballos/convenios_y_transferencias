import pandas as pd
import sqlite3
import sqlalchemy
import numpy as np
from datetime import datetime
from datetime import date
import xlsxwriter
import glob
import os
from datetime import datetime
from lib.centralizacion.analisis.analisis import Analisis
#from lib.centralizacion.scrapy import Scrapy
from lib.centralizacion.scrapyProceso.setup import Setup


class Informes(object):

	def rendicionDeCuentas(self, writer, cnx, nombre_archivo, f):
		now = datetime.now()
		year = now.year
		month = now.month-1
		periodo = f"{year}{month:02d}"
		
		variable_periodo = "variable_periodo"
		#periodo = input("ingresa el periodo de atencion que vas a trabajar, se sugiere " + periodo + ', Ingresa el periodo : ')
		periodo = '202311'

		with open(f, 'r') as file:
			consulta_template = file.read()
			consulta_modificada = consulta_template.replace(f'{{{variable_periodo}}}', periodo)
			#print(consulta_modificada)
			df = pd.read_sql_query(consulta_modificada, cnx)
			analisis = Analisis()
			df = analisis.analisis_Rendiciones(df)




			# ========================================================================================================
			"""
			condicion = abs(df['Diferencia']) > 100
			filas_cumplen_condicion = df.loc[condicion]
			for index, row in filas_cumplen_condicion.iterrows():
				print(row['Diferencia'])
				filas_cumplen_condicion = df.loc[condicion]
				filas_cumplen_condicion['MES_ATENCION'] = filas_cumplen_condicion['mes_atencion']
				filas_cumplen_condicion['COD_PROYECTO'] = filas_cumplen_condicion['cod_proyecto']

			driver = Setup(filas_cumplen_condicion)
			"""
			# ========================================================================================================




			df.to_excel(writer, sheet_name=nombre_archivo, index=False)

	def __init__(self):
		
		writer = pd.ExcelWriter(r'./output/Centralizacion.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
		cnx = sqlite3.connect('centralizacion.db')

		for f in glob.glob('./lib/centralizacion/querys/*.txt', recursive=True):
			nombre_archivo, _ = os.path.splitext(os.path.basename(f))
			# print(nombre_archivo)
			# if nombre_archivo == 'rendicionDeCuentas':
			self.rendicionDeCuentas(writer, cnx, nombre_archivo, f)

		# Obtener el objeto workbook y la hoja de trabajo
		workbook = writer.book
		worksheet = writer.sheets['5.mallaTodosLosPagos']

		# Agregar formato a cada columna
		rojo 	= workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
		verde 	= workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
		azul 	= workbook.add_format({'bg_color': '#BDD7EE', 'font_color': '#1F497D'})
		beige 	= workbook.add_format({'bg_color': '#eee9bd', 'font_color': '#1F497D'})

		worksheet.set_column('B:B', 	None, verde)
		worksheet.set_column('D:D', 	None, verde)
		worksheet.set_column('G:G', 	None, verde)
		worksheet.set_column('Y:Y', 	None, verde)
		worksheet.set_column('BA:BC', 	None, verde)
		#worksheet.set_column('BA:BA', 	None, beige)
		worksheet.set_column('BE:BE', 	None, beige)


		# Fijar la fila superior
		worksheet.freeze_panes(1, 0)  # Fijar la fila superior

		# Aplicar un filtro a la columna deseada
		worksheet.autofilter('A1:BM1')  # Filtrar la columna 'columna1'

		writer.save()