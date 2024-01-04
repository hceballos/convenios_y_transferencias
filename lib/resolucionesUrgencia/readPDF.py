from PyPDF2 import PdfReader
import glob
import re

class Main(object):
	def __init__(self):
		self.process_pdfs()

	def process_pdfs(self):
		for f in glob.glob('/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/input_excel/resolucionesUrgencia/*.pdf', recursive=True):
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
		Folio = re.findall(r'\d{15}[AM]\d{5}', data)
		print("Folio encontrado:", Folio[0])

		Fechas = re.findall(r'\b\d{2}\/\d{2}\/\d{4}\b', data)
		if len(Fechas) >= 2:
			print("Fechas encontradas:", Fechas[0], Fechas[1])
		else:
			print("No se encontraron suficientes fechas.")

		regex_pattern = r'\b\d+\b'
		matches = re.findall(regex_pattern, data)

		position_to_find = 13
		if len(matches) > position_to_find:
			number_at_position_14 = matches[position_to_find]
			print("Plazas Convenidas:", number_at_position_14)
		else:
			print("No hay suficientes números en el texto.")

		regex_pattern = r'(\d+)Fecha'
		matches = re.findall(regex_pattern, data)

		if matches:
			numero_antes_fecha = matches[0]
			print("Plazas Atendidas:", numero_antes_fecha)
		else:
			print("No se encontró un número antes de 'Fecha'.")

if __name__ == '__main__':
	Main()
