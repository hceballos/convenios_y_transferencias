from lib.database  import Database
from lib.readJson  import ReadJson
from datetime import datetime
from datetime import datetime, timedelta
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

		cnx = sqlite3.connect('database.db')
		consulta = """
			SELECT 
				r.'Unidad Ejecutora',
				r.'Concepto Presupuesto',
				r.'tipo_de_pago',
				r.'Folio' as 'r.Folio',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido',
				c.'Folio' as 'c.Folio',
				c.'rut' as 'c.rut',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido'		
			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos WHERE disponibilidadRequerimientos.'cuenta' like '2401%')r

				LEFT JOIN(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos WHERE disponibilidadRequerimientos.'cuenta' like '2401%' )n
					ON r.'unico' = n.'unico'
					and r.'CodRegion' = n.'CodRegion'
					and r.'cuenta' = n.'cuenta'
					and r.'tipo_de_pago' = n.'tipo_de_pago'
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso WHERE disponibilidadCompromiso.'cuenta' like '2401%' )c
					ON r.'unico' = c.'unico'
					and r.'CodRegion' = c.'CodRegion'
					and r.'cuenta' = c.'cuenta'
					and r.'tipo_de_pago' = c.'tipo_de_pago'	
				WHERE
				c.'CodRegion' like '2111002%'
				and c.'cuenta' like '2401%'
		"""
		df = pd.read_sql_query(consulta, cnx)
		#meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		#df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))


		df_item0 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		df_item0 = df_item0.sort_values(by=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago"], ascending=[True, True, False])
		# ----------------------------------------------------------------------------------------------
		consulta = """
			SELECT 
				r.'Unidad Ejecutora',
				r.'cuenta',
				r.'tipo_de_pago',
				r.'Folio' as 'r.Folio',
				(SELECT SUM(r2.'Monto Vigente')  FROM disponibilidadRequerimientos r2  WHERE r2.'cuenta' = r.'cuenta' AND r2.'CodRegion' = '2111001') as 'DisponibleNacional',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido'
			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos WHERE disponibilidadRequerimientos.'cuenta' LIKE '2401%') r
		"""
		df = pd.read_sql_query(consulta, cnx)
		#meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		#df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))


		okRequerimiento = pd.pivot_table(df,
			index=["Unidad Ejecutora", "DisponibleNacional", "cuenta", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		okRequerimiento = okRequerimiento.sort_values(by=["Unidad Ejecutora", "cuenta", "tipo_de_pago"], ascending=[True, True, False])
		# ----------------------------------------------------------------------------------------------
		consulta = """
			SELECT 
				r.'Unidad Ejecutora',
				r.'cuenta',
				r.'tipo_de_pago',
				r.'Folio' as 'r.Folio',
				(SELECT SUM(r2.'Monto Vigente')  FROM disponibilidadRequerimientos r2  WHERE r2.'cuenta' = r.'cuenta' AND r2.'CodRegion' = '2111001') as 'DisponibleNacional',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido',
				c.'rut' as 'c.rut',
				c.'Folio' as 'c.Folio',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido'

			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos)r
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso)c
					ON r.'unico' = c.'unico'
					and r.'tipo_de_pago' = c.'tipo_de_pago'
					
			WHERE
				r.'CodRegion' like '2111002%'
				and r.'cuenta' like '2401%'


		"""
		df = pd.read_sql_query(consulta, cnx)
		#meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		#df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))


		okCompromiso = pd.pivot_table(df,
			index=["Unidad Ejecutora", "DisponibleNacional", "cuenta", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.rut", "c.Folio", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		okCompromiso = okCompromiso.sort_values(by=["Unidad Ejecutora", "cuenta", "tipo_de_pago"], ascending=[True, True, False])
		# ----------------------------------------------------------------------------------------------
		consulta = """
			SELECT 
				r.'Unidad Ejecutora',
				r.'cuenta',
				r.'tipo_de_pago',
				r.'Folio' as 'r.Folio',
				(SELECT SUM(r2.'Monto Vigente')  FROM disponibilidadRequerimientos r2  WHERE r2.'cuenta' = r.'cuenta' AND r2.'CodRegion' = '2111001') as 'DisponibleNacional',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido',
				c.'rut' as 'c.rut',
				c.'Folio' as 'c.Folio',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'mes' as 'd.mes',
				d.'Folio' as 'd.Folio',
				d.'rut' as 'd.rut',
				d.'Monto Vigente' as 'd.MontoVigente'

			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos)r
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso)c
					ON r.'unico' = c.'unico'
					and r.'tipo_de_pago' = c.'tipo_de_pago'
				LEFT JOIN(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo WHERE disponibilidadDevengo.'cuenta' like '2401%')d 
					ON r.'unico' = d.'unico'
					and r.'tipo_de_pago' = d.'tipo_de_pago'
					and r.'CodRegion' = d.'CodRegion'
					and r.'cuenta' = d.'cuenta'
				WHERE
				c.'CodRegion' like '2111002%'
				and c.'cuenta' like '2401003%'
				and d.'CodRegion' = c.'CodRegion'
				and d.'cuenta' = c.'cuenta'
				and d.'rut' = c.'rut'
				and d.'tipo_de_pago' = c.'tipo_de_pago'	


		"""
		df = pd.read_sql_query(consulta, cnx)
		#meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		#df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))


		Devengo = pd.pivot_table(df,
			index=["Unidad Ejecutora", "DisponibleNacional", "cuenta", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.rut", "c.Folio", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.rut", "d.Folio", "d.mes" ,"d.MontoVigente"],
			margins = False,
			aggfunc='sum'
			)
		Devengo = Devengo.sort_values(by=["Unidad Ejecutora", "cuenta", "tipo_de_pago"], ascending=[True, True, False])


		# ----------------------------------------------------------------------------------------------
		consulta = """
			SELECT 
				r.'Unidad Ejecutora',
				r.'cuenta',
				r.'tipo_de_pago',
				r.'Folio' as 'r.Folio',
				(SELECT SUM(r2.'Monto Vigente') FROM disponibilidadRequerimientos r2 WHERE r2.'cuenta' = r.'cuenta' AND r2.'CodRegion' = '2111001') as 'DisponibleNacional',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido',
				c.'rut' as 'c.rut',
				c.'Folio' as 'c.Folio',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'mes' as 'd.mes',
				d.'Folio' as 'd.Folio',
				d.'rut' as 'd.rut',
				d.'Monto Vigente' as 'd.MontoVigente',
				(SELECT SUM(d2.'Monto Vigente') FROM disponibilidadDevengo d2 WHERE d2.'rut' = d.'rut' AND d2.'tipo_de_pago' = d.'tipo_de_pago') as 'grupo'
			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos) r
				LEFT JOIN (SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso WHERE disponibilidadCompromiso.'cuenta' LIKE '2401%') c
					ON r.'unico' = c.'unico'
					AND r.'tipo_de_pago' = c.'tipo_de_pago'
					AND r.'CodRegion' = c.'CodRegion'
					AND r.'cuenta' = c.'cuenta'
				LEFT JOIN (SELECT disponibilidadDevengo.* FROM disponibilidadDevengo WHERE disponibilidadDevengo.'cuenta' LIKE '2401%') d
					ON r.'unico' = d.'unico'
					AND r.'tipo_de_pago' = d.'tipo_de_pago'
					AND r.'CodRegion' = d.'CodRegion'
					AND r.'cuenta' = d.'cuenta'
			WHERE
				c.'CodRegion' like '2111002%'
				AND c.'cuenta' LIKE '2401003%'
				AND d.'CodRegion' = c.'CodRegion'
				AND d.'cuenta' = c.'cuenta'
				AND d.'rut' = c.'rut'
				AND d.'tipo_de_pago' = c.'tipo_de_pago'
		"""
		df1 = pd.read_sql_query(consulta, cnx)
		#meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		#df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))


		okDevengo = pd.pivot_table(df1,
			index=["Unidad Ejecutora", "DisponibleNacional", "cuenta", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.rut", "c.Folio", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.rut", "d.Folio", "d.mes" ,"d.MontoVigente"],
			margins = False,
			aggfunc='sum'
			)
		okDevengo = okDevengo.sort_values(by=["Unidad Ejecutora", "cuenta", "tipo_de_pago"], ascending=[True, True, False])
		# ----------------------------------------------------------------------------------------------



		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - TEST-3.xlsx', engine='xlsxwriter')
		df.to_excel(writer, sheet_name='df', index = False)
		df_item0.to_excel(writer, sheet_name='df_item0')
		df.to_excel(writer, sheet_name='df')
		okRequerimiento.to_excel(writer, sheet_name='okRequerimiento')
		okCompromiso.to_excel(writer, sheet_name='okCompromiso')
		Devengo.to_excel(writer, sheet_name='Devengo')
		okDevengo.to_excel(writer, sheet_name='okDevengo')
		writer.save()

if __name__ == '__main__':
	main()