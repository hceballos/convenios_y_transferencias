import pulp

saldo = 148645

# Crear el problema de optimización
problema = pulp.LpProblem('Problema de cambio', pulp.LpMinimize)

# Definir las variables
monedas = [145945, 2700, 12050, 34176, 80884, 73120]
variables = []
for i in range(len(monedas)):
    var = pulp.LpVariable('x{}'.format(i), lowBound=0, cat='Integer')
    variables.append(var)

# Definir la función objetivo
problema += pulp.lpSum(variables)

# Definir las restricciones
problema += pulp.lpDot(variables, monedas) == saldo

# Resolver el problema
problema.solve()

# Imprimir la solución
for i in range(len(monedas)):
    print('{}: {}'.format(monedas[i], variables[i].value()))