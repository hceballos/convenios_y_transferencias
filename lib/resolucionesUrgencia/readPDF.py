from PyPDF2 import PdfReader
import glob

class Main(object):
    def __init__(self):
        self.data = ""  # Inicializa la variable 'data'

        for f in glob.glob('./input_excel/resolucionesUrgencia/*.pdf', recursive=True):
            print('Procesando  : ', f)
            with open(f, 'rb') as archivo_pdf:  # Abre el archivo en modo lectura binaria ('rb')
                lector_pdf = PdfReader(archivo_pdf)
                
                numero_paginas = len(lector_pdf.pages)  # Obtiene el número total de páginas del PDF
                
                # Lee el contenido de cada página del PDF
                for pagina_num in range(numero_paginas):
                    pagina = lector_pdf.pages[pagina_num]
                    texto = pagina.extract_text()
                    
                    # Agrega el contenido de la página a la variable 'data'
                    self.data += texto + "\n"  # Agrega un salto de línea entre páginas

        # Puedes imprimir 'data' para verificar o hacer lo que necesites con ella
        # print(self.data)


if __name__ == '__main__':
    Main()
