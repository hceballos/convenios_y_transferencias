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


class Informe_reportePago(object):


	def __init__(self):

		# Quiz()
		
		self.selectSubCategorias()

	def selectSubCategorias(self):
		cnx = sqlite3.connect('database.db')
		consulta = " \
		SELECT \
			pago.*, \
			retencion.* \
		FROM \
			( \
			SELECT \
			reportePago.* \
		FROM reportePagO) pago \
		LEFT JOIN \
			( \
			SELECT \
			retenciones.'Periodo de Atención a Levantar o Retener', \
			retenciones.'Código ', \
			retenciones.'SI Presenta Rend. De Cuenta', \
			retenciones.'NO Presenta Rend. De Cuenta' \
			FROM \
			retenciones) retencion \
		ON pago.'COD PROYECTO' = retencion.'Código ' and pago.'MES ATENCION' = retencion.'Periodo de Atención a Levantar o Retener' \
		"
		reportePago = pd.read_sql_query(consulta, cnx)

		# ----------------------------------------------------------------------------------------------

		writer = pd.ExcelWriter('informe_reportePago.xlsx', engine='xlsxwriter')
		reportePago.to_excel(writer, sheet_name='informe_reportePagos')
		writer.save()


if __name__ == '__main__':
	Informe_reportePago()
