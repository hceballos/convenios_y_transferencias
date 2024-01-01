import pandas as pd
import glob
from lib.centralizacion.database.database import Database

class ReadMalla:
	def __init__(self, datos):
		self.datos = datos

		malla = pd.DataFrame()
		for f in glob.glob('./input_excel/centralizacion/malla/*.xlsx', recursive=True):
			print('Procesando  : ', f)
			malla_actual = pd.read_excel(f, converters={
				'CUENTA': str,
				'Costo NNA': int,
				'cod_Proyecto': int,
				'NroPlazas': int,
				'Monto Convenio 2021': int,
				'Monto Fijo': int,
				'Monto Variable': int,
				'Factor USS': int
				} )
			malla = malla.append(malla_actual, ignore_index=True)

		malla['Analisis']      = 'Pendiente'
		malla.rename(columns={'CUENTA' : 'cuenta', 'Costo NNA' : 'costo_NNA', 'REVISIÓN DS 19 y OTROS' : 'revision_DS_19_y_otros', 'CodProyecto' : 'cod_Proyecto', 'CODIGO PADRE' : 'codigo_Padre', 'NombreProyecto' : 'nombre_Proyecto', 'Cod Region' : 'cod_Region', 'Cod Institucion' : 'cod_Institucion', 'Nombre Institucion' : 'mombre_Institucion', 'Des Tipo Proyecto' : 'des_Tipo_Proyecto', 'Nuevas Líneas SMN' : 'nuevas_Líneas_SMN', 'DesTematica' : 'DesTematica', 'Modelo' : 'modelo', 'mod' : 'mod', 'NroPlazas' : 'nro_Plazas', 'Monto Convenio 2021' : 'monto_Convenio_2021', 'Monto Fijo' : 'monto_Fijo', 'Monto Variable' : 'monto_Variable', 'FactorFijo' : 'factor_Fijo', 'Factor Variable' : 'factor_Variable', 'Factor Edad' : 'factor_Edad', 'FactorCobertura' : 'factor_Cobertura', 'factor discapacidad' : 'factor_Discapacidad', 'Factor Complejidad' : 'factor_Complejidad', 'FactorCVF/Factor Edad RVA - RVT' : 'factor_CVF/Factor_Edad_RVA_RVT', 'PorcentajeZona' : 'porcentaje_Zona', 'Factor USS' : 'factor_USS', 'AnoResolucion' : 'ano_Resolucion', 'resol' : 'resol', 'InicioProyecto' : 'inicio_Proyecto', 'TerminoProyecto' : 'termino_Proyecto', 'RutNumeroProyecto' : 'rut_Numero_Proyecto', 'CodBanco' : 'cod_Banco', 'banco' : 'banco', 'CuentaCorrienteNumero' : 'cuenta_Corriente_Numero', 'EdadMinima' : 'edad_Minima', 'EdadMaxima' : 'edad_Maxima', 'nsexo' : 'nsexo', 'Direccion' : 'direccion', 'Comuna' : 'comuna', 'Analisis' : 'analisis'}, inplace=True)

		database = Database()
		database.crear_malla(malla)