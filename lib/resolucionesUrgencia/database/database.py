import sqlalchemy

class Database(object):

	def crear_PDF(self, pdf):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///resolucionesUrgencia.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'pdf',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Convenio_2021', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		pdf.to_sql('pdf', engine, if_exists='replace')



	def crear_ResolucionesExentas(self, resolucionesExentas):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///resolucionesUrgencia.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'resolucionesExentas',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Convenio_2021', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		resolucionesExentas.to_sql('resolucionesExentas', engine, if_exists='replace')


	def crear_resoluciones(self, resoluciones):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///resolucionesUrgencia.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'resoluciones',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Convenio_2021', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		resoluciones.to_sql('resoluciones', engine, if_exists='replace')

	def crear_cdp(self, cdp):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///resolucionesUrgencia.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'cdp',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Convenio_2021', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		cdp.to_sql('cdp', engine, if_exists='replace')

	def crear_rendicionDeCuentas(self, rendicionDeCuentas):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'rendicionDeCuentas',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Convenio_2021', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		rendicionDeCuentas.to_sql('rendicionDeCuentas', engine, if_exists='replace')

	def crear_malla(self, malla):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'malla',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Convenio_2021', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		malla.to_sql('malla', engine, if_exists='replace')
		#print("Éxito en la actualización de la tabla 'malla' en la base de datos 'centralizacion'.")


	def crear_todosLosPagos(self, todosLosPagos):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'todosLosPagos',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('nro_Plazas', sqlalchemy.Integer),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		todosLosPagos.to_sql('todosLosPagos', engine, if_exists='replace')
		#print("Éxito en la actualización de la tabla 'todosLosPagos' en la base de datos 'centralizacion'.")


	def crear_transferencias(self, transferencias):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'transferencias',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('nro_Plazas', sqlalchemy.Integer),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('uss', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		transferencias.to_sql('transferencias', engine, if_exists='replace')
		#print("Éxito en la actualización de la tabla 'transferencias' en la base de datos 'centralizacion'.")

	def crear_retenidos(self, retenidos):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'retenidos',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('nro_Plazas', sqlalchemy.Integer),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('uss', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		retenidos.to_sql('retenidos', engine, if_exists='replace')
		#print("Éxito en la actualización de la tabla 'transferencias' en la base de datos 'centralizacion'.")



	def crear_deuda(self, deuda):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'deuda',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('cuenta', sqlalchemy.String),
			sqlalchemy.Column('costo_NNA', sqlalchemy.Integer),
			sqlalchemy.Column('cod_Proyecto', sqlalchemy.String),
			sqlalchemy.Column('nro_Plazas', sqlalchemy.Integer),
			sqlalchemy.Column('mes_atencion', sqlalchemy.String),
			sqlalchemy.Column('monto_Fijo', sqlalchemy.Integer),
			sqlalchemy.Column('monto_Variable', sqlalchemy.Integer),
			sqlalchemy.Column('factor_USS', sqlalchemy.Integer, primary_key=True)
			)

		metadata.create_all(engine)
		deuda.to_sql('deuda', engine, if_exists='replace')
		#print("Éxito en la actualización de la tabla 'deuda' en la base de datos 'centralizacion'.")



