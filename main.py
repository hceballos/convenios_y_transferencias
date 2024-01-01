# PS C:\Users\hector.ceballos\Desktop\HectorCeballos\pandora> scrapy crawl facturas -o facturas.json
# scrapy crawl facturas -o ..\pandora\input\facturas\facturas.json
from lib.readJson  import ReadJson
from lib.readReportePago  import ReadReportePago
from lib.readRetenciones  import ReadRetenciones
from lib.readPagoManual  import ReadPagoManual
#from lib.informe_reportePago import Informe_reportePago
import sqlite3
import pandas as pd
import numpy as np


class main(ReadJson):
	def __init__(self, json_path):
		ReadJson.__init__(self, json_path)
		datos = self.datos

		# ReportePago - listado de pagos que ofrece SIS
		#ReadReportePago(datos)

		# Pago Manual - Pago manual que negera Carolina
		#ReadPagoManual(datos)

		# Retenciones - unifica los documentos de retenciones en 1
		ReadRetenciones(datos)
		#Informe_reportePago()




json_path = r'../mejorninez/data/data.json'


if __name__ == '__main__':
	main(json_path)#