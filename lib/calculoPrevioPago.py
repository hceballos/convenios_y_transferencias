from lib.database  import Database
from lib.readJson  import ReadJson
from lib.readRetenciones  import ReadRetenciones
import sqlalchemy
import pandas as pd
import numpy as np
import glob
import sqlite3
import xlrd
import csv
import os
import re
import sys

class Reporte_FES(ReadJson):

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		acepta = pd.DataFrame()
		for f in glob.glob(datos['reporte_FES'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f, skiprows=3, header=0)  
			#print(df.columns)

			df['modalidad']			= df['ModeloIntervencion'].str.split(' - ', n = 1, expand = True)[0]
			df['nombre_modalidad']	= df['ModeloIntervencion'].str.split(' - ', n = 1, expand = True)[1]
			df['year'] 				= pd.DatetimeIndex(df['Fechaactualizacion']).year
			df['mes']				= pd.DatetimeIndex(df['Fechaactualizacion']).month

			writer = pd.ExcelWriter('reporte_FES.xlsx', engine='xlsxwriter')
			df.to_excel(writer, sheet_name='Todas las cuentas')
			writer.save()

			database = Database()
			database.databaseReporte_FES(df)


class Malla(ReadJson):

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		acepta = pd.DataFrame()
		for f in glob.glob(datos['malla'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f)  
			#print(df.columns)


			writer = pd.ExcelWriter('malla.xlsx', engine='xlsxwriter')
			df.to_excel(writer, sheet_name='Todas las cuentas')
			writer.save()


			database = Database()
			database.databaseMalla(df)

		ReadRetenciones(datos)

class Calculos(object):

	def factorVariable(self, query):
		factorVariable = query['Factor Variable'] *  ( 1 + 
														(query['Factor Edad']/100) + 
														(query['Factor Complejidad']/100) + 
														(query['factor discapacidad']/100) + 
														(query['PorcentajeZona']/100)
													 ) * query['Factor USS'] * query['NroPlazas']
		return factorVariable


	def factorFijo(self, query):
		factorFijo = query['FactorFijo']
		return factorFijo

	def __init__(self):

		cnx = sqlite3.connect('calculoPrevioPago.db')
		consulta  = " \
			SELECT \
				f.*, \
				m.NroPlazas, \
				m.FactorFijo, \
				m.'Factor Variable', \
				m.'Interveciones exigidas', \
				m.'Factor Edad', \
				m.'Factor Complejidad', \
				m.'factor discapacidad', \
				m.'FactorCobertura', \
				m.'FactorCVF/Factor Edad RVA - RVT', \
				m.'Factor USS', \
				m.'PorcentajeZona' \
			FROM \
				(SELECT reporte_FES.* FROM reporte_FES)f \
				LEFT JOIN(SELECT malla.* FROM malla)m ON f.codproyecto = m.codproyecto \
		"
		query = pd.read_sql_query(consulta, cnx)
		query['calculo Hector'] = 'Pendiente de calculo'

		query.loc[query['modalidad'] == "PPF", "calculo Hector"] = self.factorFijo(query) + self.factorVariable(query)
		query.loc[query['modalidad'] == "OPD", "calculo Hector"] = self.factorFijo(query) + self.factorVariable(query)

		query.loc[query['modalidad'] == "PER", "calculo Hector"] = self.factorFijo(query) + self.factorVariable(query)
		query.loc[query['modalidad'] == "PIE", "calculo Hector"] = self.factorFijo(query) + self.factorVariable(query)
		query.loc[query['modalidad'] == "DAM", "calculo Hector"] = self.factorFijo(query) + self.factorVariable(query)

		

		"""
		SELECT 
			*
		FROM 
			retenciones 
		WHERE 
			(retenciones.'Fecha de Recepción') IN (SELECT Max(retenciones.'Fecha de Recepción') FROM retenciones GROUP BY retenciones.'Periodo de Atención a Levantar o Retener' ORDER BY	retenciones.'Periodo de Atención a Levantar o Retener' DESC)
			and  retenciones.'Código ' = '1100480'
		ORDER BY	
			retenciones.'Fecha de Recepción' DESC,
			retenciones.'Periodo de Atención a Levantar o Retener' DESC
		"""



		# PPF
		# OPD
		# PRM
		# PER
		# PIE
		# REM
		# DAM
		# FAE
		# PRO
		# RLP
		# PDE
		# PRE
		# PDC
		# RVA
		# PPE
		# PEE
		# PRI
		# RPM
		# PAD
		# PAS
		# RDS
		# PRD
		# PEC
		# RMA
		# RPA
		# RPE
		# RPP
		# RSP
		# RVT

		writer = pd.ExcelWriter('informe_calculoPrevioPago.xlsx', engine='xlsxwriter')
		query.to_excel(writer, sheet_name='Calculos previos a pago')
		writer.save()

		