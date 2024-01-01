from lib.database  import Database
from lib.readJson  import ReadJson
import sqlalchemy
import pandas as pd
import glob
import sqlite3
import xlrd
import csv
import os
import re
import sys

class ReadReportePago(object):

	def __init__(self, datos):
		self.datos = datos

		acepta = pd.DataFrame()
		for f in glob.glob(self.datos['readReportePago'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f) 
			acepta = acepta.append(df)
		#print(acepta)
		# _______________________________________________________________________________
		database = Database()
		database.databaseReportePago(acepta)
		# _______________________________________________________________________________
		writer = pd.ExcelWriter(r'ReportePago.xlsx', engine='xlsxwriter')
		acepta.to_excel(writer, sheet_name='Detalle')
		writer.save()



class Pago(ReadJson):

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		fes = pd.DataFrame()
		for f in glob.glob(datos['reporte_FES'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f) 
			fes = fes.append(df)
		print(fes.columns)
		print("Clase fes")

		database = Database()
		database.databaseFes(fes)

		writer = pd.ExcelWriter(r'fes.xlsx', engine='xlsxwriter')
		fes.to_excel(writer, sheet_name='Detalle')
		writer.save()

		# _______________________________________________________________________________


		masivo = pd.DataFrame()
		for f in glob.glob(datos['pagoMasivo'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f) 
			masivo = masivo.append(df)
		print(masivo.columns)
		print("Clase masivo")

		database = Database()
		database.databaseMasivo(masivo)

		writer = pd.ExcelWriter(r'masivo.xlsx', engine='xlsxwriter')
		masivo.to_excel(writer, sheet_name='Detalle')
		writer.save()

class CalculoPago(object):

	def __init__(self):

		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				f.'ARCHIVO', \
				f.'Folio', \
				f.'codproyecto', \
				f.'mesano', \
				r.'Código ', \
				r.'Periodo de Atención a Levantar o Retener', \
				m.'Cod. Proyecto', \
				m.'Mes Atención', \
				r.'SI Presenta Rend. De Cuenta', \
				r.'NO Presenta Rend. De Cuenta', \
				m.'Monto Líquido A Pago' \
			FROM \
				(SELECT fes.* FROM fes)f \
				LEFT JOIN(SELECT * FROM  retenciones WHERE (retenciones.'Fecha de Recepción') IN (SELECT Max(retenciones.'Fecha de Recepción') FROM retenciones GROUP BY retenciones.'Periodo de Atención a Levantar o Retener' ORDER BY	retenciones.'Periodo de Atención a Levantar o Retener' DESC) ORDER BY retenciones.'Fecha de Recepción' DESC, retenciones.'Periodo de Atención a Levantar o Retener' DESC )r ON f.codproyecto = r.'Código ' and f.mesano = r.'Periodo de Atención a Levantar o Retener' \
				LEFT JOIN(SELECT masivo.* FROM masivo)m ON f.codproyecto	= m.'Cod. Proyecto' \
			WHERE \
				f.'codproyecto' = r.'Código ' \
				and  f.'codproyecto' = m.'Cod. Proyecto' \
				and f.'mesano' = r.'Periodo de Atención a Levantar o Retener' \
				and f.'mesano' = m.'Mes Atención' \
				and f.'ARCHIVO' = 'SUBVENCION' \
				and r.'SI Presenta Rend. De Cuenta' like '%' \
		"
		query = pd.read_sql_query(consulta, cnx)


		consulta  = " \
			SELECT \
				f.'ARCHIVO', \
				f.'codproyecto', \
				f.'mesano', \
				r.'Código ', \
				r.'Periodo de Atención a Levantar o Retener', \
				m.'Cod. Proyecto', \
				m.'Mes Atención', \
				r.'SI Presenta Rend. De Cuenta', \
				r.'NO Presenta Rend. De Cuenta', \
				m.'Monto Líquido A Pago' \
			FROM \
				(SELECT fes.* FROM fes)f \
				LEFT JOIN(SELECT * FROM  retenciones WHERE (retenciones.'Fecha de Recepción') IN (SELECT Max(retenciones.'Fecha de Recepción') FROM retenciones GROUP BY retenciones.'Periodo de Atención a Levantar o Retener' ORDER BY	retenciones.'Periodo de Atención a Levantar o Retener' DESC) ORDER BY retenciones.'Fecha de Recepción' DESC, retenciones.'Periodo de Atención a Levantar o Retener' DESC )r ON f.codproyecto = r.'Código ' and f.mesano = r.'Periodo de Atención a Levantar o Retener' \
				LEFT JOIN(SELECT masivo.* FROM masivo)m ON f.codproyecto	= m.'Cod. Proyecto' \
			WHERE \
				f.'ARCHIVO' = 'SUBVENCION' \
		"
		ALL = pd.read_sql_query(consulta, cnx)


		consulta  = " \
			SELECT \
				f.'ARCHIVO', \
				f.'Folio', \
				f.'codproyecto', \
				f.'mesano', \
				r.'Código ', \
				r.'Periodo de Atención a Levantar o Retener', \
				m.'Cod. Proyecto', \
				m.'Mes Atención', \
				r.'SI Presenta Rend. De Cuenta', \
				r.'NO Presenta Rend. De Cuenta', \
				m.'Monto Líquido A Pago' \
			FROM \
				(SELECT fes.* FROM fes)f \
				LEFT JOIN(SELECT * FROM  retenciones WHERE (retenciones.'Fecha de Recepción') IN (SELECT Max(retenciones.'Fecha de Recepción') FROM retenciones GROUP BY retenciones.'Periodo de Atención a Levantar o Retener' ORDER BY	retenciones.'Periodo de Atención a Levantar o Retener' DESC) ORDER BY retenciones.'Fecha de Recepción' DESC, retenciones.'Periodo de Atención a Levantar o Retener' DESC )r ON f.codproyecto = r.'Código ' and f.mesano = r.'Periodo de Atención a Levantar o Retener' \
				LEFT JOIN(SELECT masivo.* FROM masivo)m ON f.codproyecto	= m.'Cod. Proyecto' \
			WHERE \
				f.'ARCHIVO' = 'SUBVENCION' \
				and f.'Folio' like '%u%' \
		"
		urgencia = pd.read_sql_query(consulta, cnx)

		writer = pd.ExcelWriter('X.xlsx', engine='xlsxwriter')
		query.to_excel(writer, sheet_name='Calculos previos a pago')
		ALL.to_excel(writer, sheet_name='Todo')
		urgencia.to_excel(writer, sheet_name='urgencia')
		writer.save()


