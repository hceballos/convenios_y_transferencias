from PyPDF2 import PdfReader
import glob
import re
import os
import pandas as pd
from lib.resolucionesUrgencia.database.database import Database


class ReadPDF(object):

	def getFolio(self, data):
		folio = re.findall(r'\d{15}[AMU]\d{5}', data)
		return folio[0]

	def getFechaInicio(self, data):
		Fechas = re.findall(r'\b\d{2}\/\d{2}\/\d{4}\b', data)
		if len(Fechas) >= 2:
			return Fechas[0]
		else:
			print("No se encontraron suficientes fechas.")

	def getFechaTermino(self, data):
		Fechas = re.findall(r'\b\d{2}\/\d{2}\/\d{4}\b', data)
		if len(Fechas) >= 2:
			return Fechas[1]
		else:
			print("No se encontraron suficientes fechas.")

	def getPlazas_convenidas(self, data):
		regex_pattern = r'\b\d+\b'
		matches = re.findall(regex_pattern, data)
		position_to_find = 13
		if len(matches) > position_to_find:
			#number_at_position_14 = matches[position_to_find]
			number_at_position_14 = int(matches[position_to_find])


			return number_at_position_14
		else:
			print("No hay suficientes números en el texto.")

	def getPlazas_atendidas(self, data):
		regex_pattern = r'(\d+)Fecha'
		matches = re.findall(regex_pattern, data)
		if matches:
			numero_antes_fecha = int(matches[0])
			return numero_antes_fecha
		else:
			print("No se encontró un número antes de 'Fecha'.")


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



	def vaciaCarpeta(self):
		carpeta = '/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/resolucionesUrgencia/pdfs'

		# Verificar si la carpeta existe
		if os.path.exists(carpeta):
		    # Buscar archivos que terminen en ".pdf" y eliminarlos
		    archivos_pdf = glob.glob(os.path.join(carpeta, '*.pdf'))
		    
		    for archivo_pdf in archivos_pdf:
		        try:
		            os.remove(archivo_pdf)
		            print(f"Archivo eliminado: {archivo_pdf}")
		        except Exception as e:
		            print(f"No se pudo eliminar {archivo_pdf}: {e}")
		else:
		    print(f"La carpeta {carpeta} no existe.")

		return


	def __init__(self):
		self.process_pdfs()
		#self.vaciaCarpeta()

	def process_pdfs(self):

		self.data_list = []

		for f in glob.glob('/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/resolucionesUrgencia/pdfs/*.pdf', recursive=True):
			print('Procesando: ', f)
			with open(f, 'rb') as archivo_pdf:
				lector_pdf = PdfReader(archivo_pdf)
				data = ""

				for pagina_num in range(len(lector_pdf.pages)):
					pagina = lector_pdf.pages[pagina_num]
					texto = pagina.extract_text()
					data += texto + "\n"
				print()
				self.extract_data(data)
		pdf = pd.DataFrame(self.data_list, columns=["folio", "proyecto", "mesAtencion", "fechaInicio", "fechaTermino", "plazas_convenidas", "plazas_atendidas"])
		print(pdf)
		database = Database()
		database.crear_PDF(pdf)


	def extract_data(self, data):

		folio = self.getFolio(data)
		print("Folio encontrado x :", folio)






		proyecto = self.getProyecto(folio)
		print("Proyecto 		: ", proyecto)

		mesAtencion = self.getMesAtencion(folio)
		print("MesAtencion 		: ", mesAtencion)










		fechaInicio = self.getFechaInicio(data)
		print("Fechas encontradas:", fechaInicio)

		fechaTermino = self.getFechaTermino(data)
		print("Fechas encontradas:", fechaTermino)

		plazas_convenidas = self.getPlazas_convenidas(data)
		print("Plazas Convenidas:", plazas_convenidas)

		plazas_atendidas = self.getPlazas_atendidas(data)
		print("Plazas Atendidas:", plazas_atendidas)

		self.data_list.append([folio, proyecto, mesAtencion, fechaInicio, fechaTermino, plazas_convenidas, plazas_atendidas])


