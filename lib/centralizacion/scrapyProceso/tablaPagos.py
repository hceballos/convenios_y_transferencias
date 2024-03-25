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
from lib.contraloria.scrapyProceso.get_data import Get_data

class TablaPagos():

	def __init__(self, row, driver):

		print("# =============================== ===================================================")
		print("ENTRANDO EN DETALLE 1")
		time.sleep(3.5)
		tabla = driver.find_element_by_xpath('//*[@id="GV_pago"]/tbody')
		filas = tabla.find_elements_by_tag_name('tr')
		time.sleep(1)

		informacion = []
		for fila in filas:
			columnas = fila.find_elements_by_tag_name('td')
			datos_fila = []
			for columna in columnas:
				datos_fila.append(columna.text)
			informacion.append(datos_fila)
		resultados = [sublista for sublista in informacion if len(sublista) > 0]

		# print("resultados : ", resultados, len(resultados) )
		for i in range(0, len(resultados)):
			print("i : ", i)
			time.sleep(3.5)

			link_xpath = "//*[@id='GV_pago_lblPeriodo_" + str(i) + "']"
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, link_xpath))).click()  # LINK DETALLE
			time.sleep(3.5)

		Get_data(driver, resultados)


