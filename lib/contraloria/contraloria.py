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


class Contraloria(Fuente):

	def descargar_archivo(self,url):
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		else:
			print(f"No se pudo descargar el archivo. Código de estado: {response.status_code}")
			return None

	def actualizar_archivo_local(self, archivo_contenido, ruta_local):
		with open(ruta_local, 'w') as archivo_local:
			archivo_local.write(archivo_contenido)
		print(f"Archivo actualizado localmente: {ruta_local}")

	def opcion1(self, datos, url_archivo_github, ruta_local_archivo):
		print("Has seleccionado la opción 1.")
		contenido_archivo = self.descargar_archivo(url_archivo_github)
		if contenido_archivo:
			self.actualizar_archivo_local(contenido_archivo, ruta_local_archivo)
		ReadExcel(datos)

	def opcion2(self, datos):
		print("Has seleccionado la opción 2.")
		Scrapy(datos)

	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
		datos = self.datos

		url_archivo_github = "https://raw.githubusercontent.com/hceballos/convenios_y_transferencias/master/lib/elementos.py"
		ruta_local_archivo = "/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/lib/contraloria/elementos.py"

		while True:
			print("\nMenú:")
			print("1. Opción 1 : Genera la base de datos")
			print("2. Opción 2 : Inicia el proceso")
			print("3. Salir")

			seleccion = input("Selecciona una opción (1/2/3): ")

			if seleccion == "1":
				self.opcion1(datos, url_archivo_github, ruta_local_archivo)
			elif seleccion == "2":
				self.opcion2(datos)
			elif seleccion == "3":
				print("Saliendo del programa. ¡Hasta luego!")
				break
			else:
				print("Opción no válida. Por favor, elige una opción válida.")