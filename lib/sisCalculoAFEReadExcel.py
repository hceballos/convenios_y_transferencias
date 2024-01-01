#! /bin/env python3
from datetime import date
from lib.fuente import Fuente
import os
import pandas as pd
import sys
import time
import glob
import xlrd
import shutil
import csv
import sqlalchemy
from datetime import datetime
import sqlite3
import xlsxwriter
import sqlalchemy


class ReadExcel(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)

		datos = self.datos

		#libros ={"Rendiciones" : "\\output\\*Consolidado Retenciones*", "PagosAprobados" : "\\input_excel\\calculoAFE\\PagosAprobados\\*", "PagosRetenidos" : "\\input_excel\\calculoAFE\\PagosRetenidos\\*", "ListaNegra" : "\\input_excel\\calculoAFE\\ListaNegra\\*"}
		libros ={	"Rendiciones"	 : "\\output\\*Consolidado Retenciones*", 
					"PagosAprobados" : "\\input_excel\\calculoAFE\\PagosAprobados\\*", 
					"PagosRetenidos" : "\\input_excel\\calculoAFE\\PagosRetenidos\\*", 
					"ListaNegra" 	 : "\\input_excel\\calculoAFE\\ListaNegra\\*",
					"Bis" 		 	 : "\\input_excel\\calculoAFE\\80bis\\*",
					"Urgencias" 	 : "\\input_excel\\calculoAFE\\Urgencias\\*"
				}


		for key in libros.keys():
			#print(key, " >>>>>>>>>>>>> " ,libros[key])
			if key == 'PagosAprobados' or key == 'PagosRetenidos':
				print(key, "	: " ,libros[key])
				for f in glob.glob(os.path.join(os.getcwd()) +libros[key], recursive=True):
					df = pd.read_excel(f, converters={ 'COD PROYECTO': str, 'MES ATENCION': str, 'Periodo de Atención a Levantar o Retener': str , 'Código ': str }  )
					df.rename(columns={	"Periodo de Atención a Levantar o Retener": "MES ATENCION", "Código ": "COD PROYECTO"}, inplace=True)
					df['unico']	= df['COD PROYECTO'] + df['MES ATENCION']
					df['SI Presenta Rend. De Cuenta ANTES'] = "Pendiente"
					df['SI Presenta Rend. De Cuenta AHORA'] = "Pendiente"
					df['80Bis'] = "Pendiente"
					df['Urgencias'] = "Pendiente"
					df['Esta en Lista Negra'] = "Pendiente"
					df['ANALISIS'] = "Pendiente"
					self.toDataBase(key, f, df)

			else:
				print(key, "	: " ,libros[key])
				for f in glob.glob(os.path.join(os.getcwd()) +libros[key], recursive=True):
					df = pd.read_excel(f, converters={'MES ATENCION': str, 'mesano': str, 'codproyecto': str, 'COD PROYECTO': str, 'Periodo de Atención a Levantar o Retener': str , 'Código ': str , 'Mes Atención ': str }  )
					df.rename(columns={
										"codproyecto": "COD PROYECTO", 
										"mesano": "MES ATENCION", 
										"Mes Atención": "MES ATENCION", 
										"Periodo de Atención a Levantar o Retener": "MES ATENCION", 
										"Código ": "COD PROYECTO", 
										"Cod. Proyecto ": "COD PROYECTO", 
										"Cod. Proyecto": "COD PROYECTO"
									}, inplace=True)

					df['unico']	= df['COD PROYECTO'] + df['MES ATENCION']
					df['SI Presenta Rend. De Cuenta ANTES']		= "Pendiente"
					df['SI Presenta Rend. De Cuenta AHORA'] 	= "Pendiente"
					df['80Bis'] 	= "Pendiente"
					df['Urgencias'] 	= "Pendiente"
					df['Esta en Lista Negra'] = "Pendiente"
					df['ANALISIS'] = "Pendiente"

					self.toDataBase(key, f, df)

		#self.todo()



		"""
		for key in libros.keys():
			print(key, " >>>>>>>>>>>>> " ,libros[key])
			for f in glob.glob(os.path.join(os.getcwd()) +libros[key], recursive=True):
				df = pd.read_excel(f, converters={ 'COD PROYECTO': str, 'MES ATENCION': str, 'Periodo de Atención a Levantar o Retener': str , 'Código ': str }  )
				df.rename(columns={	"Periodo de Atención a Levantar o Retener": "MES ATENCION", "Código ": "COD PROYECTO"}, inplace=True)
				df['unico']	= df['COD PROYECTO'] + df['MES ATENCION']
				df['SI Presenta Rend. De Cuenta ANTES']		= "Pendiente"
				df['SI Presenta Rend. De Cuenta AHORA'] 	= "Pendiente"
				df['Esta en Lista Negra'] = "Pendiente"
				df['ANALISIS'] = "Pendiente"
				self.toDataBase(key, f, df)
		"""


	def toDataBase(self, key, f, df):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///AFE.db', echo=False)
		metadata = sqlalchemy.MetaData()

		Asigfe = sqlalchemy.Table(
			key,
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
		)
		metadata.create_all(engine)
		df.to_sql(key, engine, if_exists='replace')




	def todo(self):

		cnx = sqlite3.connect('AFE.db')
		query  = " \
			SELECT \
				pa.*, \
				r.'Fecha de Recepción' as 'Fecha de Recepción de RC', \
				r.'SI Presenta Rend. De Cuenta', \
				r.'NO Presenta Rend. De Cuenta', \
				ln.'LISTA NEGRA', \
				bis.'Monto Total' as 'Monto - 80 Bis', \
				u.'Monto Líquido A Pago' as 'Monto - Urgencias' \
			FROM \
				(SELECT PagosAprobados.* FROM PagosAprobados)pa \
				LEFT JOIN(SELECT DISTINCT(Rendiciones.'unico'), MAX(Rendiciones.'Fecha de Recepción'), Rendiciones.*  FROM Rendiciones GROUP BY Rendiciones.'unico' ORDER by Rendiciones.'Fecha de Recepción')r ON pa.unico = r.unico \
				LEFT JOIN(SELECT ListaNegra.* FROM ListaNegra)ln ON pa.unico = ln.unico \
				LEFT JOIN(SELECT Bis.'COD PROYECTO' || Bis.'MES ATENCION' as 'unico2', Bis.* FROM Bis)bis ON pa.unico = bis.unico2 and pa.'TIPO PAGO' = bis.Tipo \
				LEFT JOIN(SELECT Urgencias.* FROM Urgencias)u ON pa.unico = u.unico and pa.'TIPO PAGO' = u.Tipo \
			"
		Aprobados = pd.read_sql_query(query, cnx)

		Aprobados['Diferencia Monto - 80 Bis'] = ""
		Aprobados['Diferencia Monto - Urgencias'] = ""
		Aprobados['ANALISIS'] = "Pendiente"

		#writer = pd.ExcelWriter('AFE Aprobados.xlsx', engine='xlsxwriter')
		#Aprobados.to_excel(writer, sheet_name='Pagos Aprobados', index=False, columns=['unico'])
		#Aprobados.to_excel(writer, sheet_name='Pagos Aprobados', index=False)

		writer = pd.ExcelWriter('AFE Aprobados.xlsx', engine='xlsxwriter')

		# Escribir el DataFrame en el archivo de Excel
		Aprobados.to_excel(writer, sheet_name='Aprobados', index=False)

		# Obtener el objeto workbook y la hoja de trabajo
		workbook = writer.book
		worksheet = writer.sheets['Aprobados']

		# Agregar formato a las columnas deseadas
		formato_columnas = workbook.add_format({'bg_color': '#f5e79e', 'font_color': '#000300'})
		columnas_a_colorear = ['D', 'F', 'I','J', 'R', 'Z','AQ', 'AZ', 'BA', 'BB', 'BG']  # Columnas 'columna1' y 'columna2'
		for columna in columnas_a_colorear:
		    worksheet.set_column(f'{columna}:{columna}', None, formato_columnas)

		# Fijar la fila superior
		worksheet.freeze_panes(1, 0)  # Fijar la fila superior

		# Aplicar un filtro a la columna deseada
		worksheet.autofilter('A1:BE1')  # Filtrar la columna 'columna1'

		# Guardar y cerrar el archivo de Excel
		writer.save()




		cnx = sqlite3.connect('AFE.db')
		query  = " \
			SELECT \
				pr.*, \
				r.'Fecha de Recepción' as 'Fecha de Recepción de RC', \
				r.'SI Presenta Rend. De Cuenta', \
				r.'NO Presenta Rend. De Cuenta', \
				ln.'LISTA NEGRA', \
				bis.'Monto Total' as 'Monto - 80 Bis', \
				u.'Monto Líquido A Pago' as 'Monto - Urgencias' \
			FROM \
				(SELECT PagosRetenidos.* FROM PagosRetenidos)pr \
				LEFT JOIN(SELECT DISTINCT(Rendiciones.'unico'), MAX(Rendiciones.'Fecha de Recepción'), Rendiciones.*  FROM Rendiciones GROUP BY Rendiciones.'unico' ORDER by Rendiciones.'Fecha de Recepción')r ON pr.unico = r.unico \
				LEFT JOIN(SELECT ListaNegra.* FROM ListaNegra)ln ON pr.unico = ln.unico \
				LEFT JOIN(SELECT Bis.'COD PROYECTO' || Bis.'MES ATENCION' as 'unico2', Bis.* FROM Bis)bis ON pr.unico = bis.unico2 and pr.'TIPO PAGO' = bis.Tipo \
				LEFT JOIN(SELECT Urgencias.* FROM Urgencias)u ON pr.unico = u.unico and pr.'TIPO PAGO' = u.Tipo \
			"
		Retenidos = pd.read_sql_query(query, cnx)

		Retenidos['Diferencia Monto - 80 Bis'] = ""
		Retenidos['Diferencia Monto - Urgencias'] = ""
		Retenidos['ANALISIS'] = "Pendiente"


		#writer = pd.ExcelWriter('AFE Retenidos.xlsx', engine='xlsxwriter')
		#Retenidos.to_excel(writer, sheet_name='Pagos Retenidos')
		#writer.save()

		writer = pd.ExcelWriter('AFE Retenidos.xlsx', engine='xlsxwriter')

		# Escribir el DataFrame en el archivo de Excel
		Retenidos.to_excel(writer, sheet_name='Retenidos', index=False)

		# Obtener el objeto workbook y la hoja de trabajo
		workbook = writer.book
		worksheet = writer.sheets['Retenidos']

		# Agregar formato a las columnas deseadas
		formato_columnas = workbook.add_format({'bg_color': '#f5e79e', 'font_color': '#000300'})
		columnas_a_colorear = ['D', 'F', 'I','J', 'R', 'Z','AQ', 'AZ', 'BA', 'BB', 'BG']  # Columnas 'columna1' y 'columna2'
		for columna in columnas_a_colorear:
		    worksheet.set_column(f'{columna}:{columna}', None, formato_columnas)

		# Fijar la fila superior
		worksheet.freeze_panes(1, 0)  # Fijar la fila superior

		# Aplicar un filtro a la columna deseada
		worksheet.autofilter('A1:BE1')  # Filtrar la columna 'columna1'

		# Guardar y cerrar el archivo de Excel
		writer.save()