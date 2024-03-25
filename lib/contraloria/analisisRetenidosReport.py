import sqlite3
import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente
import re
from datetime import date


class AnalisisRetenidosReport(Fuente):
	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos
 
		self.parse_Excel(datos)
 
	def parse_Excel(self, datos):
		cnx = sqlite3.connect('AnalisisRetenidos.db')
		consulta  = " \
			SELECT \
				scrapy.* \
			FROM \
				scrapy \
		"
		query = pd.read_sql_query(consulta, cnx)


		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - AnalisisRetenidos Report.xlsx', engine='xlsxwriter')
		query.to_excel(writer, sheet_name='80Bis')


		# ==================================================================================================
		# Obtener el objeto workbook y la hoja de trabajo
		workbook = writer.book
		worksheet = writer.sheets['80Bis']

		# Agregar formato a cada columna
		rojo  = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
		verde = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
		azul  = workbook.add_format({'bg_color': '#BDD7EE', 'font_color': '#1F497D'})


		worksheet.set_column('E:E', None, verde)
		worksheet.set_column('J:J', None, verde)
		worksheet.set_column('L:M', None, verde)
		worksheet.set_column('R:T', None, verde)
		worksheet.set_column('AA:AA', None, verde)

		worksheet.set_column('AP:AP', None, azul)
		worksheet.set_column('AR:AR', None, azul)
		worksheet.set_column('AU:AU', None, azul)
		worksheet.set_column('BB:BB', None, azul)

		worksheet.set_column('BC:BC', None, rojo)


		# Fijar la fila superior
		worksheet.freeze_panes(1, 0)  # Fijar la fila superior

		# Aplicar un filtro a la columna deseada
		worksheet.autofilter('A1:BD1')  # Filtrar la columna 'columna1'

		# Guardar y cerrar el archivo de Excel
		writer.save()
		# ==================================================================================================