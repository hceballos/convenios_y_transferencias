import sqlalchemy
import pandas as pd
import sqlite3


class UnionTables(object):
	def __init__(self):

		self.databaseCFP()

	def databaseCFP(self):

		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				ejecucion.codConcepto as codConcepto, \
				ejecucion.'Concepto Presupuestario', \
				ejecucion.monto, \
				clasificador.categoria, \
				clasificador.subcategoria \
			FROM \
				ejecucion \
				LEFT JOIN clasificador on ejecucion.codConcepto = clasificador.codigo \
		"
		query = pd.read_sql_query(consulta, cnx)

		#writer = pd.ExcelWriter('ejecucion.xlsx', engine='xlsxwriter')
		#query.to_excel(writer, sheet_name='ejecucion')
		#writer.save()

		print('Procesando  : Creando Tabla "Arbol"')

		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		cnx = sqlite3.connect('database.db')
		consulta  = " \
			SELECT \
				clas.categoria as categoria, \
				clas.subcategoria as subcategoria, \
				c.*, \
				a.*, \
				m.*, \
				f.* \
			FROM \
				(SELECT cfp.* FROM cfp)c \
				LEFT JOIN(SELECT acepta.* FROM acepta)a                 ON c.unico	= a.unico \
				LEFT JOIN(SELECT mercadoPublico.*, mercadoPublico.Cantidad as 'mercadoPublicoCantidad' FROM mercadoPublico)m ON a.folio_oc	= m.Codigo  \
				LEFT JOIN(SELECT clasificador.* FROM clasificador)clas  ON c.CodConcepto = clas.codigo \
				LEFT JOIN(SELECT facturas.* FROM facturas)f 			ON c.unico = f.unico \
		"
		df = pd.read_sql_query(consulta, cnx)

		#df['year']	= pd.DatetimeIndex(df['fechaGeneracion']).year
		#df['mes']	= pd.DatetimeIndex(df['fechaGeneracion']).month

		df.to_sql('arbol', engine, if_exists='replace')