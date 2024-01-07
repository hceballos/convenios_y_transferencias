from PyPDF2 import PdfReader
import glob
import pandas as pd
from lib.resolucionesUrgencia.database.database import Database

class ReadCDP(object):

	def __init__(self, datos):
		self.datos = datos

		cdp = pd.DataFrame()
		for f in glob.glob('./input_excel/resolucionesUrgencia/cdp/*.xlsx', recursive=True):
			print('Procesando  : ', f)
			datos_excel = pd.read_excel(f, 
				converters={'N° CDP': str, 'CODIGO': str, 'CODIGO LINEA DE ACCION': str, 'MONTO TOTAL': int, 'MEMO': str, 'FECHA RECEPCION': str, 'ESTADO': str}, 
				usecols = ['N° CDP', 'PROYECTO', 'NUEVO PROYECTO EMG', 'CODIGO', 'CODIGO LINEA DE ACCION', 'MODALIDAD', 'MONTO TOTAL', 'PLAZAS', 'OBSERVACIONES', 'MEMO', 'SOLICITADO', 'FECHA RECEPCION']
			)
			cdp = cdp.append(datos_excel, ignore_index=True)

		#print(cdp)
		database = Database()
		database.crear_cdp(cdp)