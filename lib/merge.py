from lib.database  import Database
from lib.readJson  import ReadJson
from datetime import datetime
import sqlite3
import pandas as pd
import glob
import xlrd
import csv
import os
from lib.sisRetener import SisRetener
from time import sleep
import time
from datetime import datetime


class Merge_Fes_ConsolidadoRC(object):

	def __init__(self):
		print("Merge_Fes_Retenidos")
		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				fes.* \
			FROM \
				fes \
		"
		fes = pd.read_sql_query(consulta, cnx)

		for index, row in fes.iterrows():
			print( row['unico'], "	", row['mesano'], "	", row['codproyecto'] )
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

		consulta  = " \
			SELECT \
				fes.* \
			FROM \
				fes \
		"
		update = pd.read_sql_query(consulta, cnx)

		writer = pd.ExcelWriter('Merge_Fes_Retenidos.xlsx', engine='xlsxwriter')
		update.to_excel(writer, sheet_name='Calculos previos a pago')
		writer.save()
		# ================================================================================================================
		# ================================================================================================================

class Merge_Retenidos_ConsolidadoRC(object):

	def __init__(self):
		print("Merge_Retenidos_ConsolidadoRC")
		cnx = sqlite3.connect('database.db')

		# ============================================ FECHA INICIO ====================================================================
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
		fechaRecepcion = str(fecha.strftime('%Y-%m-%d')+"%")
		print("fechaRecepcion 	: ", fechaRecepcion) 
		# ============================================ FECHA FIN ====================================================================

		# ============================================ PERIODO A RENDIR - INICIO ====================================================================
		now = datetime.now()
		anio = str(now.year)
		mes = str(now.month-1)
		periodo = anio+mes
		print("periodo 			: ", periodo) 
		# ============================================ PERIODO A RENDIR - FIN    ====================================================================


		# ============================================ LISTADO DE PROYECTOS QUE SI PRESENTARON HOY - INICIO    ====================================================================
		listado  = " \
			SELECT \
				DISTINCT(consolidadoRendicionDeCuentas.'unico'), \
				consolidadoRendicionDeCuentas.'Fecha de Recepción', \
				consolidadoRendicionDeCuentas.'Código ', \
				consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener', \
				consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta', \
				consolidadoRendicionDeCuentas.'NoPresentaRendDeCuenta', \
				consolidadoRendicionDeCuentas.'unico' \
			FROM \
				consolidadoRendicionDeCuentas \
			WHERE \
				consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta' is not NULL \
				and consolidadoRendicionDeCuentas.'Fecha de Recepción' LIKE '"+fechaRecepcion+"' \
				and consolidadoRendicionDeCuentas.'unico' is not NULL \
				and consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener' = "+periodo+" \
			ORDER BY \
				consolidadoRendicionDeCuentas.'Código ' asc, \
				consolidadoRendicionDeCuentas.'Periodo de Atención a Levantar o Retener' desc \
		"
		siPresentaronAhora = pd.read_sql_query(listado, cnx) 
		siPresentaronAhora['id'] = siPresentaronAhora['Código ']+siPresentaronAhora['Periodo de Atención a Levantar o Retener']

		lista = []
		for index, row in siPresentaronAhora.iterrows():
			lista.append(row)
		print(" ========== LISTA ========== ")
		#print(lista)
		print(" ========== LISTA ========== ")
		# ============================================ LISTADO DE PROYECTOS QUE SI PRESENTARON HOY - FIN    ====================================================================


		# ============================================ LISTADO DE PROYECTOS QUE SI PRESENTARON HOY Y ANTES - INICIO    ====================================================================
		siPresentaronAhorayAntes = pd.DataFrame()
		for x in lista:
			print(">>>>>>>>>>>>>>> : ", x['Código '], x['Periodo de Atención a Levantar o Retener'])
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
					consolidadoRendicionDeCuentas.'Fecha de Recepción' LIKE '"+fechaRecepcion+"' \
					and consolidadoRendicionDeCuentas.'Código ' = "+x['Código ']+" \
					and consolidadoRendicionDeCuentas.'SiPresentaRendDeCuenta' is not NULL \
				"
			#query = pd.read_sql_query(consulta, cnx)

			x = pd.read_sql_query(consulta1, cnx)
			if x.empty:
				pass
			else:
				print(x['SiPresentaRendDeCuenta'][0], x['NoPresentaRendDeCuenta'][0])
				cnx.execute("""UPDATE
									retenidos
								SET
									LevantarRetencion=?,
									MantenerRetencion=?
								WHERE
									CODPROYECTO=?
									and MESATENCION=?
								""", ("Lenvantar", "MantenerRetencion", row['Código '], row['Periodo de Atención a Levantar o Retener']) )
				cnx.commit()
				print("Table updated...... ")

			siPresentaronAhorayAntes = siPresentaronAhorayAntes.append(x,ignore_index=True)
		print("siPresentaronAhorayAntes : ",siPresentaronAhorayAntes)
		database = Database()
		database.databasePresentaronAhorayAntes(siPresentaronAhorayAntes)

		# ============================================ LISTADO DE PROYECTOS QUE SI PRESENTARON HOY Y ANTES - FIN    ====================================================================
		consulta1  = " \
			SELECT \
				r.*, \
				p.* \
			FROM \
				(SELECT retenidos.* FROM retenidos)r \
				LEFT JOIN(SELECT presentaronAhorayAntes.* FROM presentaronAhorayAntes)p \
				ON r.unico	= p.unico \
			"
		join = pd.read_sql_query(consulta1, cnx)


		consulta1  = " \
			SELECT \
				 presentaronAhorayAntes.* \
			FROM \
				presentaronAhorayAntes \
			"
		presentaronAhorayAntes = pd.read_sql_query(consulta1, cnx)


		writer = pd.ExcelWriter('Merge_Retenidos_ConsolidadoRC.xlsx', engine='xlsxwriter')
		siPresentaronAhorayAntes.to_excel(writer, sheet_name='siPresentaronAhorayAntes')
		join.to_excel(writer, sheet_name='join')
		presentaronAhorayAntes.to_excel(writer, sheet_name='presentaronAhorayAntes')
		writer.save()


