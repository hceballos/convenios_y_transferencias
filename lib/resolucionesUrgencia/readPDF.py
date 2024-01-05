from PyPDF2 import PdfReader
import glob
import re

class Main(object):

	def getFolio(self, data):
		folio = re.findall(r'\d{15}[AMU]\d{5}', data)
		return folio[0]

	def getFechas(self, data):
		Fechas = re.findall(r'\b\d{2}\/\d{2}\/\d{4}\b', data)
		if len(Fechas) >= 2:
			return Fechas[0], Fechas[1]
		else:
			print("No se encontraron suficientes fechas.")

	def getPlazas_convenidas(self, data):
		regex_pattern = r'\b\d+\b'
		matches = re.findall(regex_pattern, data)
		position_to_find = 13
		if len(matches) > position_to_find:
			number_at_position_14 = matches[position_to_find]
			return number_at_position_14
		else:
			print("No hay suficientes números en el texto.")

	def getPlazas_atendidas(self, data):
		regex_pattern = r'(\d+)Fecha'
		matches = re.findall(regex_pattern, data)
		if matches:
			numero_antes_fecha = matches[0]
			return numero_antes_fecha
		else:
			print("No se encontró un número antes de 'Fecha'.")

	def __init__(self):
		self.process_pdfs()

	def process_pdfs(self):
		for f in glob.glob('C:/Users/hceballos/Music/desarrollo/convenios_y_transferencias/input_excel/resolucionesUrgencia/pdfs/*.pdf', recursive=True):
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

	def extract_data(self, data):
		# print(data)



		folio = self.getFolio(data)
		print("Folio encontrado x :", folio)

		fechas = self.getFechas(data)
		print("Fechas encontradas:", fechas[0], fechas[1])

		plazas_convenidas = self.getPlazas_convenidas(data)
		print("Plazas Convenidas:", plazas_convenidas)

		plazas_atendidas = self.getPlazas_atendidas(data)
		print("Plazas Atendidas:", plazas_atendidas)



if __name__ == '__main__':
	Main()