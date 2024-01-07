from PyPDF2 import PdfReader
import glob
import pandas as pd
from lib.resolucionesUrgencia.database.database import Database

class ReadReporte_resoluciones(object):

	def __init__(self, datos):
		self.datos = datos

		resoluciones = pd.DataFrame()
		for f in glob.glob('./input_excel/resolucionesUrgencia/reporte_resoluciones/*.xlsx', recursive=True):
			print('Procesando  : ', f)
			datos_excel = pd.read_excel(f, 
				converters={'N° CDP': str, 'CODIGO': str, 'CODIGO LINEA DE ACCION': str, 'MONTO TOTAL': int, 'MEMO': str, 'FECHA RECEPCION': str, 'ESTADO': str}, 
			)
			resoluciones = resoluciones.append(datos_excel, ignore_index=True)

		#print(resoluciones)
		database = Database()
		database.crear_resoluciones(resoluciones)