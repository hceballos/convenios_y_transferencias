#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sqlite3
from xlsxwriter.utility import xl_rowcol_to_cell
import pandas as pd


class Consulta():

    def documento(self):
        print("============================================")
        cnx = sqlite3.connect('save_pandas.db')
        
        consulta  = " \
        SELECT \
        	devengo.'Número Documento', \
        	devengo.'Folio', \
        	devengo.'N Concepto' \
        FROM \
        	devengo \
        "
        datos = pd.read_sql_query(consulta, cnx)
        
        """
        for index, row in datos.iterrows(): 
            print( row['Número Documento'], row["Folio"], row['N Concepto'] ) 
        """    
        for index, row in datos.iterrows(): 
            print( row['Número Documento'] )        
            print( row["Folio"] )     
            print( row['N Concepto'] )     
            print("============================================")
                        
                        
        
        #print(datos)
        
        writer = pd.ExcelWriter('Fuentes y uso de fondos.xlsx', engine='xlsxwriter')
        datos.to_excel(writer, sheet_name='Pandas')
        writer.save()
