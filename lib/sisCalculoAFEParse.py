#! /bin/env python3
from datetime import date
from lib.fuente import Fuente
import os
import pandas as pd
import sys
import time
import glob
import xlrd
import shutil
import csv
import sqlalchemy
import sqlite3
import datetime


class Parse(object):


	def databaseUpate(self, cnx, info , unico):
		cnx.execute("UPDATE PagosAprobados SET 'Esta en Lista Negra'=? WHERE unico=?", (info , unico))
		cnx.commit()

	def __init__(self):

		ano = datetime.datetime.today().year
		mes = datetime.datetime.today().month-1
		#mes = 3
		print("ParseAprobados mes : ", mes)
		
		if mes == 0:
			mes = 12
			ano = ano-1
		periodo = str(ano)+str(mes)
		print("periodo  : ", periodo, mes, len(str(mes)) )
		if len(str(mes)) == 1:
			mes = '0'+str(mes)
		print("periodo  : ", periodo, mes, len(str(mes)) )
		periodo = str(ano)+str(mes)
		print("periodo  : ", periodo, mes, len(str(mes)) )

		cnx = sqlite3.connect('AFE.db')
		query  = " \
			SELECT \
				PagosAprobados.* \
			FROM \
				PagosAprobados \
			"
		PagosAprobados = pd.read_sql_query(query, cnx)

		for index, row in PagosAprobados.iterrows():
			queryRendiciones  = " \
				SELECT \
					Rendiciones.* \
				FROM \
					Rendiciones \
				WHERE \
					Rendiciones.'unico' = "+row['unico']+" \
				ORDER BY \
					Rendiciones.'Fecha de Recepción' DESC \
				LIMIT 1 \
				"
			Rendiciones = pd.read_sql_query(queryRendiciones, cnx)
			if Rendiciones.empty:
				cnx.execute("UPDATE PagosAprobados SET 'SI Presenta Rend. De Cuenta ANTES'=? WHERE unico=?", ("Retener!" , row['unico']))
				cnx.commit()
			else:
				cnx.execute("UPDATE PagosAprobados SET 'SI Presenta Rend. De Cuenta ANTES'=? WHERE unico=?", (Rendiciones['SI Presenta Rend. De Cuenta'][0] , row['unico']))
				cnx.commit()
			# =======================================================================================================================================================
			queryRendicionesAHORA  = " \
				SELECT \
					Rendiciones.'unico', \
					Rendiciones.'SI Presenta Rend. De Cuenta' \
				FROM \
					Rendiciones \
				WHERE \
					Rendiciones.'unico' = "+str(row['COD PROYECTO'])+str(periodo)+" \
				ORDER BY \
					Rendiciones.'Fecha de Recepción' DESC \
				LIMIT 1 \
				"
			RendicionesAHORA = pd.read_sql_query(queryRendicionesAHORA, cnx)
			if RendicionesAHORA.empty:
				cnx.execute("UPDATE PagosAprobados SET 'SI Presenta Rend. De Cuenta AHORA'=? WHERE unico=?", ("Retener!" , row['unico']))
				cnx.commit()
			else:
				cnx.execute("UPDATE PagosAprobados SET 'SI Presenta Rend. De Cuenta AHORA'=? WHERE unico=?", (RendicionesAHORA['SI Presenta Rend. De Cuenta'][0] , row['unico']))
				cnx.commit()
			# =======================================================================================================================================================
			queryListaNegra  = " \
				SELECT \
					ListaNegra.'LISTA NEGRA', \
					ListaNegra.'OBSERVACIÓN' \
				FROM \
					ListaNegra \
				WHERE  \
					ListaNegra.'unico' = "+str(row['unico'])+" \
				"
			listaNegra = pd.read_sql_query(queryListaNegra, cnx)
			if listaNegra.empty:
				cnx.execute("UPDATE PagosAprobados SET 'Esta en Lista Negra'=? WHERE unico=?", ("" , row['unico']))
				cnx.commit()
			else:
				cnx.execute("UPDATE PagosAprobados SET 'Esta en Lista Negra'=? WHERE unico=?", (listaNegra['OBSERVACIÓN'][0] , row['unico']))
				cnx.commit()
			# ================================================================ i=======================================================================================
			#print(row['unico'], " 	", row['TIPO PAGO'])
			queryBis  = " \
				SELECT \
					Bis.* \
				FROM \
					Bis \
				WHERE  \
					Bis.'LLAVE UNICA' = "+str(row['unico'])+" \
				"
			Bis = pd.read_sql_query(queryBis, cnx)

			diff80bis = (Bis['Monto Total']-int(row['MONTO LIQUIDO PAGADO']))*1

			if Bis.empty:
				cnx.execute("UPDATE PagosAprobados SET '80Bis'=? WHERE unico=?", ("" , row['unico'] ))
				cnx.commit()
			else:
				cnx.execute("UPDATE PagosAprobados SET '80Bis'=? WHERE unico=?", (int(diff80bis[0]) , row['unico']))
				cnx.commit()
			# ===================================================================f ====================================================================================
			queryRU  = " \
				SELECT \
					Urgencias.* \
				FROM \
					Urgencias \
				WHERE  \
					Urgencias.'unico' = "+str(row['unico'])+" \
				"
			RU = pd.read_sql_query(queryRU, cnx)

			diffRU = (RU['Monto Líquido A Pago']-int(row['MONTO LIQUIDO PAGADO']))*1

			if RU.empty:
				cnx.execute("UPDATE PagosAprobados SET 'Urgencias'=? WHERE unico=?", ("" , row['unico']))
				cnx.commit()
			else:
				cnx.execute("UPDATE PagosAprobados SET 'Urgencias'=? WHERE unico=?", (int(diffRU[0]) , row['unico']))
				cnx.commit()
			# ===================================================================f ====================================================================================

			if (row['SI Presenta Rend. De Cuenta ANTES'] == "X" or row['SI Presenta Rend. De Cuenta ANTES'] == "x") and (row['SI Presenta Rend. De Cuenta AHORA'] == "X" or row['SI Presenta Rend. De Cuenta AHORA'] == "x") and (row['Esta en Lista Negra'] == ""):			# TODO OK
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("PAGAR" , row['unico']))
				cnx.commit()

			elif (row['SI Presenta Rend. De Cuenta ANTES'] != "X" or row['SI Presenta Rend. De Cuenta ANTES'] != "x") and (row['SI Presenta Rend. De Cuenta AHORA'] == "X" or row['SI Presenta Rend. De Cuenta AHORA'] == "x") and (row['Esta en Lista Negra'] == ""):		# RETENER : NO PRESENTA RC EN ESE MES
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER : No presentó RC en ese mes, ver mes de inicio" , row['unico']))
				cnx.commit()

			elif (row['SI Presenta Rend. De Cuenta ANTES'] == "X" or row['SI Presenta Rend. De Cuenta ANTES'] == "x") and (row['SI Presenta Rend. De Cuenta AHORA'] != "x" or row['SI Presenta Rend. De Cuenta AHORA'] != "X") and (row['Esta en Lista Negra'] == ""):		# RETENER : NO PRESENTA RC EN ESE MES
				#print(row['PROYECTO'])
				evaluaMes = str(ano)+"-"+str(mes)
				if evaluaMes in row['FECHA CREACION']:
					cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("PAGAR : Es primes mes de funcionamiento, PAGAR" , row['unico']))				# PAGAR : PRIMER MES DE FUNCIONAMIENTO
					cnx.commit()
				elif row['TIPO PAGO'] == "ANTICIPO":
					cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("PAGAR : Pagar Anticipo" , row['unico']))										# PAGAR : PAGAR ANTICIPO
					cnx.commit()
				elif "EMG" in row['PROYECTO']:
					#print("row['PROYECTO'] : ", row['PROYECTO'])
					cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("PAGAR : Pagar Emergencia" , row['unico']))									# PAGAR : PAGAR EMERGENCIA
					cnx.commit()
				else:
					cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER : No presenta RC en el mes "+str(mes)+" , ver mes de inicio" , row['unico']))			# RETENER : NO PRESENTA RC EN ESE MES
					cnx.commit()

			elif (row['SI Presenta Rend. De Cuenta ANTES'] == "x" or row['SI Presenta Rend. De Cuenta ANTES'] == "X") and (row['SI Presenta Rend. De Cuenta AHORA'] == "x" or row['SI Presenta Rend. De Cuenta AHORA'] == "X") and (row['Esta en Lista Negra'] != ""):		# RETENER : NO PRESENTA RC ESTE MES
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER : Está en lista negra" , row['unico']))
				cnx.commit()

			else:
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER" , row['unico']))
				cnx.commit()
			# =======================================================================================================================================================

			if "EMG" in row['PROYECTO']:
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("PAGAR EMERGENCIA" , row['unico']))												# PAGAR : PRIMER MES DE FUNCIONAMIENTO
				cnx.commit()


			evaluaMes = str(ano)+"-"+str(mes)
			if (evaluaMes in row['FECHA CREACION']) and ("RETENER" in row['ANALISIS']):
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("PAGAR : PRIMER MES DE FUNCIONAMIENTO" , row['unico']))							# PAGAR : PRIMER MES DE FUNCIONAMIENTO
				cnx.commit()

			if len(str(row['CUENTA CORRIENTE NUMERO'])) > 1 :
				pass 
			else:
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER : Sin número de cuenta corriente" , row['unico']))						# RETENER : SIN NUMERO DE CUENTA
				cnx.commit()



			if (int(row['MONTO LIQUIDO PAGADO']) <= 0):
				#print(">>>>>>>>>> : ", int(row['MONTO LIQUIDO PAGADO']), type(int(row['MONTO LIQUIDO PAGADO'])) )
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER : Monto igual o menor a 0" , row['unico']))								# RETENER : MONTO IGUAL O MENOR A 0
				cnx.commit()

		query  = " \
			SELECT \
				PagosAprobados.* \
			FROM \
				PagosAprobados \
			"
		PagosAprobados = pd.read_sql_query(query, cnx)

		writer = pd.ExcelWriter('PagosAprobados.xlsx', engine='xlsxwriter')
		PagosAprobados.to_excel(writer, sheet_name='Pagos Aprobados')
		writer.save()

		# ==================================================================================================
		writer = pd.ExcelWriter('AFE Aprobados.xlsx', engine='xlsxwriter')
		PagosAprobados.to_excel(writer, sheet_name='Pagos Aprobados', index=False)

		# Obtener el objeto workbook y la hoja de trabajo
		workbook = writer.book
		worksheet = writer.sheets['Pagos Aprobados']

		# Agregar formato a cada columna
		rojo  = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
		verde = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
		azul  = workbook.add_format({'bg_color': '#BDD7EE', 'font_color': '#1F497D'})

		worksheet.set_column('BC:BC', None, rojo)

		worksheet.set_column('D:D', None, verde)
		worksheet.set_column('I:I', None, verde)
		worksheet.set_column('AX:AX', None, verde)
		worksheet.set_column('Z:Z', None, verde)
		worksheet.set_column('F:F', None, azul)
		worksheet.set_column('J:J', None, azul)
		worksheet.set_column('R:R', None, azul)
		worksheet.set_column('AQ:AQ', None, azul)
		worksheet.set_column('AY:AY', None, azul)
		worksheet.set_column('AZ:AZ', None, azul)
		worksheet.set_column('BA:BA', None, azul)
		worksheet.set_column('BB:BB', None, azul)

		# Fijar la fila superior
		worksheet.freeze_panes(1, 0)  # Fijar la fila superior

		# Aplicar un filtro a la columna deseada
		worksheet.autofilter('A1:BD1')  # Filtrar la columna 'columna1'

		# Guardar y cerrar el archivo de Excel
		writer.save()
		# ==================================================================================================