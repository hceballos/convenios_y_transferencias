import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente

class Database(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		self.parse_Excel(datos)

	def parse_Excel(self, datos):

		ruts = pd.DataFrame()
		for f in glob.glob(datos['nombrerutyfirma']):
			df = pd.read_excel(f, converters={ 'ruts': str } )
			print('Procesando  : ', f)
			ruts = ruts.append(df,ignore_index=True)

		def formatear_run(run):
			partes = run.split('-')
			parte_numerica = partes[0]
			parte_dv = partes[1]
			
			# Formatear la parte numérica con puntos de miles
			parte_numerica_formateada = '{:,}'.format(int(parte_numerica)).replace(',', '.')
			
			# Unir la parte formateada con el dígito verificador
			run_formateado = f'{parte_numerica_formateada}-{parte_dv}'
			
			return run_formateado

		# Aplicar la función a la columna 'run'
		ruts['rut'] = ruts['ruts'].apply(formatear_run)
		ruts['rut'] = 'https://www.nombrerutyfirma.com/rut?term='+ruts['rut']

		self.crear_database(ruts['rut'])

	def crear_database(self, ruts):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///nombreRut.db', echo=False)
		metadata = sqlalchemy.MetaData()

		Asigfe = sqlalchemy.Table(
			'nombreRut',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
			sqlalchemy.Column('rut', sqlalchemy.String),
			sqlalchemy.Column('Estatus', sqlalchemy.String)
		)

		metadata.create_all(engine)

		self.insertar_Datos(ruts, engine)

	def insertar_Datos(self, ruts, engine):
		ruts.to_sql('nombreRut', engine, if_exists='replace')