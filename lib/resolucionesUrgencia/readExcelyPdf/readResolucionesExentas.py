from PyPDF2 import PdfReader
import pandas as pd
import glob
import re
from lib.resolucionesUrgencia.database.database import Database

class ReadResolucionesExentas(object):

	def getFolio(self, data):
		folio = re.findall(r'\d{15}[AMU]\d{5}', data)
		return folio[0]

	def getProyecto(self, texto):
		patron = r"\d{7}"
		resultado = re.search(patron, texto)
		if resultado:
			numeros = resultado.group(0)
			return numeros
		else:
			return "No se encontraron 7 números consecutivos en la cadena."

	def getMesAtencion(self, texto):
		patron = r"\d{7}(\d{6})"
		resultado = re.search(patron, texto)
		if resultado:
			numeros_entre = resultado.group(1)
			return numeros_entre
		else:
			return "No se encontró la secuencia específica en la cadena."


	def getMes(self, texto):
		patron = r"\d{11}(\d{2})"
		resultado = re.search(patron, texto)
		if resultado:
			numeros_entre = resultado.group(1)
			return numeros_entre
		else:
			return "No se encontró la secuencia específica en la cadena."


	def getAnio(self, texto):
		patron = r"\d{7}(\d{4})"
		resultado = re.search(patron, texto)
		if resultado:
			numeros_entre = resultado.group(1)
			return numeros_entre
		else:
			return "No se encontró la secuencia específica en la cadena."


	def getProyectoDenominado(self, texto):
		patron = r'PROYECTO\s+[\n\s]*DENOMINADO\s+[“\'"](.*?)[”\'"]'
		texto = texto.replace('\n', ' ')
		coincidencias = re.search(patron, texto)
		if coincidencias:
			nombre_proyecto = coincidencias.group(1)
			return nombre_proyecto
		else:
			return "No se encontró el nombre del proyecto en el texto."

	def getResolucionExenta(self, texto):
		patron = r'RESOLUCIÓN EXENTA Nº\s*(\d+)'
		coincidencias = re.findall(patron, texto)
		if coincidencias:
			return coincidencias[0]
		else:
			return "No se encontró el número de Resolución Exenta en el texto."

	def getCDP(self, texto):
		patron = r'Certificado\s+de\s+Disponibilidad\s+Presupuestaria(?:\s*..\s*(\d+)|\s*(\d+))'
		coincidencias = re.search(patron, texto)
		if coincidencias:
			numero = next((num for num in coincidencias.groups() if num), None)
			return numero
		else:
			return "No se encontró un número con el formato especificado en el texto."

	def getPlazasAtendidas(self, texto):
		patron = r'(\d+)\s+plazas\s+atendidas'
		coincidencias = re.search(patron, texto)
		if coincidencias:
			numero_plazas = coincidencias.group(1)
			return numero_plazas
		else:
			return "No se encontró el número de plazas atendidas en el texto."


	def __init__(self):
		self.data_list = []

		self.process_pdfs()

	def process_pdfs(self):
		for f in glob.glob('/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/resolucionesUrgencia/resolucionesExentas/*.pdf', recursive=True):
			print('Procesando: ', f)
			with open(f, 'rb') as archivo_pdf:
				lector_pdf = PdfReader(archivo_pdf)
				data = ""

				for pagina_num in range(len(lector_pdf.pages)):
					pagina = lector_pdf.pages[pagina_num]
					texto = pagina.extract_text()
					data += texto + "\n"
				print()
				self.extract_data(data)  # Llamada a la función para procesar los datos y almacenarlos en data_list

		df = pd.DataFrame(self.data_list, columns=["folio", "proyecto", "mesAtencion", "mes", "anio", "proyectoDenominado", "resolucionExenta", "cdp", "plazasAtendidas"])
		
		print(df)
		database = Database()
		database.crear_ResolucionesExentas(df)

	def extract_data(self, data):
		texto = re.sub(r'\n+', ' ', data)
		print(texto)
		print()

		folio = self.getFolio(texto)
		print("Folio 			: ", folio)

		proyecto = self.getProyecto(texto)
		print("Proyecto 		: ", proyecto)

		mesAtencion = self.getMesAtencion(texto)
		print("MesAtencion 		: ", mesAtencion)




		mes = self.getMes(texto)
		print("Mes 			: ", mes)

		anio = self.getAnio(texto)
		print("Anio			: ", anio)




		proyectoDenominado = self.getProyectoDenominado(texto)
		print("Nombre Proyecto 	: ", proyectoDenominado)

		resolucionExenta = self.getResolucionExenta(texto)
		print("Número de Resolución 	: ", resolucionExenta)

		cdp = self.getCDP(texto)
		print("Número de CDP 		: ", cdp)

		plazasAtendidas = self.getPlazasAtendidas(texto)
		print("Plazas Atendidas 	: ", plazasAtendidas)

		self.data_list.append([folio, proyecto, mesAtencion, mes, anio, proyectoDenominado, resolucionExenta, cdp, plazasAtendidas])



