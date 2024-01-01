# python mainValidacion.py --operation report
# DisponibilidadDeDevengo - 121060101
import argparse
from lib.validacion import Database
from lib.analisisRetenidos import AnalisisRetenidos
from lib.analisisRetenidosDataBase import AnalisisRetenidosDataBase
from lib.analisisRetenidosReport import AnalisisRetenidosReport
from lib.apruebaConvenioDataBase import ApruebaConvenioDataBase
from lib.apruebaConvenio import ApruebaConvenio
from lib.sisValidacion import SisValidacion
from lib.sisValidacionTest import SisValidacionTest
from lib.sisValidacionTest1 import SisValidacionTest1
from lib.sisValidacion80Bis import SisValidacion80Bis
from lib.hayQueRetener import SisHayQueRetener
from lib.sisValidacion_Sandra import SisValidacion_Sandra
from lib.sisDescargas import SisDescargasPagosAprobados, SisDescargasPagosRetenidos, SisDescargasTransferencias
from lib.sisValidacion_urgencias import SisValidacion_urgencias
from lib.sisCalculoAFEdescarga import Descargas
from lib.sisCalculoAFEReadExcel import ReadExcel
from lib.sisCalculoAFEParse import Parse
from lib.sisCalculoAFEParseLevantar import ParseLevantar
from lib.sisCalculoAFEParseLevantar import ParseLevantar

from lib.scrapingSigfeReports import ScrapingSigfeReports
from lib.scrapingSigfeReports_backup import ScrapingSigfeReportsDisponibilidad
from lib.scrapingSigfeReportsPresupuesto import ScrapingSigfeReportsPresupuesto
from lib.readRetenciones  import ReadRetenciones
from lib.readCompromiso import ReadCompromiso
from lib.readDevengo import ReadDevengo
from lib.readReportePago import Pago, CalculoPago
from lib.readconsolidadoRendicionDeCuentas import ConsolidadoRendicionDeCuentas, Fes, HayQueRetener, HayQueLevantar, UnionTablas, Merge
#from lib.merge import Merge_Fes_ConsolidadoRC, Merge_Retenidos_ConsolidadoRC
from lib.calculoPrevioPago import Reporte_FES
from lib.calculoPrevioPago import Malla
from lib.calculoPrevioPago import Calculos
from lib.readDisponibilidadCompromisoPresupuestarios import ReadDisponibilidadCompromisoPresupuestarios
from lib.readDisponibilidadDevengoPresupuestarios import ReadDisponibilidadDevengoPresupuestarios
from lib.readDisponibilidadRequerimientosPresupuestarios import ReadDisponibilidadRequerimientosPresupuestarios
from lib.readEstadoEjecucionPresupuestaria import ReadEstadoEjecucionPresupuestaria
from lib.informe import Informes
from lib.informeRequerimiento import InformeRequerimiento
from lib.centralizacion.centralizacion import Centralizacion
from lib.plazoDeLaDeuda import PlazoDeLaDeuda
import time

json_path = r'../mejorninez/data/data.json'

if __name__ == '__main__':

	"""
	while True:

		try:
			parser = argparse.ArgumentParser()
			parser.add_argument("--80Bis", help="80Bis")
			parser.add_argument("--analisisRetenidos", help="analisisRetenidos")
			parser.add_argument("--operation", help="operation", choices=["80Bis", "analisisRetenidos"])
			args = parser.parse_args()

			if args.operation == '80Bis':
				SisValidacion80Bis(json_path)

			#if args.operation == 'analisisRetenidos':
			#	AnalisisRetenidos(json_path)
		except Exception as e:
			print("Ocurrió un error:", str(e))
			continue

		break
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument("--db",             				help="Lectura excel de pago manual y Genera la base de datos para validar RU o 80 BIS.")
	parser.add_argument("--Hector",         				help="Valida en SIS los RU o 80 Bis con usario de Hector")
	parser.add_argument("--HectorTest",						help="Valida en SIS los RU o 80 Bis con usario de Hector")	
	parser.add_argument("--calculoPrevioPago",				help="Descarga de Comprobante de Liquidación de Fondos - listado de tesoreria")
	parser.add_argument("--Sandra",         				help="Valida en SIS los RU o 80 Bis con usario de Sandra")
	parser.add_argument("--Alvaro",         				help="Descarga de Comprobante de Liquidación de Fondos - listado de tesoreria")
	parser.add_argument("--prueba_elementos", 				help="Desde sigfe devengo extrae la informacion de ID y Numero de Orden de compra con usuario prueba_elementos")
	parser.add_argument("--mercadoPublico", 				help="scraping mercado publico - contenido de orden de compra")
	parser.add_argument("--tesoreria",      				help="Descarga de Comprobante de Liquidación de Fondos - listado de tesoreria")
	parser.add_argument("--xpert",          				help="intranet xpert")
	parser.add_argument("--retener",	      				help="retener")
	parser.add_argument("--retencionesLevantamientos",		help="retencionesLevantamientos")
	parser.add_argument("--sigfe",          				help="sigfe")
	parser.add_argument("--calculoAFE",          			help="calculoAFE")
	parser.add_argument("--80Bis",          				help="80Bis")
	parser.add_argument("--Presupuesto",          			help="Presupuesto Giulinano")
	parser.add_argument("--plazoDeLaDeuda",          		help="plazoDeLaDeuda")
	parser.add_argument("--DisponibilidadPresupuestaria",	help="DisponibilidadPresupuestaria")
	parser.add_argument("--analisisRetenidosDataBase",		help="analisisRetenidosDataBase")
	parser.add_argument("--analisisRetenidos",				help="analisisRetenidos")
	parser.add_argument("--analisisRetenidosReport",		help="analisisRetenidosReport")
	parser.add_argument("--apruebaConvenioDataBase",		help="apruebaConvenioDataBase")
	parser.add_argument("--apruebaConvenio",				help="apruebaConvenio")
	parser.add_argument("--centralizacion",					help="centralizacion")
	parser.add_argument("--operation",      				help="operation", choices=["centralizacion", "apruebaConvenioDataBase", "apruebaConvenio", "analisisRetenidosDataBase", "analisisRetenidos", "analisisRetenidosReport", "80Bis", "HectorTest", "retencionesLevantamientos", "Presupuesto", "retener", "plazoDeLaDeuda", "calculoAFE", "db", "DisponibilidadPresupuestaria" , "urgencia" , "Hector", "Sandra", "sigfe", "calculoPrevioPago" ,"Alvaro", "Alicia", "Miguel"])
	args = parser.parse_args()

	if args.operation == 'db':
		Database(json_path)
		#SisValidacion(json_path)

	if args.operation == 'sigfe':
		#ReadEstadoEjecucionPresupuestaria(json_path)
		ReadDisponibilidadRequerimientosPresupuestarios(json_path)
		ReadDisponibilidadCompromisoPresupuestarios(json_path)
		ReadDisponibilidadDevengoPresupuestarios(json_path)
		#ReadCompromiso(json_path)
		#ReadDevengo(json_path)
		#Informes()
		#InformeRequerimiento()

	elif args.operation == 'calculoPrevioPago':
		Reporte_FES(json_path)
		Malla(json_path)
		Calculos()

	elif args.operation == 'HectorTest':	# URGENCIA
		try:
			SisValidacionTest1(json_path)
		except Exception as e:
			SisValidacionTest1(json_path)
		else:
			SisValidacionTest1(json_path)
		finally:
			SisValidacionTest1(json_path)


	elif args.operation == 'Hector':
		#SisValidacion(json_path)

		try:
			SisValidacion(json_path)
		except:
			SisValidacion(json_path)
		else:
			SisValidacion(json_path)
		finally:
			SisValidacion(json_path)

	elif args.operation == 'Sandra':
		SisValidacion_Sandra(json_path)

	elif args.operation == 'urgencia':
		SisValidacion_urgencias(json_path)

	elif args.operation == '80Bis': # en caso de que falle webdriver https://googlechromelabs.github.io/chrome-for-testing/#stable
		#SisValidacion80Bis(json_path)
		while True:
			try:
				if args.operation == '80Bis':
					SisValidacion80Bis(json_path)
			except Exception as e:
				print("Ocurrió un error:", str(e))
				continue

	elif args.operation == 'DisponibilidadPresupuestaria':
		#ScrapingSigfeReportsDisponibilidad(json_path)
		ScrapingSigfeReports(json_path)

	elif args.operation == 'Presupuesto': # Giulinano
		ScrapingSigfeReportsPresupuesto(json_path)

	elif args.operation == 'calculoAFE':
		
		# Descargas(json_path)
		ReadExcel(json_path)
		#Parse()
		#ParseLevantar()

		i = 0
		while i < 2:
			print(i)
			Parse()
			ParseLevantar()
			i += 1


		"""
		i = 0
		while i < 2:
			print(i)
			ConsolidadoRendicionDeCuentas(json_path)
			Fes(json_path)
			HayQueRetener(json_path)
			Aprobados(json_path)
			UnionTablas()
			i += 1
		"""

		#HayQueRetener(json_path)
		#HayQueLevantar(json_path)


		# importante 		ConsolidadoRendicionDeCuentas(json_path)
		# importante 		Fes(json_path)
		# importante 		Retenidos(json_path)
		# importante 		Aprobados(json_path)
		#UnionTablas()
		# importante Merge()
		# importante 		Merge_Fes_ConsolidadoRC()
		#Merge_Retenidos_ConsolidadoRC()

		#Pago(json_path)
		#CalculoPago()

	elif args.operation == 'plazoDeLaDeuda':
		PlazoDeLaDeuda()

	elif args.operation == 'retener':
		SisHayQueRetener(json_path)

	elif args.operation == 'retencionesLevantamientos':
		#SisDescargasPagosAprobados(json_path)
		#SisDescargasPagosRetenidos(json_path)
		SisDescargasTransferencias(json_path)

	elif args.operation == 'apruebaConvenioDataBase':
		ApruebaConvenioDataBase(json_path)

	elif args.operation == 'apruebaConvenio':
		ApruebaConvenio(json_path)

	elif args.operation == 'analisisRetenidosDataBase':
		AnalisisRetenidosDataBase(json_path)

	elif args.operation == 'analisisRetenidos':
		AnalisisRetenidos(json_path)

		i = 1
		while i < 31:
			try:
				AnalisisRetenidos(json_path)
			except:
				AnalisisRetenidos(json_path)
			else:
				AnalisisRetenidos(json_path)
			finally:
				AnalisisRetenidos(json_path)
			i += 1

	elif args.operation == 'analisisRetenidosReport':
		AnalisisRetenidosReport(json_path)

	elif args.operation == 'centralizacion':
		Centralizacion(json_path)