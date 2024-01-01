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
		#mes = 0
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
					ListaNegra.'COD PROYECTO' = "+str(row['COD PROYECTO'])+" \
				"
			listaNegra = pd.read_sql_query(queryListaNegra, cnx)
			if listaNegra.empty:
				cnx.execute("UPDATE PagosAprobados SET 'Esta en Lista Negra'=? WHERE unico=?", ("" , row['unico']))
				cnx.commit()
			else:
				cnx.execute("UPDATE PagosAprobados SET 'Esta en Lista Negra'=? WHERE unico=?", (listaNegra['OBSERVACIÓN'][0] , row['unico']))
				cnx.commit()
			# =======================================================================================================================================================
			if (row['SI Presenta Rend. De Cuenta ANTES'] == "X" or row['SI Presenta Rend. De Cuenta ANTES'] == "x") and (row['SI Presenta Rend. De Cuenta AHORA'] == "X" or row['SI Presenta Rend. De Cuenta AHORA'] == "x") and (row['Esta en Lista Negra'] == ""):			# TODO OK
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("PAGAR" , row['unico']))
				cnx.commit()

			elif (row['SI Presenta Rend. De Cuenta ANTES'] != "X" or row['SI Presenta Rend. De Cuenta ANTES'] != "x") and (row['SI Presenta Rend. De Cuenta AHORA'] == "X" or row['SI Presenta Rend. De Cuenta AHORA'] == "x") and (row['Esta en Lista Negra'] == ""):		# RETENER : NO PRESENTA RC EN ESE MES
				cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER : No presentó RC en ese mes" , row['unico']))
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
					cnx.execute("UPDATE PagosAprobados SET 'ANALISIS'=? WHERE unico=?", ("RETENER : No presenta RC en el mes "+str(mes)+" " , row['unico']))			# RETENER : NO PRESENTA RC EN ESE MES
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