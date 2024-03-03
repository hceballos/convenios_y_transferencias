import sqlalchemy

class Database(object):


	def databaseScrapy(self, transferencias):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'scrapy',
			metadata,
			sqlalchemy.Column('ID_Pago', sqlalchemy.String), 
			sqlalchemy.Column('Region', sqlalchemy.String), 
			sqlalchemy.Column('Fecha_Pago', sqlalchemy.String), 
			sqlalchemy.Column('Cod_Proyecto', sqlalchemy.String), 
			sqlalchemy.Column('Nombre_Proyecto', sqlalchemy.String), 
			sqlalchemy.Column('Monto', sqlalchemy.String), 
			sqlalchemy.Column('Estado', sqlalchemy.String), 
			sqlalchemy.Column('Plazas', sqlalchemy.String), 
			sqlalchemy.Column('Mes_Atencion', sqlalchemy.String), 
			sqlalchemy.Column('Folio', sqlalchemy.String), 

			sqlalchemy.Column('Factor_Numero_Plaza', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Fijo', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Edad', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Discapacidad', sqlalchemy.String), 
			sqlalchemy.Column('Factor_CVF', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Tipo_USS', sqlalchemy.String),
			sqlalchemy.Column('Factor_Dias_del_Mes', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Factor_Variable', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Cobertura', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Complejidad', sqlalchemy.String), 
			sqlalchemy.Column('Factor_Porcentaje_Zona', sqlalchemy.String), 
			sqlalchemy.Column('Factor_USS', sqlalchemy.String), 

			sqlalchemy.Column('Tipo_de_Pago', sqlalchemy.String), 
			sqlalchemy.Column('Plazas_Convenidas', sqlalchemy.String), 
			sqlalchemy.Column('Plazas_Atendidas', sqlalchemy.String), 
			sqlalchemy.Column('Plazas_Normales_Atendidas', sqlalchemy.String), 
			sqlalchemy.Column('Dias_Atendidos', sqlalchemy.String), 
			sqlalchemy.Column('Liquido_Pagado', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Convenido_Fijo', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Convenido_Variable', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Convenido_Total', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Atencion_Fijo', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Atencion_Variable', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Atencion_Total', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Normal_Fijo', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Normal_Variable', sqlalchemy.String), 
			sqlalchemy.Column('Monto_Normal_Total', sqlalchemy.String), 
			sqlalchemy.Column('Nro_dias_Mes', sqlalchemy.String), 
			sqlalchemy.Column('Estado', sqlalchemy.String), 

			sqlalchemy.Column('80B_Bis_Plazas_Analisis', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Monto_a_Pago_fijo_Analisis', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Monto_a_Pago_variable_Analisis', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Monto_a_Pago_total_Analisis', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Plazas', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Monto_a_Pago_fijo', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Monto_a_Pago_variable', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Monto_a_Pago_total', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_NRO', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_ANIO', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_resolucion_pago', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_fecha', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Observacion', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Estado_CDP', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Estado_Transferencia', sqlalchemy.String), 
			sqlalchemy.Column('Urgencia_Fecha_Transferencia', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Plazas', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Monto_a_Pago_fijo', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Monto_a_Pago_variable', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Monto_a_Pago_total', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_NRO', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_ANIO', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_resolucion_pago', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_fecha', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Observacion', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Estado_CDP', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Estado_Transferencia', sqlalchemy.String), 
			sqlalchemy.Column('80B_Bis_Fecha_Transferencia', sqlalchemy.String)
		)

		metadata.create_all(engine)




	def databaseDisponibilidadCompromiso(self, disponibilidadCompromiso):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'disponibilidadCompromiso',
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
		disponibilidadCompromiso.to_sql('disponibilidadCompromiso', engine, if_exists='replace')



	def databaseDisponibilidadRequerimientos(self, disponibilidadRequerimientos):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'disponibilidadRequerimientos',
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
		disponibilidadRequerimientos.to_sql('disponibilidadRequerimientos', engine, if_exists='replace')



	def databaseDisponibilidadDevengo(self, disponibilidadDevengo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'disponibilidadDevengo',
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
		disponibilidadDevengo.to_sql('disponibilidadDevengo', engine, if_exists='replace')




	def crear_Fes(self, fes):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///centralizacion.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'fes',
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
		fes.to_sql('fes', engine, if_exists='replace')





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



