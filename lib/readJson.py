import json
import pandas as pd


class ReadJson(object):
	def __init__(self, json_path):
		self.json_path = json_path

		self.read_json(json_path)

	def read_json(self, json_path):
		with open(json_path) as secciones_json:
			self.datos = json.load(secciones_json)
			
