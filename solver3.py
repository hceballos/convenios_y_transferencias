import pandas as pd
import numpy as np
from scipy.optimize import linprog
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Leer el archivo Excel y crear un dataframe de Pandas
df = pd.read_excel('archivo_excel.xlsx')

# Definir las variables de decisión
variables = list(df['Monto'])

# Definir los objetivos
objetivos = [100, 200, 300]

# Definir la función de restricción
def restriccion(variables, objetivos):
    """
    Función que define la restricción para encontrar los montos que componen los objetivos.
    """
    # Definir los coeficientes de las variables
    coeficientes = np.array(variables)

    # Definir la matriz de coeficientes
    matriz_coeficientes = np.ones((len(objetivos), len(variables)))

    # Definir los límites inferior y superior
    limites_inferiores = np.zeros(len(objetivos))
    limites_superiores = objetivos

    # Resolver el problema de optimización lineal
    resultado = linprog(coeficientes, A_ub=matriz_coeficientes, b_ub=limites_superiores, bounds=(0, None))

    # Devolver la suma de las variables que componen la solución
    return sum(resultado.x)

# Crear el modelo
modelo = ConcreteModel()

# Definir las variables de decisión
modelo.x = Var(range(len(variables)), domain=NonNegativeReals)

# Definir la función objetivo
modelo.objetivo = Objective(expr=sum(modelo.x), sense=maximize)

# Definir la restricción
modelo.restriccion = Constraint(expr=restriccion(modelo.x, objetivos) == 1)

# Resolver el modelo usando el solver GLPK
solver = SolverFactory('glpk')
resultado = solver.solve(modelo)

# Agregar la columna de análisis al dataframe
analisis = []
for i, row in df.iterrows():
    for j, o in enumerate(objetivos):
        if row['Monto'] in [v() for v in modelo.x.values()]:
            if sum([v() for v in modelo.x.values() if v.index() == i]) == o:
                analisis.append(f'Objetivo {j + 1}')
                break
        else:
            analisis.append('N/A')

df['Análisis'] = analisis

# Guardar el dataframe en un archivo Excel
df.to_excel('archivo_excel_con_analisis.xlsx', index=False)

# Imprimir los resultados
print('Variables:')
for i, v in enumerate(modelo.x.values()):
    print(f'Variable {i + 1}: {v()}')

print('Objetivos:')
for i, o in enumerate(objetivos):
    print(f'Objetivo {i + 1}: {o}')