import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
import re
from datetime import datetime

class ApruebaConvenioDataBase(Fuente):

	def formatear_fecha(self, devengo, fecha):
		devengo[fecha] = pd.to_datetime(devengo[fecha])
		devengo[fecha] = devengo[fecha].dt.strftime("%d-%m-%Y")
		return devengo[fecha]


	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos
 
		self.parse_Excel(datos)
 
	def parse_Excel(self, datos):
		devengo = pd.DataFrame()
		for f in glob.glob(datos['apruebaConvenio']): # '../mejorninez/input_excel/apruebaConvenio/*',
			print('Procesando  : ', f)
			df = pd.read_excel(f, converters={ 'Proyecto': str} )
			devengo = devengo.append(df,ignore_index=True)


		#devengo['FechaResolucion'] = pd.to_datetime(devengo['FechaResolucion'])
		#devengo['FechaResolucion'] = devengo['FechaResolucion'].dt.strftime("%d-%m-%Y")

		self.formatear_fecha(devengo, 'FechaResolucion' )
		self.formatear_fecha(devengo, 'FechaConvenio' )
		self.formatear_fecha(devengo, 'FechaInicioProyecto' )
		self.formatear_fecha(devengo, 'FechaPrimerDiaNoPago' )


		devengo['Analisis']	= 'Pendiente'
		self.crear_database(devengo)

	def crear_database(self, devengo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///ApruebaConvenio.db', echo=False)
		metadata = sqlalchemy.MetaData()
 
		CodProyectos = sqlalchemy.Table(
			'apruebaConvenio',
			metadata,
			sqlalchemy.Column('Proyecto', sqlalchemy.String, primary_key=True),
			sqlalchemy.Column('Resolucion', sqlalchemy.String),
			sqlalchemy.Column('FechaResolucion', sqlalchemy.String),
			sqlalchemy.Column('FechaConvenio', sqlalchemy.String),
			sqlalchemy.Column('TipoResolucion', sqlalchemy.String),
			sqlalchemy.Column('FechaInicioProyecto', sqlalchemy.String),
			sqlalchemy.Column('FechaPrimerDiaNoPago', sqlalchemy.String),
			sqlalchemy.Column('Materia', sqlalchemy.String),
			sqlalchemy.Column('Cobertura(N Plazas)', sqlalchemy.String),
			sqlalchemy.Column('SexoDeLaPoblacionAtendida', sqlalchemy.String)
		)

		metadata.create_all(engine)
 
		self.insertar_Datos(devengo, engine)
 
	def insertar_Datos(self, devengo, engine):
		devengo.to_sql('apruebaConvenio', engine, if_exists='replace')
