from lib.database  import Database
import sqlalchemy
import pandas as pd
import glob
import sqlite3
from datetime import datetime
from datetime import date
import xlrd
import csv
import os
import numpy as np

class PlazoDeLaDeuda(object):

	def normalizeDate(self, dateString):
		return dateString.replace(['(\d{2})\/(\d{2})\/(\d{4})'], ['\g<1>-\g<2>-\g<3>'], regex=True)

	def normalizeFactura(self, string):
		string	= [w.replace('.0', '' ) for w in string ]
		return string



	def __init__(self):
		"""
		for f in glob.glob('..\\Users\\hector\\Documents\\PlazoDeLaDeuda\\input\\SB_CarteraFinancieraContabl*', recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f , skiprows=10, header=0)
			contable = contable.append(df,ignore_index=True)
		"""

		contable = pd.DataFrame()
		# Cartera Financiera Contable: cuentas 21522, 21529, 21534
		for f in glob.glob('input_excel/plazoDeLaDeuda/*.xls', recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f , skiprows=10, header=0)
			contable = contable.append(df,ignore_index=True)

		contable.rename(columns={'Número ':'Factura'}, inplace=True)

		contable['Título']	= contable.drop( contable[ contable['Título'] == 'Total Flujos Periodo' ].index , inplace=True )
		contable['Rut']		= contable['Principal'].str.split(' ', n = 1, expand = True)[0]
		contable['NombreProveedor'] = contable['Principal'].str.split(' ', n = 1, expand = True)[1]
		contable['Saldo'] 	= contable['Haber'] - contable['Debe']
		contable['Saldo'] 	= pd.to_numeric(contable['Saldo'])
		contable['Saldo'] 	= contable['Saldo'].astype(np.int32)
		contable['Factura'] = contable.Factura.apply(str)

		contable = contable.astype({"Factura": 'str'})
		contable['Factura'] = self.normalizeFactura(contable['Factura'])
		contable['unico'] 	=  contable['Rut'] + contable['Factura']

		del contable['Tipo Movimiento']
		del contable['Fecha']
		#del contable['Folio']
		del contable['Título']
		del contable['Saldo Acumulado']
		del contable['Tipo Documento']
		del contable['Haber']
		del contable['Debe']

		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)

		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'contable',
			metadata,
			sqlalchemy.Column('Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Contable', sqlalchemy.String),
			sqlalchemy.Column('Principal', sqlalchemy.String),
			sqlalchemy.Column('Saldo', sqlalchemy.Integer),
			sqlalchemy.Column('Fecha', sqlalchemy.String),
			sqlalchemy.Column('Factura', sqlalchemy.String),
			sqlalchemy.Column('Rut', sqlalchemy.String)

			)


		metadata.create_all(engine)
		contable.to_sql('contable', engine, if_exists='replace', index=False)


		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				contable.'unico', \
				Rut, \
				NombreProveedor, \
				Factura, \
				Folio, \
				contable.'Cuenta Contable', \
				sum(Saldo) as current_year \
			FROM \
				contable \
			GROUP BY \
				unico \
			HAVING \
				contable.'Cuenta Contable' LIKE '%' \
				and [current_year]<>0 \
			ORDER BY \
				'Cuenta Contable' asc \
		"
		contable_limpio = pd.read_sql_query(consulta, cnx)
		contable_limpio['Fecha'] = ''
		contable_limpio['Dias'] = ''
		#contable_limpio['Intervalo'] = '"=SI(I2<=30;"1 Hasta 30 días ";SI(Y(I2>=31;I2<=45);"2 Entre 31 y 45 días";SI(Y(I2>=46;I2<=60);"3 Entre 46 y 60 días";SI(Y(I2>=61;I2<=90);"4 Entre 61 y 90 días";SI(Y(I2>=91;I2<=120);"5 Entre 91 y 120 días";SI(Y(I2>=120;I2<=150);"6 Entre 121 y 150 días"; SI((I2>=150);"7 Más de 150 días" )))))))"'
		contable_limpio['Intervalo'] = '"=SI(I2<=30,"1 Hasta 30 días ",SI(Y(I2>=31,I2<=45),"2 Entre 31 y 45 días",SI(Y(I2>=46,I2<=60),"3 Entre 46 y 60 días",SI(Y(I2>=61,I2<=90),"4 Entre 61 y 90 días",SI(Y(I2>=91,I2<=120),"5 Entre 91 y 120 días",SI(Y(I2>=120,I2<=150),"6 Entre 121 y 150 días", SI((I2>=150),"7 Más de 150 días" )))))))"'



		# =====================================================================================
		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				disponibilidadDevengo.'Código Unidad Ejecutora', \
				disponibilidadDevengo.'Folio', \
				disponibilidadDevengo.'Principal', \
				disponibilidadDevengo.'Número Documento', \
				disponibilidadDevengo.'Fecha Documento', \
				disponibilidadDevengo.'Concepto Presupuestario', \
				disponibilidadDevengo.'Monto Consumido', \
				disponibilidadDevengo.'rut', \
				disponibilidadDevengo.'year', \
				disponibilidadDevengo.'mes' \
			FROM \
				disponibilidadDevengo \
		"
		disponibilidad = pd.read_sql_query(consulta, cnx)

		writer = pd.ExcelWriter('PlazoDeLaDeuda Mejor niñez.xlsx', engine='xlsxwriter')
		contable.to_excel(writer, sheet_name='contable', index=False)
		contable_limpio.to_excel(writer, sheet_name='contable_limpio', index=False)
		disponibilidad.to_excel(writer, sheet_name='disponibilidad', index=False)
		writer.save()





