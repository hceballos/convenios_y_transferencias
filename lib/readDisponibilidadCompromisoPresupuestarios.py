from lib.database  import Database
from lib.readJson  import ReadJson
import sqlite3
import pandas as pd
import glob
import xlrd
import csv
import os
from datetime import date


class ReadDisponibilidadCompromisoPresupuestarios(ReadJson):

	def normalizeDateConta(self, dateString):
		return dateString.replace(['(\d{2}).(\d{2}).(\d{2})?(\d{2})'], ['\g<4>-\g<2>-\g<1>'], regex=True)

	def normalizeDate(self, dateString):
		return dateString.replace(['(\d{2})\/(\d{2})\/(\d{4})'], ['\g<3>-\g<2>-\g<1>'], regex=True)

	def normalizeNumeric(self, string):
		string	= [w.replace(',00', '' ) for w in string ]
		string	= [w.replace(' ', '' ) for w in string ]
		string	= [w.replace('$', '' ) for w in string ]
		string	= [w.replace('.', '' ) for w in string ]
		string	= [w.replace('(', '-' ) for w in string ]
		string	= [w.replace(')', '' ) for w in string ]
		return pd.to_numeric(string)

	def normalizeFloat64ToString(self, numero):
		print(type(numero))
		numeroInString = numero.astype(str)
		print(type(numeroInString))
		return numero

	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos


		region_mapping = { '2111001': 0, '2111002': 1, '2111003': 2, '2111004': 3, '2111005': 4, '2111006': 5, '2111007': 6, '2111008': 7, '2111009': 8, '2111010': 9, '2111011': 10, '2111012': 11, '2111013': 12, '2111014': 13, '2111015': 15, '2111016': 14, '2111017': 16}
		tipo_de_pago_mapping = { 'MetasAdicionales - 00 No Aplica' : 'SUBV', 'MetasAdicionales - 01 META 80 BIS' : '80 BIS', 'MetasAdicionales - 02 EMERGENCIA' : 'EMG'}

		disponibilidadCompromiso = pd.DataFrame()
		for f in glob.glob(self.datos['DisponibilidadDeCompromiso'], recursive=True):
			print('Procesando  : ', f)

			df = pd.read_excel(f, skiprows=5, header=0)  
			df['rut']		= df['Número Identificación']
			df['CodRegion']	= df['Unidad Ejecutora'].str.split(' ', n = 1, expand = True)[0]
			df['cuenta']	= df['Concepto Presupuesto'].str.split(' ', n = 1, expand = True)[0]
			df['unico']		= df['CodRegion'] + df['cuenta']

			disponibilidadCompromiso = disponibilidadCompromiso.append(df,ignore_index=True)

		disponibilidadCompromiso['region'] 			= disponibilidadCompromiso['CodRegion'].map(region_mapping)
		disponibilidadCompromiso['tipo_de_pago'] 	= disponibilidadCompromiso['Catálogo 05'].map(tipo_de_pago_mapping)
		disponibilidadCompromiso['llave'] 			= disponibilidadCompromiso.apply(lambda row: f"{row['region']}-{row['cuenta']}-{row['tipo_de_pago']}-{row['Número Identificación']}",axis=1)

		database = Database()
		database.databaseDisponibilidadCompromiso(disponibilidadCompromiso)


		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				disponibilidadCompromiso.* \
			FROM \
				disponibilidadCompromiso \
			WHERE \
				disponibilidadCompromiso.'Concepto Presupuesto' like '2401%' \
		"
		query = pd.read_sql_query(consulta, cnx)

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - DisponibilidadCompromisosPresupuestarios.xlsx', engine='xlsxwriter')
		query.to_excel(writer, sheet_name='2401 - Todas las coberturas', index = False)
		writer.save()

		#self.centralizaciones()

	def centralizaciones(self):

		centralizaciones = pd.DataFrame()
		for f in glob.glob("../mejorninez/input_excel/Sigfe/centralizaciones*", recursive=True):
			print('Procesando  : ', f)

			df = pd.read_excel(f, converters={'ENERO': int, 'FEBRERO': int, 'MARZO': int, 'ABRIL': int, 'MAYO': int, 'JUNIO': int, 'JULIO': int, 'AGOSTO': int, 'SEPTIEMBRE': int, 'OCTUBRE': int, 'NOVIEMBRE': int, 'DICIEMBRE': int, 'TOTAL': int, 'región': str, 'cuenta': str, 'folio compromiso': str, 'COD PROYECTO': str, 'TIPO PAGO': str } )
			centralizaciones = centralizaciones.append(df,ignore_index=True)

		centralizaciones['FolioDevengo'] = 'Pendiente'


		database = Database()
		database.databasecentralizaciones(centralizaciones)

		# Genera reporte
		cnx = sqlite3.connect('database.db')

		consulta1  = " \
			SELECT \
				c.*, \
				d.'Monto Consumido', \
				d.'Monto Consumido' - c.'TOTAL' AS Diferencia, \
				d.'Folio', \
				d.'Monto Vigente' \
			FROM \
				(SELECT centralizaciones.* FROM centralizaciones)c \
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso)d ON c.llave	= d.llave \
			WHERE \
				Diferencia > 0 \
		"
		query = pd.read_sql_query(consulta1, cnx)



		consulta1  = " \
			SELECT \
				c.*, \
				d.'Monto Consumido', \
				d.'Monto Consumido' - c.'TOTAL' AS Diferencia, \
				d.'Folio', \
				d.'Monto Vigente' \
			FROM \
				(SELECT centralizaciones.* FROM centralizaciones)c \
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso)d ON c.llave	= d.llave \
			WHERE \
				Diferencia < 0 \
		"
		query1 = pd.read_sql_query(consulta1, cnx)



		consulta2  = " \
			SELECT \
				disponibilidadDevengo.* \
			FROM \
				disponibilidadDevengo \
			WHERE \
				disponibilidadDevengo.cuenta like '24%' \
		"
		devengo = pd.read_sql_query(consulta2, cnx)


		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - Revision de contabilizaciones subt.24.xlsx', engine='xlsxwriter')
		query1.to_excel(writer, sheet_name='2401 - Diferencias < 0', index = False)
		query.to_excel(writer, sheet_name='2401 - Diferencias > 0', index = False)
		devengo.to_excel(writer, sheet_name='2401 Devengos', index = False)
		writer.save()