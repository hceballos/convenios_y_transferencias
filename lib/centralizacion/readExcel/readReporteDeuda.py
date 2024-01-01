import pandas as pd
import glob
from lib.centralizacion.database.database import Database

class ReadReporteDeuda:
	def __init__(self, datos):
		self.datos = datos

		deuda = pd.DataFrame()
		for f in glob.glob('./input_excel/centralizacion/reporteDeuda/*.xlsx', recursive=True):
			print('Procesando  : ', f)
			deuda_actual = pd.read_excel(f, converters={
				'CUENTA': str,
				'Costo NNA': int,
				'cod_Proyecto': str,
				'NroPlazas': int,
				'Monto Convenio 2021': int,
				'Monto Fijo': int,
				'Monto Cuota': int,
				'Monto Variable': int,
				'Factor USS': int
				} )
			deuda = deuda.append(deuda_actual, ignore_index=True)

		deuda['Analisis']      = 'Pendiente'
		deuda.rename(columns={
			'Código Proyecto' : 'cod_proyecto',
			'Fecha Actualización' : 'fecha_Actualizacion',
			'Observación' : 'observacion',
			'N° Cuota' : 'n_Cuota'
			}, inplace=True)

		deuda['fecha'] 		= pd.to_datetime(deuda['Fecha Vencimiento'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
		deuda['numero_mes'] = deuda['fecha'].dt.month.map("{:02d}".format)

		database = Database()
		database.crear_deuda(deuda)