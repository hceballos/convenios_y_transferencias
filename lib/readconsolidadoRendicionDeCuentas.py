from lib.database  import Database
from lib.readJson  import ReadJson
from datetime import datetime
import sqlite3
import pandas as pd
import glob
import xlrd
import csv
import os
from lib.hayQueRetener import SisHayQueRetener
#from lib.sisLevantar import SisLevantar

from time import sleep
import time
from datetime import datetime

class ConsolidadoRendicionDeCuentas(ReadJson):

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		consolidadoRendicionDeCuentas = pd.DataFrame()
		for f in glob.glob(datos['consolidadoRendicionDeCuentas'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f, converters={ 'Periodo de Atención a Levantar o Retener': str,  'Fecha de Recepción': str } )
 			
			#df['Fecha de Recepción'] = df['Fecha de Recepción'].split(" ")

			#df['FechaRecepcion'] = df['Fecha de Recepción'].str.split(' ',expand=True)
			df['SiPresentaRendDeCuenta'] = df['SI Presenta Rend. De Cuenta']
			df['NoPresentaRendDeCuenta'] = df['NO Presenta Rend. De Cuenta']

			consolidadoRendicionDeCuentas = consolidadoRendicionDeCuentas.append(df,ignore_index=True)

		consolidadoRendicionDeCuentas['unico']	= consolidadoRendicionDeCuentas['Código '] + consolidadoRendicionDeCuentas['Periodo de Atención a Levantar o Retener']

		database = Database()
		database.databaseconsolidadoRendicionDeCuentas(consolidadoRendicionDeCuentas)


class HayQueRetener(ReadJson):

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		retener = pd.DataFrame()
		for f in glob.glob(datos['hayQueRetener'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f, converters={ 'MES ATENCION': str, 'COD PROYECTO': str } )
			df['MESATENCION'] 			= df['MES ATENCION']
			df['CODPROYECTO'] 			= df['COD PROYECTO']
			df['LevantarRetencion'] 	= 'Pendiente'
			df['MantenerRetencion'] 	= 'Pendiente'

			retener = retener.append(df,ignore_index=True)

		retener['unico']	= retener['COD PROYECTO'] + retener['MES ATENCION']

		database = Database()
		database.databaseRetenidos(retener)

		SisHayQueRetener(json_path, retener)


class HayQueLevantar(ReadJson):

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		levantar = pd.DataFrame()
		for f in glob.glob(datos['hayQueLevantar'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f, converters={ 'MES ATENCION': str, 'COD PROYECTO': str } )

			levantar = levantar.append(df,ignore_index=True)

		levantar['unico']	= levantar['COD PROYECTO'] + levantar['MES ATENCION']

		database = Database()
		database.databaseAprobados(levantar)
		SisLevantar(json_path, levantar)


class Fes(ReadJson):

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		fes = pd.DataFrame()
		for f in glob.glob(datos['fes'], recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f, converters={ 'mesano': str, 'codproyecto': str } )

			fes = fes.append(df,ignore_index=True)

		fes['unico']	= fes['codproyecto'] + fes['mesano']

		fes['SiPresentaRC']		= 'Pendiente'
		fes['NoPresentaRC']		= 'Pendiente'
		fes['PagosAprobados']	= 'Pendiente'
		fes['PagosRetenidos']	= 'Pendiente'
		fes['ListaNegra'] 		= 'Pendiente'


		database = Database()
		database.databaseFes(fes)

		writer = pd.ExcelWriter('FES.xlsx', engine='xlsxwriter')
		fes.to_excel(writer, sheet_name='Calculos previos a pago')
		writer.save()



class UnionTablas(object):

	def __init__(self):

		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				r.*, \
				c.* \
			FROM \
				(SELECT retenidos.* FROM retenidos) r \
				LEFT JOIN(SELECT \
							DISTINCT(consolidadoRendicionDeCuentas.'unico'), \
							consolidadoRendicionDeCuentas.'Fecha de Recepción', \
							consolidadoRendicionDeCuentas.'Código ', \
							consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener', \
							consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta' \
						FROM \
							consolidadoRendicionDeCuentas \
						WHERE \
							consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta' is not NULL \
							and consolidadoRendicionDeCuentas.'unico' is not NULL \
						ORDER BY \
							consolidadoRendicionDeCuentas.'Código ' DESC, \
							consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener' DESC \
				) c \
				ON c.'unico'	= r.'unico' \
				and c.'Código ' = r.'COD PROYECTO' \
				and c.'Periodo de Atención a Levantar o Retener' = r.'MES ATENCION' \
			WHERE \
				c.'unico'	= r.'unico' \
		"
		query = pd.read_sql_query(consulta, cnx)

		now = datetime.now()
		anio = str(now.year)
		mes = str(now.month-1)
		#print(anio+mes)
		periodo2 = anio+mes
		periodo = '202210'
		print(periodo, " ", periodo2)

		lista = []
		for index, row in query.iterrows():
			if row['Periodo de Atención a Levantar o Retener'] == periodo:
				#print("==== : ", row['Fecha de Recepción'], " 	",row['Código '], " 	" ,row['Periodo de Atención a Levantar o Retener'])
				lista.append(row['Código '])

		#print("lista :",lista)
		print("======================================================================================================")

		consulta  = " \
			SELECT \
				DISTINCT(consolidadoRendicionDeCuentas.'Fecha de Recepción') \
			FROM \
				consolidadoRendicionDeCuentas \
			ORDER BY \
				consolidadoRendicionDeCuentas.'Fecha de Recepción' DESC \
			LIMIT 1 \
		"
		fecha = pd.read_sql_query(consulta, cnx)
		laFecha =[]
		for index, row in fecha.iterrows():
			laFecha.append(row['Fecha de Recepción'])

		#print(" ", laFecha[0], "	",type(laFecha[0]))
		#x = laFecha[0].split(" ")
		#print("laFecha ", laFecha)
		#print("laFecha[0] : ", laFecha[0])

		fechaTest = '2022-11-09'
		print("Fecha de Recepción ", fechaTest)

		print("======================================================================================================")


		final = pd.DataFrame()

		for x in lista:
			#print(">>>>>>>>>>>>>>> : ", x, " 	" ,fechaTest)
			consulta  = " \
				SELECT \
					DISTINCT(consolidadoRendicionDeCuentas.'unico'), \
					consolidadoRendicionDeCuentas.'Fecha de Recepción', \
					consolidadoRendicionDeCuentas.'Código ', \
					consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener', \
					consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta' \
				FROM \
					consolidadoRendicionDeCuentas \
				WHERE \
					consolidadoRendicionDeCuentas.'Fecha de Recepción' = '2022-11-09' \
					and consolidadoRendicionDeCuentas.'Código ' = "+x+" \
					and consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta' is not NULL \
				"
			query = pd.read_sql_query(consulta, cnx)

			final = final.append(query,ignore_index=True)
		#print( final)


		# ================================================================================================================
		json_path = r'/Users/hector/Documents/desarrollo/mejorninez/data/data.json'
		SisRetener(json_path, final)
		# ================================================================================================================




		writer = pd.ExcelWriter('X.xlsx', engine='xlsxwriter')
		final.to_excel(writer, sheet_name='Calculos previos a pago')
		writer.save()


class Merge(object):

	def __init__(self):
		print("Merge")
		cnx = sqlite3.connect('database.db')

		# ================================================================================================================
		# ================================================================================================================
		print( "============================================ FES ============================================" )

		consulta  = " \
			SELECT \
				fes.* \
			FROM \
				fes \
		"
		fes = pd.read_sql_query(consulta, cnx)
		print("FES", fes)

		for index, row in fes.iterrows():
			print( row['unico'], "	", row['mesano'], "	", row['codproyecto'] )
			# ========================================================================
			consulta1  = " \
				SELECT \
					DISTINCT(consolidadoRendicionDeCuentas.'unico'), \
					consolidadoRendicionDeCuentas.'Fecha de Recepción', \
					consolidadoRendicionDeCuentas.'Código ', \
					consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener', \
					consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta', \
					consolidadoRendicionDeCuentas.'NoPresentaRendDeCuenta' \
					FROM \
					consolidadoRendicionDeCuentas \
				WHERE \
					consolidadoRendicionDeCuentas.'Código '	= "+row['codproyecto']+" \
					and consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener' = "+row['mesano']+" \
			"
			x = pd.read_sql_query(consulta1, cnx)
			if x.empty:
				pass
			else:
				cnx.execute("""UPDATE
									fes
								SET
									SiPresentaRC=?,
									NoPresentaRC=?
								WHERE
									codproyecto=?
									and mesano=?
								""", (x['SiPresentaRendDeCuenta'][0], x['NoPresentaRendDeCuenta'][0], row['codproyecto'], row['mesano']) )
				cnx.commit()
				print("Table updated...... ")

		# ================================================================================================================
		# ================================================================================================================
		print( "============================================ LEVANTAR RETENCION ============================================" )

		consulta  = " \
			SELECT \
				DISTINCT(consolidadoRendicionDeCuentas.'Fecha de Recepción') \
			FROM \
				consolidadoRendicionDeCuentas \
			ORDER BY \
				consolidadoRendicionDeCuentas.'Fecha de Recepción' DESC \
			LIMIT 1 \
		"
		fecha = pd.read_sql_query(consulta, cnx)
		laFecha =[]
		for index, row in fecha.iterrows():
			laFecha.append(row['Fecha de Recepción'])


		fecha = datetime.strptime(laFecha[0], '%Y-%m-%d %H:%M:%S.%f')
		fecha = fecha.strftime('%Y-%m-%d')

		print("fecha : ", fecha) 




		print("laFecha : ", laFecha[0])

		consulta  = " \
			SELECT \
				retenidos.* \
			FROM \
				retenidos \
		"
		retenidos = pd.read_sql_query(consulta, cnx)


		for index, row in retenidos.iterrows():
			print( row['unico'], "	", row['MESATENCION'], "	", row['CODPROYECTO'] )



			# ========================================================================






		consulta  = " \
			SELECT \
				fes.* \
			FROM \
				fes \
		"
		update = pd.read_sql_query(consulta, cnx)

		writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')
		update.to_excel(writer, sheet_name='Calculos previos a pago')
		writer.save()
