import pandas as pd
import sqlite3
import sqlalchemy
import numpy as np
from datetime import datetime
from datetime import date
import xlsxwriter
import glob
import os
from datetime import datetime
from lib.centralizacion.analisis.analisis import Analisis


class main(object):


	def __init__(self):
		now = datetime.now()
		year = now.year
		month = now.month-1
		periodo = f"{year}{month:02d}"
		#mes_atencion = input("ingresa el periodo de atencion que vas a trabajar, se sugiere " + periodo + ', Ingresa el periodo : ')
		#print(mes_atencion)





		mes_atencion = '202311'
		texto = f'este es {mes_atencion} el texto quiero poner la fecha {mes_atencion}, antes de esto'

		print(texto)
