import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import xlrd

# Ruta al archivo Excel
archivo_entrada = '/Users/hector/Downloads/Reporte_FES_04-02-2024.xls'
archivo_salida = 'bbb.xlsx'

# Utilizar pandas para leer el archivo .xls y luego guardarlo como .xlsx
df = pd.read_csv(archivo_entrada, delimiter='\t', encoding='utf-16')

# Eliminar la última fila
df = df.drop(df.index[-1])

# Reemplazar el nombre de las columnas
nombres_columnas = ['ARCHIVO', 'Tipo Resolución', 'Folio', 'codregion', 'codproyecto',
                    'mesano', 'Correlativo', 'Proyecto_Nombre', 'codinstitucion', 'Institucion',
                    'ModeloIntervencion', 'PlzAtendidas', 'DiasAtencion', 'FechaEnviorepositorio',
                    'HistoricoPagos', 'HistoricoPlz', 'HistoricoFolio', 'Diferencia_Plazas',
                    'OrdenRegion', 'Fechaactualizacion', 'Plazas_80Bis_APago', 'Plazas_Convenidas']

df.columns = nombres_columnas


# Función para eliminar etiquetas HTML específicas de una cadena
def eliminar_etiquetas_html(texto_html):
    texto_limpio = texto_html.replace('<tr>', '').replace('</tr>', '').replace('<td>', '').replace('</td>', '').replace('</Td><Td>', '').replace('</TR><Td>', '').replace('</Td>', '').replace('<TR><Td>', '')
    return texto_limpio

# Aplicar la función a todas las celdas del DataFrame
df = df.applymap(lambda x: eliminar_etiquetas_html(str(x)) if isinstance(x, str) else x)


df['PlzAtendidas']          = df['PlzAtendidas'].astype(int)
df['DiasAtencion']          = df['DiasAtencion'].astype(int)
df['Diferencia_Plazas']     = df['Diferencia_Plazas'].astype(int)
df['OrdenRegion']           = df['OrdenRegion'].astype(int)
df['Plazas_80Bis_APago']    = df['Plazas_80Bis_APago'].astype(int)
df['Plazas_Convenidas']     = df['Plazas_Convenidas'].astype(int)


# Guardar el DataFrame en un nuevo archivo Excel
df.to_excel(archivo_salida, index=False, engine='openpyxl')


print(df)

