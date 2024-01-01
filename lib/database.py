import sqlalchemy
from datetime import datetime



class Database(object):

	def databaseCompromiso(self, compromiso):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'compromiso',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('Concepto', sqlalchemy.String),
			sqlalchemy.Column('Principal', sqlalchemy.String),
			sqlalchemy.Column('Monto Documento', sqlalchemy.BigInteger),
			sqlalchemy.Column('Tipo Vista', sqlalchemy.String),
			sqlalchemy.Column('Fecha', sqlalchemy.String),
			sqlalchemy.Column('Folio', sqlalchemy.String),
			sqlalchemy.Column('Título', sqlalchemy.String),
			sqlalchemy.Column('Etapa Compromiso', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('Tipo Documento', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True)
			)

		metadata.create_all(engine)
		compromiso.to_sql('compromiso', engine, if_exists='replace')


	def databaseDevengo(self, devengo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'devengo',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		devengo.to_sql('devengo', engine, if_exists='replace')


	def databaseDisponibilidadCompromiso(self, disponibilidadCompromiso):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'disponibilidadCompromiso',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		disponibilidadCompromiso.to_sql('disponibilidadCompromiso', engine, if_exists='replace')

	def databaseDisponibilidadDevengo(self, disponibilidadDevengo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'disponibilidadDevengo',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('Fecha Documento', sqlalchemy.DateTime),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		disponibilidadDevengo.to_sql('disponibilidadDevengo', engine, if_exists='replace')


	def databaseDisponibilidadRequerimientos(self, disponibilidadRequerimientos):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'disponibilidadRequerimientos',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		disponibilidadRequerimientos.to_sql('disponibilidadRequerimientos', engine, if_exists='replace')


	def databaseEstadoEjecucionPresupuestaria(self, estadoEjecucionPresupuestaria):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'estadoEjecucionPresupuestaria',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		estadoEjecucionPresupuestaria.to_sql('estadoEjecucionPresupuestaria', engine, if_exists='replace')

	def databaseEstadoEjecucionPresupuestariaAvanzado(self, estadoEjecucionPresupuestariaAvanzado):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'estadoEjecucionPresupuestariaAvanzado',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		estadoEjecucionPresupuestariaAvanzado.to_sql('estadoEjecucionPresupuestariaAvanzado', engine, if_exists='replace')


	def databaseClasificador(self, clasificador):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'clasificador',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		clasificador.to_sql('clasificador', engine, if_exists='replace')







	def databaseRetenciones(self, acepta):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'retenciones',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.BigInteger),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		acepta.to_sql('retenciones', engine, if_exists='replace')



	def databaseRetencionesCalculoPago(self, acepta):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///calculoPrevioPago.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'retenciones',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.BigInteger),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		acepta.to_sql('retenciones', engine, if_exists='replace')



	def databasePagoManual(self, acepta):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'pagoManual',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.DateTime),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		acepta.to_sql('pagoManual', engine, if_exists='replace')


	def databaseReportePago(self, acepta):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'reportePago',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.DateTime),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		acepta.to_sql('reportePago', engine, if_exists='replace')



	def databaseReporte_FES(self, acepta):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///calculoPrevioPago.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'reporte_FES',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.DateTime),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		acepta.to_sql('reporte_FES', engine, if_exists='replace')



	def databaseMalla(self, acepta):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///calculoPrevioPago.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'malla',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.DateTime),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		acepta.to_sql('malla', engine, if_exists='replace')


	def databaseFes(self, fes):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'fes',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.BigInteger),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		fes.to_sql('fes', engine, if_exists='replace')


	def databaseMasivo(self, masivo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'masivo',
			metadata,
			sqlalchemy.Column('Fecha de Recepción', sqlalchemy.BigInteger),
			sqlalchemy.Column('Region', sqlalchemy.String),
			sqlalchemy.Column('Periodo de Atención a Levantar o Retener', sqlalchemy.String),
			sqlalchemy.Column('Código ', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Nombre del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Código OCA', sqlalchemy.String),
			sqlalchemy.Column('Nombre OCA', sqlalchemy.String),
			sqlalchemy.Column('SI Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('NO Presenta Rend. De Cuenta', sqlalchemy.String),
			sqlalchemy.Column('Fecha Recepcion R.C.', sqlalchemy.DateTime),
			sqlalchemy.Column('Monto de la R.C.', sqlalchemy.String),
			sqlalchemy.Column('USUFI Responsable del Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Coordinador Usufi Regional', sqlalchemy.String),
			sqlalchemy.Column('Observaciones', sqlalchemy.String),
			sqlalchemy.Column('PRESENTÓ', sqlalchemy.String)
			)

		metadata.create_all(engine)
		masivo.to_sql('masivo', engine, if_exists='replace')


	def databaseconsolidadoRendicionDeCuentas(self, consolidadoRendicionDeCuentas):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'consolidadoRendicionDeCuentas',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		consolidadoRendicionDeCuentas.to_sql('consolidadoRendicionDeCuentas', engine, if_exists='replace')


	def databaseRetenidos(self, retenidos):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'retenidos',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		retenidos.to_sql('HayQueRetener', engine, if_exists='replace')


	def databaseAprobados(self, aprobados):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'aprobados',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		aprobados.to_sql('HayQueLevantar', engine, if_exists='replace')


	def databaseFes(self, fes):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'fes',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)

		metadata.create_all(engine)
		fes.to_sql('fes', engine, if_exists='replace')


	def databasePresentaronAhorayAntes(self, presentaronAhorayAntes):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'presentaronAhorayAntes',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)
		metadata.create_all(engine)
		presentaronAhorayAntes.to_sql('presentaronAhorayAntes', engine, if_exists='replace')



	def databasecentralizaciones(self, centralizaciones):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		OrdenDeCompra = sqlalchemy.Table(
			'centralizaciones',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer),
			sqlalchemy.Column('concepto', sqlalchemy.String),
			sqlalchemy.Column('principal', sqlalchemy.String),
			sqlalchemy.Column('montoDocumento', sqlalchemy.BigInteger),
			sqlalchemy.Column('fechaGeneracion', sqlalchemy.String),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('titulo', sqlalchemy.String),
			sqlalchemy.Column('numero', sqlalchemy.String),
			sqlalchemy.Column('fechaDocumento', sqlalchemy.String),
			sqlalchemy.Column('tipoDocumento', sqlalchemy.String),
			sqlalchemy.Column('monto', sqlalchemy.BigInteger),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('unico', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('ordenDeCompra', sqlalchemy.String),
			sqlalchemy.Column('status', sqlalchemy.String),
			sqlalchemy.Column('year', sqlalchemy.String),
			sqlalchemy.Column('mes', sqlalchemy.String)
			)
		metadata.create_all(engine)
		centralizaciones.to_sql('centralizaciones', engine, if_exists='replace')
