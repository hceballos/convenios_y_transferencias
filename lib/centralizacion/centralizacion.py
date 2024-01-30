#! /bin/env python3
from datetime import date
from lib.fuente import Fuente
import os
import pandas as pd
import sys
import time
import glob
import xlrd
import shutil
import csv
import sqlalchemy
from datetime import datetime
import sqlite3
import xlsxwriter
import sqlalchemy
from lib.centralizacion.readExcel.readMalla import ReadMalla
from lib.centralizacion.readExcel.readTodosLosPagos import ReadTodosLosPagos
from lib.centralizacion.readExcel.readTransferencias import ReadTransferencias
from lib.centralizacion.readExcel.readRetenidos import ReadRetenidos
from lib.centralizacion.readExcel.readReporteDeuda import ReadReporteDeuda
from lib.centralizacion.readExcel.readRendicionDeCuentas import ReadRendicionDeCuentas
from lib.centralizacion.readExcel.readtodasLasFES import ReadtodasLasFES
from lib.centralizacion.informes import Informes
from lib.centralizacion.readExcel.scrapingSigfeReports import ScrapingSigfeReports


from lib.centralizacion.readExcel.test_Deuda import main


class Centralizacion(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		# ReadMalla(datos)
		# ReadRetenidos(datos)
		# ReadRendicionDeCuentas(datos)
		ReadTodosLosPagos(datos)
		ReadTransferencias(datos)
		ReadReporteDeuda(datos)
		# ReadtodasLasFES(datos)
		# ScrapingSigfeReports(datos)

		# main()

		Informes()