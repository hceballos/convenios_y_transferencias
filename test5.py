from lib.database  import Database
from lib.readJson  import ReadJson
from datetime import datetime
from datetime import datetime, timedelta
import sqlalchemy
import pandas as pd
import sqlite3
import numpy as np
import glob
import xlrd
import csv
import os
from datetime import date
import json

class main(object):
	def __init__(self):


		pago = pd.DataFrame()
		for f in glob.glob("../mejorninez/input_excel/Sigfe/ResumenDePagosMesual/*", recursive=True):
			print('Procesando  : ', f)
			df = pd.read_excel(f, converters={'MES ATENCION': str, 'TIPO PAGO': str, 'COD REGION': str,'COD PROYECTO': str, 'PROYECTO': str, 'RUT PROYECTO': str, 'MONTO LIQUIDO PAGADO': int, })  

			#print(df.columns)
			#df['rut']		= df['Principal'].str.split(' ', n = 1, expand = True)[0]
			#df['Concepto']	= df['Concepto Presupuestario'].str.split(' ', n = 1, expand = True)[0]
			#df['CodRegion']	= df['Código Unidad Ejecutora'].str.split(' ', n = 1, expand = True)[0]
			#df['cuenta']	= df['Concepto Presupuestario'].str.split(' ', n = 1, expand = True)[0]
			#df['year'] 		= pd.DatetimeIndex(df['Fecha Documento']).year
			#df['mes']		= pd.DatetimeIndex(df['Fecha Documento']).month
			#df['unico']		= df['CodRegion'] + df['cuenta']

			pago = pago.append(df,ignore_index=True)

		# Eliminar columnas no deseadas
		columns_to_delete = ['ID TIPO PAGO', 'MONTO RETENCION','FOLIO', 'MODELO INTERVENCION', 'COD INSTITUCION', 'INSTITUCION', 'DEPARTAMENTO SENAME', 'TIPO SUBVENCION_DES', 'TIPO PROYECTO_DES', 'BANCO', 'CUENTA CORRIENTE NUMERO', 'MONTO MAXIMO PAGO', 'MONTO PAGO FIJO', 'MONTO PAGO VARIABLE', 'MONTO POR ATENCION', 'MONTO DEUDA', 'MONTO RELIQUIDACION', 'PLAZAS CONVENIDAS', 'PLAZAS ATENDIDAS', 'FACTOR FIJO', 'FACTOR VARIABLE', 'FACTOR EDAD', 'FACTOR COBERTURA', 'FACTOR DISCAPACIDAD', 'FACTOR COMPLEJIDAD', 'FACTOR CVF', 'ASIGNACION ZONA', 'FACTOR USS', 'USS', 'NUMERO PLAZAS', 'NRO DIAS', 'FECHA CIERRE PAGO ', 'NUMERO RESOLUCION', 'FECHA CREACION', 'FECHA TERMINO', 'NUMERO CDP', 'ANNO PRESUPUESTARIO', 'NUMERO RESOLUCION CDP', 'FECHA RESOLUCION CDP', 'DESCRIPCION CDP']
		pago.drop(columns=columns_to_delete, inplace=True)

		pago['PROYECTO']	= pago['PROYECTO'].str.slice(0, 3)
		pago['TIPO PAGO'] 	= pago['TIPO PAGO'].replace(['URGENCIA', 'ANTICIPO', 'MASIVO NORMAL'], 'SUBV').replace('OTROS PAGOS', 'EMG')

		cambios_de_nombre = {
			'CLA': '2401004',
			'CPE': '2401004', 'DAM': '2401001', 'DCE': '2401001', 'FAE': '2401004', 'FAS': '2401004', 'FPA': '2401002', 'OPD': '2401006',
			'PAD': '2401002','PAS': '2401002','PDC': '2401002','PDE': '2401002','PEC': '2401002','PEE': '2401002','PER': '2401003', 
			'PIB': '2401002', 'PIE': '2401002', 'PPC': '2401002', 'PPE': '2401003', 'PPF': '2401002', 'PRD': '2401003', 'PRE': '2401003', 'PRI': '2401005',
			'PRM': '2401002','PRO': '2401003','RAD': '2401004','RDD': '2401004','RDG': '2401004','RDS': '2401004','REM': '2401004','REN': '2401004', 
			'RLP': '2401004', 'RMA': '2401004', 'RPA': '2401004', 'RPE': '2401004', 'RPF': '2401004', 'RPL': '2401004', 'RPM': '2401004', 'RPP': '2401004', 'RSP': '2401004', 'RVA': '2401004', 'RVT': '2401004'
		}
		pago['cuenta'] = pago['PROYECTO'].replace(cambios_de_nombre)


		cambios_de_nombre_region = {
			'1': '2111002', '2': '2111003', '3': '2111004', '4': '2111005', '5': '2111006',
			'6': '2111007', '7': '2111008', '8': '2111009', '9': '21110010', '10': '2111011', '11': '2111012',
			'12': '2111013', '13': '2111014', '14': '2111015', '15': '2111016', '16': '2111017', '17': '2111001'			
		}
		pago['CodRegion'] = pago['COD REGION'].replace(cambios_de_nombre_region)


		pago.rename(columns={
			'MES ATENCION':'mes_atencion',
			'TIPO PAGO':'tipo_de_pago',
			'COD REGION':'CodRegion',
			'COD PROYECTO':'proyecto',
			'PROYECTO':'tipo_de_proyecto',
			'RUT PROYECTO':'rut',
			'MONTO LIQUIDO PAGADO':'monto'
		}, inplace=True)

		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'pago',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('tipo_de_pago', sqlalchemy.String),
			sqlalchemy.Column('CodRegion', sqlalchemy.String),
			sqlalchemy.Column('proyecto', sqlalchemy.String),
			sqlalchemy.Column('tipo_de_proyecto', sqlalchemy.String),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('RUT PROYECTO', sqlalchemy.String),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.Integer)
			)

		metadata.create_all(engine)
		pago.to_sql('pago', engine, if_exists='replace', index=False)


		cnx = sqlite3.connect('database.db')
		consulta = " \
			SELECT \
				DISTINCT(disponibilidadRequerimientos.'CodRegion'), \
				disponibilidadRequerimientos.'Unidad Ejecutora' \
			FROM \
				disponibilidadRequerimientos \
			WHERE \
				disponibilidadRequerimientos.'CodRegion' <> '2111001' \
		"
		df = pd.read_sql_query(consulta, cnx)
		for index, row in df.iterrows():
			print(row['CodRegion'], row['Unidad Ejecutora'])
			self.databaseArbol(row)

	def databaseArbol(self, row):
		# ----------------------------------------------------------------------------------------------
		cnx = sqlite3.connect('database.db')		

		consulta = " \
			SELECT \
				pago.* \
			FROM \
				pago \
			WHERE \
			   pago.'CodRegion' = '"+row['CodRegion']+"' \
			   AND pago.'cuenta' LIKE '2401003%' \
		"
		reportePago = pd.read_sql_query(consulta, cnx)
		# ----------------------------------------------------------------------------------------------

		# ----------------------------------------------------------------------------------------------
		cnx = sqlite3.connect('database.db')		

		consulta = " \
			SELECT \
			   r.'Unidad Ejecutora', \
			   r.'cuenta', \
			   r.'tipo_de_pago', \
			   r.'Folio' as 'r.Folio', \
			   r.'Monto Vigente' as 'r.MontoVigente', \
			   r.'Monto Disponible' as 'r.MontoDisponible', \
			   r.'Monto Consumido' as 'r.MontoConsumido', \
			   c.'rut' as 'c.rut', \
			   c.'Folio' as 'c.Folio', \
			   c.'Monto Vigente' as 'c.MontoVigente', \
			   c.'Monto Disponible' as 'c.MontoDisponible', \
			   c.'Monto Consumido' as 'c.MontoConsumido', \
			   p.'monto' \
			FROM \
			   (SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso)c \
			   LEFT JOIN (SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos)r \
					ON c.'unico' = r.'unico' \
					AND c.'CodRegion' = r.'CodRegion' \
					AND c.'cuenta' = r.'cuenta' \
					AND c.'tipo_de_pago' = r.'tipo_de_pago' \
			   LEFT JOIN (SELECT pago.* FROM pago)p \
					ON c.'CodRegion' = p.'CodRegion' \
					AND c.'cuenta' = p.'cuenta' \
					AND c.'rut' = p.'rut' \
					AND c.'tipo_de_pago' = p.'tipo_de_pago' \
			WHERE \
			   c.'CodRegion' = '"+row['CodRegion']+"' \
			   AND c.'cuenta' LIKE '2401003%' \
		"
		df2 = pd.read_sql_query(consulta, cnx)
		# ----------------------------------------------------------------------------------------------
		consulta = " \
			SELECT \
			   r.'unico', \
			   r.'Unidad Ejecutora', \
			   r.'cuenta', \
			   r.'tipo_de_pago', \
			   r.'Folio' as 'r.Folio', \
			   r.'Monto Vigente' as 'r.MontoVigente', \
			   r.'Monto Disponible' as 'r.MontoDisponible', \
			   r.'Monto Consumido' as 'r.MontoConsumido', \
			   c.'rut' as 'c.rut', \
			   c.'Folio' as 'c.Folio', \
			   c.'Monto Vigente' as 'c.MontoVigente', \
			   c.'Monto Disponible' as 'c.MontoDisponible', \
			   c.'Monto Consumido' as 'c.MontoConsumido', \
			   p.'monto' \
			FROM \
			   (SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso)c \
			   LEFT JOIN (SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos)r \
					ON c.'unico' = r.'unico' \
					AND c.'CodRegion' = r.'CodRegion' \
					AND c.'cuenta' = r.'cuenta' \
					AND c.'tipo_de_pago' = r.'tipo_de_pago' \
			   LEFT JOIN (SELECT pago.* FROM pago)p \
					ON c.'CodRegion' = p.'CodRegion' \
					AND c.'cuenta' = p.'cuenta' \
					AND c.'rut' = p.'rut' \
					AND c.'tipo_de_pago' = p.'tipo_de_pago' \
			WHERE \
			   c.'CodRegion' = '"+row['CodRegion']+"' \
			   AND c.'cuenta' LIKE '2401003%' \
			   AND (c.'rut' IS NULL OR r.'Monto Vigente' IS NULL OR r.'Monto Vigente' <> c.'Monto Vigente') \
		"
		df3 = pd.read_sql_query(consulta, cnx)



		# Crea DataFrames separados para las tablas 'c' y 'p' con las filas no coincidentes
		c_not_matched = df3[df3['c.Folio'].isna()].copy()
		c_not_matched['MontoVigente'] = 0
		c_not_matched['MontoDisponible'] = 0
		c_not_matched['MontoConsumido'] = 0

		p_not_matched = df3[df3['monto'].isna()].copy()
		p_not_matched['c.rut'] = 0
		p_not_matched['c.Folio'] = 0
		p_not_matched['c.MontoVigente'] = 0
		p_not_matched['c.MontoDisponible'] = 0
		p_not_matched['c.MontoConsumido'] = 0

		# Combina los DataFrames que representan las no coincidencias
		combined_df = pd.concat([df3, c_not_matched, p_not_matched])

		# Realiza la tabla pivote en el DataFrame combinado
		df_3 = pd.pivot_table(combined_df,
		       index=["Unidad Ejecutora", "cuenta", "tipo_de_pago", "r.Folio", "c.rut"],
		       values=["monto"],
		       aggfunc=[np.sum],
		       fill_value=0,
		       margins=True
		       )
		# ----------------------------------------------------------------------------------------------


		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - '+str(row['Unidad Ejecutora'])+'.xlsx', engine='xlsxwriter')
		reportePago.to_excel(writer, sheet_name="reportePago")
		df2.to_excel(writer, sheet_name="QWERT")
		df_3.to_excel(writer, sheet_name="df_3")
		writer.save()

if __name__ == '__main__':
	main()