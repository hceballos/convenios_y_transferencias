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
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'Folio' as 'd.Folio',
				d.'rut' as 'd.rut',
				d.'Monto Vigente' as 'd.MontoVigente',
				d.'Monto Disponible' as 'd.MontoDisponible',
				d.'Monto Consumido' as 'd.MontoConsumido'		
			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos WHERE disponibilidadRequerimientos.'cuenta' like '2401%')r
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso WHERE disponibilidadCompromiso.'cuenta' like '2401%')c
					ON r.'unico' = c.'unico'
					and r.'CodRegion' = c.'CodRegion'
					and r.'cuenta' = c.'cuenta'
					and r.'tipo_de_pago' = c.'tipo_de_pago'	
				LEFT JOIN(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo WHERE disponibilidadDevengo.'cuenta' like '2401%')d 
					ON r.'unico' = d.'unico'
					and r.'tipo_de_pago' = d.'tipo_de_pago'
					and r.'CodRegion' = d.'CodRegion'
					and r.'cuenta' = d.'cuenta'
				WHERE
				r.'CodRegion' = c.'CodRegion'
				and c.'CodRegion' = d.'CodRegion'
				and r.'cuenta' = c.'cuenta'
				and c.'cuenta' = d.'cuenta'
				and c.'rut' = d.'rut'
				and r.'CodRegion' like '2111002%'
				and r.'cuenta' like '2401004%'
		"""
		df = pd.read_sql_query(consulta, cnx)
		df_item1 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido" , "d.MontoVigente", "d.MontoDisponible", "d.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		df_item1 = df_item1.sort_values(by=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago"], ascending=[True, True, False])

		# ----------------------------------------------------------------------------------------------
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
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'Folio' as 'd.Folio',
				d.'rut' as 'd.rut',
				d.'Monto Vigente' as 'd.MontoVigente',
				d.'Monto Disponible' as 'd.MontoDisponible',
				d.'Monto Consumido' as 'd.MontoConsumido'		
			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos WHERE disponibilidadRequerimientos.'cuenta' like '2401%')r
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso WHERE disponibilidadCompromiso.'cuenta' like '2401%')c
					ON r.'unico' = c.'unico'
					and r.'CodRegion' = c.'CodRegion'
					and r.'cuenta' = c.'cuenta'
					and r.'tipo_de_pago' = c.'tipo_de_pago'	
				LEFT JOIN(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo WHERE disponibilidadDevengo.'cuenta' like '2401%')d 
					ON r.'unico' = d.'unico'
					and r.'tipo_de_pago' = d.'tipo_de_pago'
					and r.'CodRegion' = d.'CodRegion'
					and r.'cuenta' = d.'cuenta'
				WHERE
				r.'CodRegion' = c.'CodRegion'
				and c.'CodRegion' = d.'CodRegion'
				and r.'cuenta' = c.'cuenta'
				and c.'cuenta' = d.'cuenta'
				and c.'rut' = d.'rut'
				and r.'CodRegion' like '2111002%'
				and r.'cuenta' like '2401004%'
		"""
		df = pd.read_sql_query(consulta, cnx)
		df_item2 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.Folio", "d.rut", "d.MontoVigente", "d.MontoDisponible", "d.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		df_item2 = df_item2.sort_values(by=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago"], ascending=[True, True, False])


		# ----------------------------------------------------------------------------------------------
		consulta = """
			SELECT 
				c.'Unidad Ejecutora',
				c.'Concepto Presupuesto',
				c.'tipo_de_pago',
				c.'Folio' as 'c.Folio',
				c.'rut' as 'c.rut',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'Folio' as 'd.Folio',
				d.'rut' as 'd.rut',
				d.'Monto Vigente' as 'd.MontoVigente',
				d.'Monto Disponible' as 'd.MontoDisponible',
				d.'Monto Consumido' as 'd.MontoConsumido'		
			FROM
				(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso WHERE disponibilidadCompromiso.'cuenta' like '2401%')c
				LEFT JOIN(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo WHERE disponibilidadDevengo.'cuenta' like '2401%')d
					ON d.'unico' = c.'unico'
					and d.'CodRegion' = c.'CodRegion'
					and d.'cuenta' = c.'cuenta'
					and d.'rut' = c.'rut'
					and d.'tipo_de_pago' = c.'tipo_de_pago'	

			WHERE
				c.'CodRegion' like '2111002%'
				and c.'cuenta' like '2401%'
				and d.'CodRegion' = c.'CodRegion'
				and d.'cuenta' = c.'cuenta'
				and d.'rut' = c.'rut'
				and d.'tipo_de_pago' = c.'tipo_de_pago'	

		"""
		df = pd.read_sql_query(consulta, cnx)
		df_item3 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido" , "d.Folio", "d.rut", "d.MontoVigente", "d.MontoDisponible", "d.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		df_item3 = df_item3.sort_values(by=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago"], ascending=[True, True, False])


		# ----------------------------------------------------------------------------------------------
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
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'mes' as 'd.mes',
				d.'Folio' as 'd.Folio',
				d.'rut' as 'd.rut',
				d.'Monto Vigente' as 'd.MontoVigente',
				d.'Monto Disponible' as 'd.MontoDisponible',
				d.'Monto Consumido' as 'd.MontoConsumido'		
			FROM
				(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos WHERE disponibilidadRequerimientos.'cuenta' like '2401%')r

				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso WHERE disponibilidadCompromiso.'cuenta' like '2401%' )c
					ON r.'unico' = c.'unico'
					and r.'CodRegion' = c.'CodRegion'
					and r.'cuenta' = c.'cuenta'
					and r.'tipo_de_pago' = c.'tipo_de_pago'	
				LEFT JOIN(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo WHERE disponibilidadDevengo.'cuenta' like '2401%')d 
					ON r.'unico' = d.'unico'
					and r.'tipo_de_pago' = d.'tipo_de_pago'
					and r.'CodRegion' = d.'CodRegion'
					and r.'cuenta' = d.'cuenta'
				WHERE
				c.'CodRegion' like '2111002%'
				and c.'cuenta' like '2401%'
				and d.'CodRegion' = c.'CodRegion'
				and d.'cuenta' = c.'cuenta'
				and d.'rut' = c.'rut'
				and d.'tipo_de_pago' = c.'tipo_de_pago'	
		"""
		df0 = pd.read_sql_query(consulta, cnx)

		meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		df0['d.mes'] = df0['d.mes'].map(lambda x: meses_mapping.get(x, x))

		df_item4 = pd.pivot_table(df0,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		df_item4 = df_item4.sort_values(by=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago"], ascending=[True, True, False])



		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - TEST-2.xlsx', engine='xlsxwriter')
		df.to_excel(writer, sheet_name='df', index = False)
		df_item0.to_excel(writer, sheet_name='df_item0')
		df_item1.to_excel(writer, sheet_name='df_item1')
		df_item2.to_excel(writer, sheet_name='df_item2')
		df_item3.to_excel(writer, sheet_name='df_item3')
		df0.to_excel(writer, sheet_name='df0')
		df_item4.to_excel(writer, sheet_name='df_item4')
		writer.save()



if __name__ == '__main__':
	main()