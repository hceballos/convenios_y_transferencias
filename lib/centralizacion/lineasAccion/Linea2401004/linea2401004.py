import pandas as pd
import glob
from lib.centralizacion.database.database import Database
import re

class Linea2401004:

	def __init__(self, dataframe):

		# print(dataframe)

		# Aplicar la condición y asignar valores a la columna 'Recalculado'
		# transferencias.loc[	(transferencias['decreto'] == '481') & (transferencias['tipo_pago'] == 'ANTICIPO'	), 'Recalculado'] = 'ANTICIPO'
		# transferencias.loc[	(transferencias['decreto'] == '481') & (transferencias['tipo_pago'] == '80BIS'		), 'Recalculado'] = '80BIS'
		# transferencias.loc[	(transferencias['decreto'] == '481') & (transferencias['tipo_pago'] == 'URGENCIA'	), 'Recalculado'] = 'URGENCIA'
		# transferencias.loc[	(transferencias['decreto'] == '481') & (transferencias['tipo_pago'] == 'EMERGENCIA'	), 'Recalculado'] = 'EMERGENCIA'
		# transferencias.loc[	(transferencias['decreto'] == '481') & (transferencias['tipo_pago'] == 'OTROSPAGOS'), 'Recalculado'] = 'OTROSPAGOS'

		# transferencias.loc[	(transferencias['decreto'] == '19') & (transferencias['tipo_pago'] == 'ANTICIPO'	), 'Recalculado'] = 'ANTICIPO'
		# transferencias.loc[	(transferencias['decreto'] == '19') & (transferencias['tipo_pago'] == '80BIS'		), 'Recalculado'] = '80BIS'
		# transferencias.loc[	(transferencias['decreto'] == '19') & (transferencias['tipo_pago'] == 'URGENCIA'	), 'Recalculado'] = 'URGENCIA'
		# transferencias.loc[	(transferencias['decreto'] == '19') & (transferencias['tipo_pago'] == 'EMERGENCIA'	), 'Recalculado'] = 'EMERGENCIA'
		# transferencias.loc[	(transferencias['decreto'] == '19') & (transferencias['tipo_pago'] == 'OTROSPAGOS'	), 'Recalculado'] = 'OTROSPAGOS'

		# transferencias.loc[	(transferencias['decreto'] == '07') & (transferencias['tipo_pago'] == 'ANTICIPO'	), 'Recalculado'] = 'ANTICIPO'
		# transferencias.loc[	(transferencias['decreto'] == '07') & (transferencias['tipo_pago'] == '80BIS'		), 'Recalculado'] = '80BIS'
		# transferencias.loc[	(transferencias['decreto'] == '07') & (transferencias['tipo_pago'] == 'URGENCIA'	), 'Recalculado'] = 'URGENCIA'
		# transferencias.loc[	(transferencias['decreto'] == '07') & (transferencias['tipo_pago'] == 'EMERGENCIA'	), 'Recalculado'] = 'EMERGENCIA'
		# transferencias.loc[	(transferencias['decreto'] == '07') & (transferencias['tipo_pago'] == 'OTROSPAGOS'	), 'Recalculado'] = 'OTROSPAGOS'


		# mask01 = dataframe['cuenta'] == '2401004'
		# dataframe.loc[mask01, 'Recalculado'] 	= (dataframe[mask01]['plazas_atendidas'] * dataframe[mask01]['factor_variable'] * (1 + dataframe[mask01]['asignacion_zona'] / 100) * dataframe[mask01]['uss']).round().astype(int)
		# dataframe.loc[mask01, 'diferencia'] 	= dataframe[mask01]['monto_liquido_pagado'] - round(dataframe[mask01]['plazas_atendidas'] * dataframe[mask01]['factor_variable'] * (1 + dataframe[mask01]['asignacion_zona'] / 100.0) * dataframe[mask01]['uss'])
		
		print("El número total de filas es:", len(dataframe))

		database = Database()
		database.crear_transferencias(dataframe)