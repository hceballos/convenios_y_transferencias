import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
import re

class AnalisisRetenidosDataBase(Fuente):
	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos
 
		self.parse_Excel(datos)
 
	def parse_Excel(self, datos):
		devengo = pd.DataFrame()
		for f in glob.glob(datos['analisisRetenidos']): # '../mejorninez/input_excel/AnalisisRetenidos/*',
			print('Procesando  : ', f, re.search(r'([^/]+)(\.[^.]+$)', f).group(1))
			archivo = re.search(r'([^/]+)(\.[^.]+$)', f).group(1)
			df = pd.read_excel(f, converters={ 'MES_ATENCION': str, 'COD_PROYECTO': str} )
			devengo = devengo.append(df,ignore_index=True)

		devengo['unico']  		 =  devengo['COD_PROYECTO'] + devengo['MES_ATENCION']
		devengo['Analisis'] 	 = 'Pendiente'
		self.crear_database(devengo)

	def crear_database(self, devengo):
		metadata = sqlalchemy.MetaData()
		engine = sqlalchemy.create_engine('sqlite:///AnalisisRetenidos.db', echo=False)
		metadata = sqlalchemy.MetaData()
 
		CodProyectos = sqlalchemy.Table(
			'CodProyectos',
			metadata,
			sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
			sqlalchemy.Column('folio', sqlalchemy.String),
			sqlalchemy.Column('Estatus', sqlalchemy.String)
		)

		scrapy = Table('scrapy', metadata,
			#sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),


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
 
		self.insertar_Datos(devengo, engine)
 
	def insertar_Datos(self, devengo, engine):
		devengo.to_sql('CodProyectos', engine, if_exists='replace')
