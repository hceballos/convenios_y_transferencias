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
				r.'Catálogo 05',
				r.'Folio' as 'r.Folio',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido',
				c.'rut' as 'c.rut',
				c.'Folio' as 'c.Folio',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'rut' as 'd.rut',
				d.'Folio' as 'd.Folio',
				d.'mes' as 'd.mes',
				d.'Monto Vigente' as 'd.MontoVigente',
				d.'Monto Disponible' as 'd.MontoDisponible',
				d.'Monto Consumido' as 'd.MontoConsumido'
			FROM
				(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo 
					WHERE disponibilidadDevengo.'CodRegion' like '2111002%' 
					and disponibilidadDevengo.'cuenta' like '2401%'
					and disponibilidadDevengo.'Catálogo 05' = 'MetasAdicionales - 00 No Aplica'	)d
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso
					WHERE disponibilidadCompromiso.'cuenta' like '2401%'
					and disponibilidadCompromiso.'Monto Vigente' > 0
					and disponibilidadCompromiso.'Monto Disponible' > 0
					and disponibilidadCompromiso.'Monto Consumido' > 0)c
					ON d.'unico' = c.'unico'
					and c.'rut' = d.'rut'
					and c.'tipo_de_pago' = d.'tipo_de_pago'
					and c.'rut' = d.'rut'
				LEFT JOIN(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos
					WHERE disponibilidadRequerimientos.'cuenta' like '2401%')r
					ON r.'unico' = c.'unico'
			WHERE
				d.'CodRegion' like '2111002%'
				and d.'cuenta' like '2401%'
				and c.'Catálogo 05' = 'MetasAdicionales - 00 No Aplica'
				and r.'Catálogo 05' = 'MetasAdicionales - 00 No Aplica'
			ORDER BY
				d.'rut'
		"""
		df = pd.read_sql_query(consulta, cnx)


		df_item0 = pd.pivot_table(df,
							index = ["Unidad Ejecutora", "Concepto Presupuesto", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.rut", "c.Folio", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido"],
							aggfunc=[np.sum],
							fill_value=0,
							margins=True
							)
		# ----------------------------------------------------------------------------------------------

		df_item1 = pd.pivot_table(df,
							#index = ["Unidad Ejecutora", "Concepto Presupuesto", "r.Folio", "r.MontoVigente", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.Folio", "d.mes", "d.MontoVigente", "d.MontoDisponible", "d.MontoConsumido"],
							index = ["Unidad Ejecutora", "Concepto Presupuesto", "r.Folio", "r.MontoVigente", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.Folio", "d.mes", "d.MontoConsumido"],
							)


		meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))

		df_item2 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "r.Folio", "r.MontoVigente", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.Folio", "d.mes", "d.MontoConsumido"]
			)
		# ----------------------------------------------------------------------------------------------
		
		df_item3 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "r.Folio", "r.MontoVigente", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.Folio", "d.mes", "d.MontoConsumido"]
			)
		# ----------------------------------------------------------------------------------------------

		consulta = """
			SELECT
				r.'Unidad Ejecutora',
				r.'Concepto Presupuesto',
				d.'tipo_de_pago',
				r.'Folio' as 'r.Folio',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido',
				c.'rut' as 'c.rut',
				c.'Folio' as 'c.Folio',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'rut' as 'd.rut',
				d.'Folio' as 'd.Folio',
				d.'mes' as 'd.mes',
				d.'Monto Vigente' as 'd.MontoVigente',
				d.'Monto Disponible' as 'd.MontoDisponible',
				d.'Monto Consumido' as 'd.MontoConsumido'
			FROM
				(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo 
					WHERE disponibilidadDevengo.'CodRegion' like '2111002%' 
					and disponibilidadDevengo.'cuenta' like '2401%')d
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso
					WHERE disponibilidadCompromiso.'cuenta' like '2401%'
					and disponibilidadCompromiso.'Monto Vigente' > 0
					and disponibilidadCompromiso.'Monto Disponible' > 0
					and disponibilidadCompromiso.'Monto Consumido' > 0)c
					ON d.'unico' = c.'unico'
					and c.'rut' = d.'rut'
					and c.'tipo_de_pago' = d.'tipo_de_pago'
					and c.'rut' = d.'rut'
				LEFT JOIN(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos
					WHERE disponibilidadRequerimientos.'cuenta' like '2401%')r
					ON r.'unico' = c.'unico'
					and r.'tipo_de_pago' = d.'tipo_de_pago'
			WHERE
				d.'CodRegion' like '2111002%'
				and d.'cuenta' like '2401%'

			ORDER BY
				'r.Folio' desc
		"""
		df = pd.read_sql_query(consulta, cnx)
		meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))


		df_item4 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.Folio", "d.mes", "d.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		df_item4 = df_item4.sort_values(by=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago"], ascending=[True, True, False])
		# ----------------------------------------------------------------------------------------------


		consulta = """
			SELECT
				r.'Unidad Ejecutora',
				r.'Concepto Presupuesto',
				d.'tipo_de_pago',
				r.'Folio' as 'r.Folio',
				r.'Monto Vigente' as 'r.MontoVigente',
				r.'Monto Disponible' as 'r.MontoDisponible',
				r.'Monto Consumido' as 'r.MontoConsumido',
				c.'rut' as 'c.rut',
				c.'Folio' as 'c.Folio',
				c.'Monto Vigente' as 'c.MontoVigente',
				c.'Monto Disponible' as 'c.MontoDisponible',
				c.'Monto Consumido' as 'c.MontoConsumido',
				d.'rut' as 'd.rut',
				d.'Folio' as 'd.Folio',
				d.'mes' as 'd.mes',
				d.'Monto Vigente' as 'd.MontoVigente',
				d.'Monto Disponible' as 'd.MontoDisponible',
				d.'Monto Consumido' as 'd.MontoConsumido'
			FROM
				(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo 
					WHERE disponibilidadDevengo.'CodRegion' like '2111002%' 
					and disponibilidadDevengo.'cuenta' like '2401%')d
				LEFT JOIN(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso
					WHERE disponibilidadCompromiso.'cuenta' like '2401%'
					and disponibilidadCompromiso.'Monto Vigente' > 0
					and disponibilidadCompromiso.'Monto Disponible' > 0
					and disponibilidadCompromiso.'Monto Consumido' > 0)c
					ON d.'unico' = c.'unico'
					and c.'rut' = d.'rut'
					and c.'tipo_de_pago' = d.'tipo_de_pago'
					and c.'rut' = d.'rut'
				LEFT JOIN(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos
					WHERE disponibilidadRequerimientos.'cuenta' like '2401%')r
					ON r.'unico' = c.'unico'
					and r.'tipo_de_pago' = d.'tipo_de_pago'
			WHERE
				d.'CodRegion' like '2111002%'
				and d.'cuenta' like '2401%'

			ORDER BY
				'r.Folio' desc
		"""
		df = pd.read_sql_query(consulta, cnx)
		meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		df['d.mes'] = df['d.mes'].map(lambda x: meses_mapping.get(x, x))


		df_item5 = pd.pivot_table(df,
			index=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.Folio", "c.rut", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.Folio", "d.mes", "d.MontoConsumido"],
			margins = False,
			aggfunc='sum'
			)
		df_item5 = df_item5.sort_values(by=["Unidad Ejecutora", "Concepto Presupuesto", "tipo_de_pago"], ascending=[True, True, False])
		# ----------------------------------------------------------------------------------------------

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - TEST.xlsx', engine='xlsxwriter')
		df.to_excel(writer, sheet_name='df', index = False)
		df_item0.to_excel(writer, sheet_name='df_item0')		
		df_item1.to_excel(writer, sheet_name='df_item1')
		df_item2.to_excel(writer, sheet_name='df_item2')
		df_item3.to_excel(writer, sheet_name='df_item3')
		df_item4.to_excel(writer, sheet_name='df_item4')
		df_item5.to_excel(writer, sheet_name='df_item5')
		writer.save()



if __name__ == '__main__':
	main()