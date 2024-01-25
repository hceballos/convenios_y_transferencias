

en un archivo tengo esto:

ScrapingSigfeReports(datos)

y en otro tengo :

class ScrapingSigfeReports(object):
	def __init__(self, datos):
        self.datos = datos  # Asigna el valor del parámetro datos al atributo self.datos
        print(self.datos)

me arroja este error : AttributeError: 'ScrapingSigfeReports' object has no attribute 'datos'