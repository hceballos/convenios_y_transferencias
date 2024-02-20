#! /bin/env python3
from datetime import date
from lib.elementos import Click
from lib.elementos import Envio_Informacion
from lib.fuente import Fuente
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine, Table, Column, String, MetaData, insert, update, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import re
import sqlite3
import time
import requests
from lib.contraloria.readExcel import ReadExcel
from lib.contraloria.scrapy import Scrapy
from lib.contraloria.informes import Informes
from lib.bis80.database import Database
from lib.bis80.validacion import Validacion
from lib.bis80.informe import Informe


class Bis80(Fuente):

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		url_archivo_github = "https://raw.githubusercontent.com/hceballos/convenios_y_transferencias/master/lib/elementos.py"
		ruta_local_archivo = "/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/lib/contraloria/elementos.py"
		
		while True:
			print("\nMenú:")
			print("1. Opción 1 : Genera la base de Datos")
			print("2. Opción 2 : Inicia el proceso de Validar")
			print("2. Opción 3 : Inicia el proceso de Editar")
			print("4. Opción 4 : Genera Informe")
			print("5. Salir")

			seleccion = input("Selecciona una opción (1/2/3/4/5): ")

			if seleccion == "1":
				Database(datos)
			elif seleccion == "2":
				Validacion(datos)
			elif seleccion == "3":
				self.opcion3()
			elif seleccion == "4":
				Informe(datos)
			elif seleccion == "5":
				print("Saliendo del programa. ¡Hasta luego!")
				break
			else:
				print("Opción no válida. Por favor, elige una opción válida.")