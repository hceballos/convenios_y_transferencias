import sqlalchemy
import pandas as pd
import glob
import sqlite3
import numpy as np
from datetime import datetime
from datetime import date
import re
import xlrd
import csv
import os


class InformeRequerimiento(object):


	def __init__(self):		

		self.selectSubCategorias()

	def selectSubCategorias(self):
		cnx = sqlite3.connect('database.db')
		consulta = " \
			SELECT \
				DisponibilidadCompromiso.* \
			FROM \
				DisponibilidadCompromiso \
			WHERE \
				DisponibilidadCompromiso.'Concepto Presupuesto' like '2401%' \
				and DisponibilidadCompromiso.'Catálogo 04'  != 'MetasAdicionales - 01 META 80 BIS' \
			GROUP BY \
				DisponibilidadCompromiso.'unico' \
			HAVING \
				Sum(DisponibilidadCompromiso.'Monto Vigente') \
		"
		DisponibilidadCompromiso = pd.read_sql_query(consulta, cnx)
		DisponibilidadCompromiso.rename(columns={1 :'Ene', 2 :'Feb', 3 :'Mar', 4 :'Abr', 5 :'May', 6 :'Jun', 7 :'Jul', 8 :'Ago', 9 :'Sep', 10 :'Oct', 11 :'Nov', 12 :'Dic', 'Principal':'principal', 'Monto Documento':'montoDocumento', 'Fecha Generación':'fechaGeneracion', 'Folio':'folio', 'Título':'titulo', 'Número Documento': 'numero', 'Fecha Documento':'fechaDocumento', 'Tipo Documento':'tipoDocumento','Monto Documento.1':'monto'}, index={'Concepto':'Linea de acción'}, inplace=True)

		# ----------------------------------------------------------------------------------------------
		cnx = sqlite3.connect('database.db')
		consulta = " \
			SELECT \
				DisponibilidadDevengo.* \
			FROM \
				DisponibilidadDevengo \
			WHERE \
				DisponibilidadDevengo.'Concepto Presupuestario' like '2401%' \
				and DisponibilidadDevengo.'Catálogo 04' != 'MetasAdicionales - 01 META 80 BIS' \
		"
		DisponibilidadDevengo = pd.read_sql_query(consulta, cnx)
		DisponibilidadDevengo.rename(columns={1 :'Ene', 2 :'Feb', 3 :'Mar', 4 :'Abr', 5 :'May', 6 :'Jun', 7 :'Jul', 8 :'Ago', 9 :'Sep', 10 :'Oct', 11 :'Nov', 12 :'Dic', 'Principal':'principal', 'Monto Documento':'montoDocumento', 'Fecha Generación':'fechaGeneracion', 'Folio':'folio', 'Título':'titulo', 'Número Documento': 'numero', 'Fecha Documento':'fechaDocumento', 'Tipo Documento':'tipoDocumento','Monto Documento.1':'monto'}, index={'Concepto':'Linea de acción'}, inplace=True)
		
		# ----------------------------------------------------------------------------------------------
		frames = [DisponibilidadCompromiso, DisponibilidadDevengo]
		result = pd.merge(DisponibilidadCompromiso, DisponibilidadDevengo, how="right", on=["unico", "unico"])


		writer = pd.ExcelWriter('InformeRequerimiento01.xlsx', engine='xlsxwriter')
		DisponibilidadCompromiso.to_excel(writer, sheet_name='DisponibilidadCompromiso')
		DisponibilidadDevengo.to_excel(writer, sheet_name='DisponibilidadDevengo')
		result.to_excel(writer, sheet_name='df')
		writer.save()



