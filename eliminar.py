#! /bin/env python3
import os
import sys
import codecs
import time
import re
import sqlite3
import pandas as pd
import glob
import numpy as np
import pandas as pd
import sqlalchemy
from datetime import datetime
from time import sleep


class main(object):
	def __init__(self):
		self.read_Excel()

	def read_Excel(self):
		df = pd.DataFrame()
		for f in glob.glob("../mejorninez/input_excel/rocio.xls"):
			print('Procesando  : ', f)
			df = pd.read_excel(f, converters={ 'Fecha tipo cambio': str, 'Fecha tipo cambio.1': str, 'Fecha Cumplimiento': str, 'Fecha Tipo cambio cump': str, 'MES2': str, 'folio': str, 'Nº CDP': str, 'LINEA DE ACCION 2': str, 'Fecha Cumplimiento': str, 'Fecha Tipo cambio cump': str } )
			df = df.append(df,ignore_index=True)
		
		df['unico'] = df['MES2'] +"_"+ df['LINEA DE ACCION 2'] +"_"+ df['DR 2']

		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///contabilidad.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'df',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('Fecha tipo cambio', sqlalchemy.String),
			sqlalchemy.Column('Fecha tipo cambio.1', sqlalchemy.String),
			sqlalchemy.Column('Fecha Cumplimiento', sqlalchemy.String),
			sqlalchemy.Column('Fecha Tipo cambio cump', sqlalchemy.String),
			sqlalchemy.Column('Tipo Documento', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True)
			)
		metadata.create_all(engine)
		df.to_sql('df', engine, if_exists='replace')

		cnx = sqlite3.connect('contabilidad.db')
		consulta  = " \
			SELECT \
				DISTINCT(df.'unico') \
			FROM \
				df \
		"
		meses = pd.read_sql_query(consulta, cnx)
		print(meses)

		for index, row in meses.iterrows():
			consulta1  = " \
				SELECT \
					DISTINCT(df.'unico'), \
					df.* \
				FROM \
					df \
				WHERE \
					df.'unico' = "+"'"+row[0]+"'"+" \
			"
			query = pd.read_sql_query(consulta1, cnx)
			print(query['unico'])

			df2 = pd.DataFrame()
			df2 = df2.append(query,ignore_index=True)

			del df2['MES']
			del df2['MES2']
			del df2['AUXILIAR']
			del df2['LINEA DE ACCION']
			del df2['LINEA DE ACCION 2']
			del df2['DR']
			del df2['DR 2']
			del df2['unico']
			df2 = df2.drop(df2.columns[[0]],axis = 1)

			DfNew=df2[df2.duplicated()] 

			print(DfNew['Fecha tipo cambio'])


			print(" _______________________________________________________________________________________ ")
			DfNew.to_csv('salida/'+'aux_financiero_'+row['unico']+'.csv', sep=';', index=False, header=True, encoding='utf-8')

if __name__ == '__main__':
	main()