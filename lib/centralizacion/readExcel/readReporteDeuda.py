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
		deuda = deuda[deuda['Monto Cuota'].notna()]

		deuda['Analisis']      = 'Pendiente'
		deuda.rename(columns={
			'Código Proyecto' : 'cod_proyecto',
			'Fecha Actualización' : 'fecha_Actualizacion',
			'Observación' : 'observacion',
			'N° Cuota' : 'n_Cuota'
			}, inplace=True)

		deuda['numero_mes'] = pd.to_datetime(deuda['Fecha Vencimiento'], format='%d-%m-%Y %H:%M:%S').dt.month.map("{:02d}".format)
		#deuda['unico'] 		= deuda['unico'] = deuda['cod_proyecto'].astype(str) + deuda['Tipo'] + deuda['numero_mes'].astype(str) + deuda['Estado Cuota']
		deuda.reset_index(drop=True, inplace=True)

		database = Database()
		database.crear_deuda(deuda)