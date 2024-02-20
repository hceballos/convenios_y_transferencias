#! /bin/env python3
import os
import sys
import codecs
from lib.elementos import Envio_Informacion
from lib.elementos import Click
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from lib.fuente import Fuente
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sqlite3
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import platform


class Informe(object):

	def __init__(self, datos):

		cnx = sqlite3.connect('proyectos.db')
		consulta  = " \
			SELECT \
				CodProyectos.'Mes Atención', \
				CodProyectos.'Región', \
				CodProyectos.'Cod. Proyecto', \
				CodProyectos.'Monto Total', \
				CodProyectos.'Nº CDP', \
				CodProyectos.'AÑO CDP', \
				CodProyectos.'Resolución', \
				CodProyectos.'Fecha', \
				CodProyectos.'OBSERVACION', \
				CodProyectos.'Tipo', \
				CodProyectos.'CodProyecto', \
				CodProyectos.'MesAtencion', \
				CodProyectos.'Estatus', \
				CodProyectos.'Plazas Atendidas' \
			FROM \
				CodProyectos \
			WHERE \
				CodProyectos.'Tipo' = '80 BIS' \
				and CodProyectos.'Estatus' != 'OK' \
			ORDER BY \
				CodProyectos.'Región' DESC, \
				CodProyectos.'Cod. Proyecto' ASC \
		"
		query = pd.read_sql_query(consulta, cnx)
		# =================================================================================== *************************** COMENTAR PARA GENERAR EL INFORME **********************************
		consulta  = " \
			SELECT CodProyectos.* FROM CodProyectos \
		"
		query = pd.read_sql_query(consulta, cnx)

		today = date.today()
		writer = pd.ExcelWriter(today.strftime("output/"+"%d-%b-%Y")+' - Resumen Validados 80 Bis.xlsx', engine='xlsxwriter')
		query.style.set_properties(**{'text-align': 'center'}).to_excel(writer, sheet_name='Todas las cuentas', index=False)
		writer.save()
		# ================================================================================================================================

