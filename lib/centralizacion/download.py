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
from lib.contraloria.scrapyProceso.tablaPagos import TablaPagos
from lib.centralizacion.descargaExcel.descargaFES import FES
from lib.centralizacion.descargaExcel.descargaTransferencias import Transferencias
from lib.centralizacion.descargaExcel.descargaDeudas import Deudas


class Download():

	def __init__(self):

		sistema_operativo = platform.system()
		if sistema_operativo == 'Darwin':
			print("Estás utilizando un sistema Mac")
			FES()
			Transferencias()
			#Deudas()
		

		elif sistema_operativo == 'Windows':
			print("Estás utilizando un sistema Windows.")
