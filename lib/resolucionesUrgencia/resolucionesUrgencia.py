#! /bin/env python3
from datetime import date
from lib.fuente import Fuente
import pandas as pd
from datetime import datetime
from lib.resolucionesUrgencia.readExcelyPdf.readCDP import ReadCDP
from lib.resolucionesUrgencia.readExcelyPdf.readPDF import ReadPDF
from lib.resolucionesUrgencia.readExcelyPdf.readReporte_resoluciones import ReadReporte_resoluciones
from lib.resolucionesUrgencia.readExcelyPdf.readResolucionesExentas import ReadResolucionesExentas
from lib.resolucionesUrgencia.readExcelyPdf.descargaRAM import DescargaRAM
from lib.resolucionesUrgencia.informes import Informes


class ResolucionesUrgencia(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		ReadCDP(datos)
		ReadReporte_resoluciones(datos)
		ReadResolucionesExentas()
		#DescargaRAM(datos)
		ReadPDF()
		Informes()