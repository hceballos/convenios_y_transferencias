import sqlalchemy
import pandas as pd
import glob
import sqlite3
from lib.fuente import Fuente


class Database(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos
		self.parse_Excel(datos)

	def parse_Excel(self, datos):
		pagos = pd.DataFrame()
		for f in glob.glob(datos['excel_path']):
			df = pd.read_excel(f )
			print('Procesando  : ', f)
			pagos = pagos.append(df,ignore_index=True)

		pagos['status_Monto'] = "pendiente"
		pagos['status_Plazas'] = "pendiente"
		pagos['status_Atenciones'] = "pendiente"
		pagos['status_DiasAtendidos'] = "pendiente"
		pagos['Fecha'] = pd.to_datetime(pagos['Fecha']).dt.date

		del pagos['Unnamed: 17']
		del pagos['LLAVE UNICA']
		del pagos['LLAVE LARGA']
		del pagos['OBSERVACION']
		del pagos['Tipo']
		del pagos['Proyecto']
		del pagos['Plazas Convenio']
		del pagos['OBSERVACIÓN']

		print(pagos)

		self.crear_database(pagos)

	def crear_database(self, pagos):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
		metadata = sqlalchemy.MetaData()

		Asigfe = sqlalchemy.Table(
			'pagos',
			metadata,
			sqlalchemy.Column('Región', sqlalchemy.String),
			sqlalchemy.Column('Cod. Proyecto', sqlalchemy.String),
			sqlalchemy.Column('Monto Total', sqlalchemy.Integer),
			sqlalchemy.Column('Nº CDP', sqlalchemy.BigInteger),
			sqlalchemy.Column('AÑO CDP', sqlalchemy.String),
			sqlalchemy.Column('Resolución', sqlalchemy.String),
			sqlalchemy.Column('Fecha', sqlalchemy.Date),
			sqlalchemy.Column('OBSERVACION.1', sqlalchemy.String),
			sqlalchemy.Column('status_Monto', sqlalchemy.String),
			sqlalchemy.Column('status_Plazas', sqlalchemy.String),
			sqlalchemy.Column('status_Atenciones', sqlalchemy.String),
			sqlalchemy.Column('status_DiasAtendidos', sqlalchemy.String)
		)

		metadata.create_all(engine)

		self.insertar_Datos(pagos, engine)

	def insertar_Datos(self, pagos, engine):
		pagos.to_sql('pagos', engine, if_exists='replace')


json_path = r'/Users/hector/Documents/desarrollo/mejorninez/data/data.json'

if __name__ == '__main__':
	Database(json_path)