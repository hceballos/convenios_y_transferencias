import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente

class Database(Fuente):
	def __init__(self, datos):


		print("================================ Datos Database ================================ ")
		self.parse_Excel(datos)

	def parse_Excel(self, datos):
		devengo = pd.DataFrame()
		for f in glob.glob(datos['readbis80']): # "../mejorninez/input_excel/pagoManual/*",
			df = pd.read_excel(f, converters={ 'folio': str, 'Nº CDP': str, 'Monto Total': int } )
			print('Procesando  : ', f)
			devengo = devengo.append(df,ignore_index=True)

		devengo['CodProyecto']  =  devengo['Cod. Proyecto']
		devengo['MesAtencion']  =  devengo['Mes Atención']
		devengo['Estatus']  	=  "Pendiente"
		devengo['Diferencia_plazas']  	=  "Pendiente"
		devengo['Diferencia_monto']  	=  "Pendiente"
		del devengo['observacion']   

		self.crear_database(devengo)

	def crear_database(self, devengo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///proyectos.db', echo=False)
		metadata = sqlalchemy.MetaData()

		Asigfe = sqlalchemy.Table(
			'CodProyectos',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('Estatus', sqlalchemy.String)
		)

		metadata.create_all(engine)

		self.insertar_Datos(devengo, engine)

	def insertar_Datos(self, devengo, engine):
		devengo.to_sql('CodProyectos', engine, if_exists='replace')

	########################

class Database_rezagados(Fuente):
	def __init__(self, datos):


		print("================================ Datos Database ================================ ")
		self.parse_Excel(datos)

	def parse_Excel(self, datos):
		devengo = pd.DataFrame()
		for f in glob.glob(datos['readbis80_rezagados']): # "../mejorninez/input_excel/pagoManual/*",
			df = pd.read_excel(f, converters={ 'folio': str, 'Nº CDP': str, 'Monto Total': int } )
			print('Procesando  : ', f)
			devengo = devengo.append(df,ignore_index=True)

		devengo['CodProyecto']  =  devengo['Cod. Proyecto']
		devengo['MesAtencion']  =  devengo['Mes Atención']
		devengo['Estatus']  	=  "Pendiente"
		devengo['Diferencia_plazas']  	=  "Pendiente"
		devengo['Diferencia_monto']  	=  "Pendiente"
		del devengo['observacion']   

		self.crear_database(devengo)

	def crear_database(self, devengo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///proyectos.db', echo=False)
		metadata = sqlalchemy.MetaData()

		Asigfe = sqlalchemy.Table(
			'80_rezagados',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('Estatus', sqlalchemy.String)
		)

		metadata.create_all(engine)

		self.insertar_Datos(devengo, engine)

	def insertar_Datos(self, devengo, engine):
		devengo.to_sql('80_rezagados', engine, if_exists='replace')