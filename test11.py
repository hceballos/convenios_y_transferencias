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
 
 

		# ----------------------------------------------------------------------------------------------
		cnx = sqlite3.connect('database.db')		
		consulta = " \
			SELECT \
				r.'Unidad Ejecutora', \
				r.'cuenta', \
				r.'tipo_de_pago', \
				r.'Folio' as 'r.Folio', \
				(SELECT SUM(r2.'Folio') FROM disponibilidadRequerimientos r2 WHERE r2.'cuenta' = r.'cuenta' AND r2.'CodRegion' = '2111001') as 'FolioNacional', \
				(SELECT SUM(r2.'Monto Vigente') FROM disponibilidadRequerimientos r2 WHERE r2.'cuenta' = r.'cuenta' AND r2.'CodRegion' = '2111001') as 'DisponibleNacional', \
				r.'Monto Vigente' as 'r.MontoVigente', \
				r.'Monto Disponible' as 'r.MontoDisponible', \
				r.'Monto Consumido' as 'r.MontoConsumido', \
				c.'rut' as 'c.rut', \
				c.'Folio' as 'c.Folio', \
				c.'Monto Vigente' as 'c.MontoVigente', \
				c.'Monto Disponible' as 'c.MontoDisponible', \
				c.'Monto Consumido' as 'c.MontoConsumido', \
				d.'mes' as 'd.mes', \
				d.'Folio' as 'd.Folio', \
				d.'Monto Vigente' as 'd.MontoVigente', \
				d.'Monto Disponible' as 'd.MontoDisponible', \
				d.'Monto Consumido' as 'd.MontoConsumido' \
			FROM \
				(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso) c \
				LEFT JOIN(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos) r \
					ON c.'unico' = r.'unico' \
					AND c.'CodRegion' = r.'CodRegion' \
					AND c.'cuenta' = r.'cuenta' \
					AND c.'tipo_de_pago' = r.'tipo_de_pago' \
				LEFT JOIN(SELECT disponibilidadDevengo.* FROM disponibilidadDevengo) d \
					ON c.'unico' = d.'unico' \
					AND c.'CodRegion' = d.'CodRegion' \
					AND c.'cuenta' = d.'cuenta' \
					AND c.'tipo_de_pago' = d.'tipo_de_pago' \
					AND c.'rut' = d.'rut' \
				LEFT JOIN(SELECT pago.* FROM pago) p \
					ON d.'CodRegion' = p.'region' \
					AND d.'cuenta' = p.'cuenta' \
					AND d.'rut' = p.'rut' \
					AND d.'tipo_de_pago' = p.'tipo_de_pago' \
			WHERE \
				c.'CodRegion' LIKE '21110%' \
				AND c.'cuenta' LIKE '240100%' \
				AND c.'CodRegion' = r.'CodRegion' \
				AND c.'cuenta' = r.'cuenta' \
				AND c.'tipo_de_pago' = r.'tipo_de_pago' \
		"
		df4 = pd.read_sql_query(consulta, cnx)

		df4['d.Folio'].fillna("--", inplace=True)
		df4['d.mes'].fillna("--", inplace=True)

		meses_mapping = {1 :'1.Ene', 2 :'2.Feb', 3 :'3.Mar', 4 :'4.Abr', 5 :'5.May', 6 :'6.Jun', 7 :'7.Jul', 8 :'8.Ago', 9 :'9.Sep', 10 :'10.Oct', 11 :'11.Nov', 12 :'12.Dic'}
		df4['d.mes'] = df4['d.mes'].map(lambda x: meses_mapping.get(x, x))



		# Crear una condición que verifica si las columnas c.MontoVigente, c.MontoDisponible y c.MontoConsumido son iguales a 0
		condicion = (df4['c.MontoConsumido'] == 0)

		# Si la condición se cumple, establecer las columnas d.MontoVigente, d.MontoDisponible y d.MontoConsumido en 0
		df4.loc[condicion, ['d.MontoVigente', 'd.MontoDisponible', 'd.MontoConsumido']] = 0



		print(df4.columns)

		df4agrupado = df4.groupby(["Unidad Ejecutora", "cuenta", "tipo_de_pago", "DisponibleNacional", "r.MontoDisponible", "c.MontoDisponible", "d.MontoDisponible"]).sum()



		disponible = pd.pivot_table(df4,
							index = ["Unidad Ejecutora", "cuenta", "FolioNacional", "DisponibleNacional", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.rut", "c.Folio", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido", "d.mes", "d.Folio", "d.MontoVigente", "d.MontoDisponible", "d.MontoConsumido"],
							#values = ["monto"],
							#columns = ["proyecto"],
							aggfunc = [np.sum],
							fill_value = 0,
							margins = True
							)


		print(disponible.columns)


		disponible.columns = disponible.columns.droplevel()

		# ----------------------------------------------------------------------------------------------

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' TEST 10 - centralizacion.xlsx', engine='xlsxwriter')
		disponible.to_excel(writer, sheet_name="requerimientos")
		# df4agrupado.to_excel(writer, sheet_name="df4agrupado")
		#pago.to_excel(writer, sheet_name="pago")
		writer.save()
 
if __name__ == '__main__':
	main()


	#73719502