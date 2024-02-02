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
from lib.nombrerutyfirma.database.database import Database
import subprocess
import os


class NombreRut(Fuente):

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

	def opcion1(self, datos):
		print("Has seleccionado la opción 1.")
		contenido_archivo = self.descargar_archivo(url_archivo_github)
		if contenido_archivo:
			pass
			#self.actualizar_archivo_local(contenido_archivo, ruta_local_archivo)	# Descarga archivo o carpeta desde github
		ReadExcel(datos)

	def opcion2(self, datos):
		print("Has seleccionado la opción 2.")
		Scrapy(datos)

	def opcion3(self):
		print("Has seleccionado la opción 3.")
		Informes()



	def __init__(self, json_path):

		while True:
			print("\nMenú:")
			print("1. Opción 1 : Genera la base de datos")
			print("2. Opción 2 : Inicia el proceso")
			print("3. Opción 3 : Genera Informe")
			print("4. Salir")

			seleccion = input("Selecciona una opción (1/2/3/4): ")

			if seleccion == "1":
				Database(json_path)

			elif seleccion == "2":
				def ejecutar_scrapy():
					# Ruta completa al directorio del proyecto Scrapy
					ruta_proyecto_scrapy = "C:/Users/hceballos/Music/desarrollo/convenios_y_transferencias/lib/nombrerutyfirma"

					# Cambiar al directorio del proyecto Scrapy
					os.chdir(ruta_proyecto_scrapy)

					# Definir el comando a ejecutar
					comando = "scrapy crawl quotes -o ../../output/nombrerutyfirma.json"

					try:
						# Ejecutar el comando usando subprocess
						subprocess.run(comando, shell=True, check=True)
						print("Comando ejecutado con éxito.")
					except subprocess.CalledProcessError as e:
						print(f"Error al ejecutar el comando: {e}")

				# Llamar a la función para ejecutar el comando
				ejecutar_scrapy()












			elif seleccion == "3":
				self.opcion3()				
			elif seleccion == "4":
				print("Saliendo del programa. ¡Hasta luego!")
				break
			else:
				print("Opción no válida. Por favor, elige una opción válida.")