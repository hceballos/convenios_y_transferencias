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
import datetime


class PlazoDeLaDeuda(object):

	def normalizeDate(self, dateString):
		return dateString.replace(['(\d{2})\/(\d{2})\/(\d{4})'], ['\g<1>-\g<2>-\g<3>'], regex=True)

	def normalizeFactura(self, string):
		string	= [w.replace('.0', '' ) for w in string ]
		return string

	def normalizeRut(self, string):
		string	= [w.replace(',00', '' ) for w in string ]
		string	= [w.replace(' ', '' ) for w in string ]
		string	= [w.replace('$', '' ) for w in string ]
		string	= [w.replace('.', '' ) for w in string ]
		string	= [w.replace('(', '-' ) for w in string ]
		string	= [w.replace(')', '' ) for w in string ]
		return string

	def normalizeNumeric(self, string):
		return pd.to_numeric(string)

	def normalizeFolio(self, string):
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
		for f in glob.glob('input_excel/plazoDeLaDeuda/SB_CarteraFinancieraContable*.xls', recursive=True):
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
		contable_limpio['Intervalo'] = '"=SI(I2<=30;"1 Hasta 30 días ";SI(Y(I2>=31;I2<=45);"2 Entre 31 y 45 días";SI(Y(I2>=46;I2<=60);"3 Entre 46 y 60 días";SI(Y(I2>=61;I2<=90);"4 Entre 61 y 90 días";SI(Y(I2>=91;I2<=120);"5 Entre 91 y 120 días";SI(Y(I2>=120;I2<=150);"6 Entre 121 y 150 días"; SI((I2>=150);"7 Más de 150 días" )))))))"'
		#contable_limpio['Intervalo'] = '"=SI(I2<=30,"1 Hasta 30 días ",SI(Y(I2>=31,I2<=45),"2 Entre 31 y 45 días",SI(Y(I2>=46,I2<=60),"3 Entre 46 y 60 días",SI(Y(I2>=61,I2<=90),"4 Entre 61 y 90 días",SI(Y(I2>=91,I2<=120),"5 Entre 91 y 120 días",SI(Y(I2>=120,I2<=150),"6 Entre 121 y 150 días", SI((I2>=150),"7 Más de 150 días" )))))))"'

		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)

		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'contable_limpio',
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
		contable_limpio.to_sql('contable_limpio', engine, if_exists='replace', index=False)


		# =====================================================================================

		acepta = pd.DataFrame()
		# Cartera Financiera acepta: cuentas 21522, 21529, 21534
		for f in glob.glob('input_excel/plazoDeLaDeuda/reporte*.xls', recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f )
			acepta = acepta.append(df,ignore_index=True)

		acepta['emisor'] 	= self.normalizeRut(acepta['emisor'])
		acepta['tipo']		= acepta.drop( acepta[acepta['tipo'] == 52 ].index , inplace=True )
		acepta['unico']		= acepta['emisor'] + (acepta['folio'].apply(str))
		acepta['unico']		= self.normalizeFolio(acepta['unico'])
		acepta['emision'] = acepta['emision'].astype(str)



		del acepta['impuestos']
		#del acepta['uri']
		del acepta['estado_intercambio']
		del acepta['informacion_intercambio']
		del acepta['estado_nar']
		del acepta['uri_nar']
		del acepta['mensaje_nar']
		del acepta['uri_arm']
		del acepta['fecha_arm']
		del acepta['fmapago']
		del acepta['estado_acepta']
		del acepta['estado_sii']
		del acepta['referencias']
		del acepta['fecha_nar']
		del acepta['controller']
		del acepta['fecha_vencimiento']
		del acepta['estado_cesion']
		del acepta['url_correo_cesion']
		del acepta['fecha_recepcion_sii']
		del acepta['estado_reclamo']
		del acepta['fecha_reclamo']
		del acepta['mensaje_reclamo']
		del acepta['estado_devengo']
		del acepta['razon_social_emisor']
		del acepta['folio_rc']
		del acepta['fecha_ingreso_rc']
		del acepta['ticket_devengo']
		del acepta['folio_sigfe']
		del acepta['tarea_actual']
		del acepta['area_transaccional']
		del acepta['fecha_ingreso']	
		del acepta['fecha_aceptacion']
		del acepta['fecha']
		del acepta['tipo']
		del acepta['tipo_documento']
		del acepta['receptor']
		del acepta['publicacion']
		#del acepta['emision']
		del acepta['monto_neto']
		del acepta['monto_exento']
		del acepta['monto_iva']
		# del acepta['monto_total']
		del acepta['fecha_ingreso_oc']
		del acepta['codigo_devengo']


		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'acepta',
			metadata,
			sqlalchemy.Column('unico', sqlalchemy.String),


			)
		metadata.create_all(engine)
		acepta.to_sql('acepta', engine, if_exists='replace', index=False)



		cnx = sqlite3.connect('database.db')
		consulta  = " \
		SELECT \
			c.Rut, \
			c.NombreProveedor, \
			c.Factura, \
			c.Folio, \
			c.'Cuenta Contable', \
			c.current_year as Saldo, \
			a.uri as url, \
			a.emision as Fecha\
		FROM \
				(SELECT \
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
					'Cuenta Contable' asc) c \
				LEFT JOIN(SELECT acepta.* FROM acepta)a ON c.unico	= a.unico \
		"
		listo = pd.read_sql_query(consulta, cnx)
		#listo['Fecha 2'] = ""
		#print(listo['Fecha 2'])
		listo['Dias'] = ''
		listo['Intervalo'] = '"=SI(I2<=30;"1 Hasta 30 días ";SI(Y(I2>=31;I2<=45);"2 Entre 31 y 45 días";SI(Y(I2>=46;I2<=60);"3 Entre 46 y 60 días";SI(Y(I2>=61;I2<=90);"4 Entre 61 y 90 días";SI(Y(I2>=91;I2<=120);"5 Entre 91 y 120 días";SI(Y(I2>=120;I2<=150);"6 Entre 121 y 150 días"; SI((I2>=150);"7 Más de 150 días" )))))))"'
		#listo['Intervalo'] = '"=SI(I2<=30,"1 Hasta 30 días ",SI(Y(I2>=31,I2<=45),"2 Entre 31 y 45 días",SI(Y(I2>=46,I2<=60),"3 Entre 46 y 60 días",SI(Y(I2>=61,I2<=90),"4 Entre 61 y 90 días",SI(Y(I2>=91,I2<=120),"5 Entre 91 y 120 días",SI(Y(I2>=120,I2<=150),"6 Entre 121 y 150 días", SI((I2>=150),"7 Más de 150 días" )))))))"'


		# =====================================================================================
		cnx = sqlite3.connect('database.db')
		consulta  = " \
		SELECT \
			c.unico, \
			c.Rut, \
			c.NombreProveedor, \
			c.Factura, \
			c.Folio, \
			c.'Cuenta Contable', \
			c.Saldo, \
			a.emision as Fecha, \
			c.Dias, \
			c.Intervalo, \
			a.uri as url \
		FROM \
			(  \
			SELECT unico, Rut, NombreProveedor, Factura, Folio, contable_limpio.'Cuenta Contable', sum(current_year) as Saldo, Dias, Intervalo \
			FROM contable_limpio \
			GROUP BY unico \
			HAVING contable_limpio.'Cuenta Contable' LIKE '%' and [current_year]<>0 \
			ORDER BY 'Cuenta Contable' asc)c \
			LEFT JOIN(SELECT DISTINCT(acepta.unico), acepta.* FROM acepta GROUP BY unico)a ON c.unico = a.unico \
		"
		ultimo = pd.read_sql_query(consulta, cnx)

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - PlazoDeLaDeuda Mejor niñez.xlsx', engine='xlsxwriter')
		listo.to_excel(writer, sheet_name='Creado por Héctor Ceballos', index=False)
		contable.to_excel(writer, sheet_name='contable', index=False)
		contable_limpio.to_excel(writer, sheet_name='contable_limpio', index=False)
		ultimo.to_excel(writer, sheet_name='ultimo', index=False)

		writer.save()

