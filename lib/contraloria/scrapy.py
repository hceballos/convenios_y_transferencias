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
from sqlalchemy import create_engine, Table, Column, String, MetaData, insert, update, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import re
import sqlite3
import time
import platform
from lib.contraloria.scrapyProceso.setup import Setup
from lib.contraloria.scrapyProceso.query import Query
from lib.contraloria.database.database import Database

class Scrapy():

	def __init__(self, datos):
		self.datos = datos
		database = Query()
		query = database.get()

		driver = Setup(query)

		




		#print(query)




		print("=================")
		time.sleep(10)