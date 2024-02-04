import pandas as pd
from fuzzywuzzy import fuzz
from unidecode import unidecode

# Crear un DataFrame de ejemplo
data = {'Nombre_Completo': ['María López', 'Juan Pérez', 'Ana García', 'Ceballos Aviles Hector Antonio', 'Ceballos Aviles Hector Antonio'],
        'Nombre_Columna': ['MARIA LOPEZ', 'juan perez', 'ANA GARCIA', 'Hector Antonio Ceballos Aviles', 'Ceballos Aviles Antonio Hector']}

df = pd.DataFrame(data)

# Función para calcular la similitud de nombres considerando el orden de palabras
def calcular_similitud(nombre1, nombre2):
    return fuzz.token_sort_ratio(unidecode(nombre1.lower()), unidecode(nombre2.lower()))

# Aplicar la función de similitud a las columnas del DataFrame
df['Similitud'] = df.apply(lambda row: calcular_similitud(row['Nombre_Completo'], row['Nombre_Columna']), axis=1)

# Definir un umbral para considerar si los nombres son "iguales"
umbral = 80  # Puedes ajustar este valor según tus necesidades

# Crear una nueva columna que indique si los nombres son "iguales"
df['Nombres_Son_Iguales'] = df['Similitud'] >= umbral

# Mostrar el DataFrame resultante
print(df)
