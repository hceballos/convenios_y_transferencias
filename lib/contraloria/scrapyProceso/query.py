import sqlalchemy
import pandas as pd
import glob
from lib.fuente import Fuente
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
import re
import platform
import time
import sqlite3
import re
import platform
import pandas as pd
import glob
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from PyPDF2 import PdfReader
from lib.fuente import Fuente
from lib.elementos import Envio_Informacion, Click

class Query(object):

	def get(self):

		cnx = sqlite3.connect('contraloria.db')
		consulta  = " \
		SELECT \
			CodProyectos.MES_ATENCION, \
			CodProyectos.COD_PROYECTO, \
			CodProyectos.unico, \
			CodProyectos.Analisis \
		FROM \
			CodProyectos \
		"
		query = pd.read_sql_query(consulta, cnx)
		return query