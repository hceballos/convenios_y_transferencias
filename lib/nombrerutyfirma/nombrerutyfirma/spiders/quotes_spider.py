# scrapy crawl quotes -o ../../output/nombrerutyfirma.json
import scrapy
import sqlite3
import sqlalchemy
import pandas as pd


class QuotesSpider(scrapy.Spider):
	name = "quotes"

	def start_requests(self):

		cnx = sqlite3.connect('C:/Users/hceballos/Music/desarrollo/convenios_y_transferencias/nombreRut.db')
		consulta  = " \
			SELECT \
				nombreRut.* \
			FROM \
				nombreRut \
		"
		query = pd.read_sql_query(consulta, cnx)
		resultados_lista = pd.read_sql_query(consulta, cnx).to_dict(orient='records')

		urls = [item['rut'] for item in resultados_lista]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('/html/body/div[2]/div/table'):
			yield {
				'nombre': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[1]/text()').extract_first(),
				'run': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[2]/text()').extract_first(),
				'direccion': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[4]/text()').extract_first(),
				'ciudad/comuna': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[5]/text()').extract_first(),
			}