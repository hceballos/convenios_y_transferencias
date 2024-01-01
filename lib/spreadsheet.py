# -*- coding: utf-8 -*-
import pandas as pd
import glob
import sqlite3
from sqlalchemy import create_engine
from lib.consulta import Consulta
from os import path
from os import remove
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, MetaData, Table

class Spreadsheet():

    def __init__(self, datos):
        self.datos = datos

        self.read_Excel(datos)

    def read_Excel(self, datos):
        devengo = pd.DataFrame()
        for f in glob.glob(datos['excel_path']):
            df = pd.read_excel(f, converters={ 'Número Documento': str } )
            print('Procesando  : ', f)
            devengo = devengo.append(df,ignore_index=True)

        devengo['Tipo Vista']          = devengo.drop( devengo[ devengo['Tipo Vista'] == 'Saldo Inicial' ].index , inplace=True )
        devengo['Monto Documento.1']   = [w.replace('(', '-') for w in devengo['Monto Documento.1']]
        devengo['Monto Documento.1']   = [w.replace(')', '' ) for w in devengo['Monto Documento.1']]
        devengo['Monto Documento.1']   = [w.replace('.', '' ) for w in devengo['Monto Documento.1']]
        devengo['Monto Documento.1']   = pd.to_numeric(devengo['Monto Documento.1'])
        devengo['Monto Documento']     = [w.replace('.', '' ) for w in devengo['Monto Documento']]
        devengo['Monto Documento']     = pd.to_numeric(devengo['Monto Documento'])
        devengo['N Concepto']          = devengo['Concepto'].str.split(' ', n = 1, expand = True)[0]
        devengo['Concepto Nombre']     = devengo['Concepto'].str.split(' ', n = 1, expand = True)[1]
        devengo['Rut']                 = devengo['Principal'].str.split(' ', n = 1, expand = True)[0]
        devengo['Rut Nombre']          = devengo['Principal'].str.split(' ', n = 1, expand = True)[1]
        #devengo['Folio']               = devengo['Folio'].astype(str)
        devengo['Fecha Generación']    = pd.to_datetime(devengo['Fecha Generación']).dt.date
        devengo['ID']                  = devengo['Rut'] + devengo['Número Documento']
        devengo['Orden de Compra']     = devengo['Tipo Vista']
        del devengo['Tipo Vista']
        
        self.base_de_datos(datos, devengo)

    def base_de_datos(self, datos, devengo):
        if path.exists("save_pandas.db"):
            remove('save_pandas.db')
        
        engine = create_engine('sqlite:///save_pandas.db', echo = False)
        devengo.to_sql('devengo', con=engine)
        
        
        consulta = Consulta()
        consulta.documento()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        