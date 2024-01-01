import sqlalchemy
import pandas as pd
import glob
import sqlite3
import numpy as np
from datetime import datetime
from datetime import date
import re
import xlrd
import csv
import os


class Informes(object):


	def __init__(self):

		# Quiz()
		
		self.selectSubCategorias()

	def selectSubCategorias(self):
		cnx = sqlite3.connect('database.db')
		consulta = " \
			SELECT \
				estadoEjecucionPresupuestaria.'Concepto Presupuestario', \
				estadoEjecucionPresupuestaria.'Ley de Presupuestos ', \
				estadoEjecucionPresupuestaria.'Requerimiento', \
				estadoEjecucionPresupuestaria.'Saldo por Aplicar', \
				estadoEjecucionPresupuestaria.'Compromiso', \
				estadoEjecucionPresupuestaria.'Saldo por Comprometer', \
				estadoEjecucionPresupuestaria.'Devengado', \
				estadoEjecucionPresupuestaria.'Saldo por Devengar', \
				estadoEjecucionPresupuestaria.'Efectivo' \
			FROM \
				estadoEjecucionPresupuestaria \
			WHERE \
				estadoEjecucionPresupuestaria.'Concepto Presupuestario' like '24010%' \
			ORDER BY \
				estadoEjecucionPresupuestaria.'Concepto Presupuestario' asc \
		"
		lineaDeAccion = pd.read_sql_query(consulta, cnx)

		# --------------------------------------------------------------------------------------------------------------------------------

		consulta = " \
			SELECT \
				ea.'Concepto Presupuestario', \
				clas.'NumeroRegionOrden' as 'Unidades Demandantes', \
				ea.'Requerimiento', \
				ea.'Saldo por Aplicar', \
				ea.'Compromiso', \
				ea.'Saldo por Comprometer', \
				ea.'Devengado', \
				ea.'Saldo por Devengar', \
				ea.'Efectivo' \
			FROM \
				(SELECT estadoEjecucionPresupuestariaAvanzado.* FROM estadoEjecucionPresupuestariaAvanzado) ea \
				LEFT JOIN(SELECT clasificador.* FROM clasificador)clas  ON ea.'Unidades Demandantes' = clas.'NumeroRegion' \
			WHERE \
				ea.'Concepto Presupuestario' like '24010%' \
			ORDER BY \
				ea.'Concepto Presupuestario' ASC, \
				clas.'NumeroRegionOrden' \
		"
		region = pd.read_sql_query(consulta, cnx)

		# --------------------------------------------------------------------------------------------------------------------------------

		consulta = " \
			SELECT \
				disponibilidadCompromiso.'Concepto Presupuesto', \
				disponibilidadCompromiso.'Unidad Ejecutora', \
				disponibilidadCompromiso.'Título', \
				disponibilidadCompromiso.'Número Identificación', \
				disponibilidadCompromiso.'Principal', \
				disponibilidadCompromiso.'Monto Vigente' as 'Monto Vigente (Comprometido)', \
				disponibilidadCompromiso.'Monto Consumido' as 'Monto Consumido (Devengado)', \
				disponibilidadCompromiso.'Monto Disponible' as 'Monto Disponible (Saldo por Devengar)' \
			FROM \
				disponibilidadCompromiso \
			WHERE \
				disponibilidadCompromiso.'Concepto Presupuesto' like '24010%' \
			ORDER BY \
				disponibilidadCompromiso.'Concepto Presupuesto' ASC, \
				disponibilidadCompromiso.'Unidad Ejecutora' ASC, \
				disponibilidadCompromiso.principal ASC \
		"
		financiamiento = pd.read_sql_query(consulta, cnx)

		# ----------------------------------------------------------------------------------------------

		consulta = " \
			SELECT \
				Compromiso.* \
			FROM \
				Compromiso \
			WHERE \
				Compromiso.'Concepto' like '24010%' \
				and Compromiso.'Concepto' != '2401006 Oficinas de Protección de Derechos' \
		"
		df = pd.read_sql_query(consulta, cnx)
		df['year'] = pd.DatetimeIndex(df['fechaGeneracion']).year
		df['mes']  = pd.DatetimeIndex(df['fechaGeneracion']).month
		# ----------------------------------------------------------------------------------------------
		compromisoMensual = pd.pivot_table(df,
							index = ["concepto"],
							values = ["monto"],
							columns = ["year", "mes"],
							aggfunc = [np.sum],
							fill_value = 0,
							margins = True
							)
		compromisoMensual.rename(columns={1 :'Ene', 2 :'Feb', 3 :'Mar', 4 :'Abr', 5 :'May', 6 :'Jun', 7 :'Jul', 8 :'Ago', 9 :'Sep', 10 :'Oct', 11 :'Nov', 12 :'Dic', 'Principal':'principal', 'Monto Documento':'montoDocumento', 'Fecha Generación':'fechaGeneracion', 'Folio':'folio', 'Título':'titulo', 'Número Documento': 'numero', 'Fecha Documento':'fechaDocumento', 'Tipo Documento':'tipoDocumento','Monto Documento.1':'monto'}, index={'Concepto':'Linea de acción'}, inplace=True)
		# ----------------------------------------------------------------------------------------------
		financiamientoCompromiso_1 = pd.pivot_table(df,
							index = ["NombreConcepto", "titulo"],
							values = ["monto"],
							columns = ["year", "mes"],
							aggfunc = [np.sum],
							fill_value = 0,
							margins = True
							)
		financiamientoCompromiso_1.rename(columns={1 :'Ene', 2 :'Feb', 3 :'Mar', 4 :'Abr', 5 :'May', 6 :'Jun', 7 :'Jul', 8 :'Ago', 9 :'Sep', 10 :'Oct', 11 :'Nov', 12 :'Dic', 'Principal':'principal', 'Monto Documento':'montoDocumento', 'Fecha Generación':'fechaGeneracion', 'Folio':'folio', 'Título':'titulo', 'Número Documento': 'numero', 'Fecha Documento':'fechaDocumento', 'Tipo Documento':'tipoDocumento','Monto Documento.1':'monto'}, index={'Concepto':'Linea de acción'}, inplace=True)
		# ----------------------------------------------------------------------------------------------
		consulta = " \
			SELECT \
				c.*, \
				clas.*, \
				req.'Unidad Ejecutora' \
			FROM \
				(SELECT estadoEjecucionPresupuestariaAvanzado.* FROM estadoEjecucionPresupuestariaAvanzado WHERE estadoEjecucionPresupuestariaAvanzado.'Concepto Presupuestario' like '2401001%' ) c \
				LEFT JOIN(SELECT clasificador.* FROM clasificador)clas  ON c.'Unidades Demandantes' = clas.'NumeroRegion' \
				LEFT JOIN(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos)req ON c.'Unidades Demandantes' = req.'Unidad Ejecutora' \
		"
		union = pd.read_sql_query(consulta, cnx)
		# ----------------------------------------------------------------------------------------------
		consulta = " \
			SELECT \
				pago.*, \
				retencion.* \
			FROM \
						( \
						SELECT \
						--(reportePago.'MES ATENCION' || reportePago.'COD PROYECTO') AS id, \
						reportePago.'MES ATENCION', \
						reportePago.'TIPO PAGO', \
						reportePago.'COD PROYECTO', \
						reportePago.'MONTO LIQUIDO PAGADO', \
						reportePago.'NRO DIAS' \
						FROM reportePagO) pago \
					LEFT JOIN \
						( \
						SELECT \
						--(retenciones.'Periodo de Atención a Levantar o Retener' || retenciones.'Código ') AS id, \
						retenciones.'Periodo de Atención a Levantar o Retener', \
						retenciones.'Código ', \
						retenciones.'SI Presenta Rend. De Cuenta', \
						retenciones.'NO Presenta Rend. De Cuenta' \
						FROM \
						retenciones) retencion \
					ON pago.'COD PROYECTO' = retencion.'Código ' and pago.'MES ATENCION' = retencion.'Periodo de Atención a Levantar o Retener' \
		"
		reportePago = pd.read_sql_query(consulta, cnx)
		
		# ----------------------------------------------------------------------------------------------

		writer = pd.ExcelWriter('informe.xlsx', engine='xlsxwriter')
		lineaDeAccion.to_excel(writer, sheet_name='Linea de acción')
		region.to_excel(writer, sheet_name='Linea de acción x Región')
		financiamiento.to_excel(writer, sheet_name='Financiamiento & OCA')
		compromisoMensual.to_excel(writer, sheet_name='Compromiso Mensual')
		financiamientoCompromiso_1.to_excel(writer, sheet_name='financiamiento Compromiso 1')
		reportePago.to_excel(writer, sheet_name='reportePago')
		union.to_excel(writer, sheet_name='union')
		writer.save()



