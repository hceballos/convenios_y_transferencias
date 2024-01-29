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
#from lib.resolucionesUrgencia.analisis.analisis import Analisis


class Informes(object):

	def __init__(self):
		
		cnx = sqlite3.connect('contraloria.db')
		consulta  = " \
			SELECT \
				scrapy.* \
			FROM \
				scrapy \
			ORDER BY \
				scrapy.'Cod_Proyecto', \
			    CAST(scrapy.'ID_Pago' AS INTEGER) DESC \
		"
		query = pd.read_sql_query(consulta, cnx)

		query['80B_Bis_Plazas'] = pd.to_numeric(query['80B_Bis_Plazas'], errors='coerce')

		# Reemplazar NaN con algún valor, por ejemplo, 0
		query['80B_Bis_Plazas'].fillna(0, inplace=True)

		# Convierte la columna a tipo entero
		query['80B_Bis_Plazas'] = query['80B_Bis_Plazas'].astype(int)


		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - Contraloria.xlsx', engine='xlsxwriter')
		query.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Todas las cuentas', index=False)
		writer.save()

		print("===============")


