import pulp

#saldo = 148645

saldo = int(input("Ingresa el monto objetivo: "))

#monedas = [145945, 2700, 12050, 34176, 80884, 73120]


monedas = [11910, 107820, 298950, 123620, 297380, 300250, 48290, 214850, 45160, 12610, 0, 103710, 480930, 206710, 64470, 497690, 213520, 139480, 2740, 259190, 66350, 186740, 119320, 110200, 401310, 206710, 64470, 497690, 213520, 139480, 27750, 883460, 249340, 377750, 269180, 170850, 327340, 106290, 626070, 240080, 255670, 133680, 208030, 308310, 158680, 261420, 95820, 255800, 2740, 163080, 247460, 44270, 269570, (2740), 39020, 117180, 197410, 1967490, 556460, 362580, 207570, 137180, 84340, 17110, 101400, 347060, 7450, 189510, 161390, 104030, 451390, 9350, 94080, 134620, 244960, 297590, 357710, 2693490, 484520, 332470, 11300, 153750, 217340, 135280]


problema = pulp.LpProblem('saldo', pulp.LpMinimize)

variables = []
for i in range(len(monedas)):
    var = pulp.LpVariable('x{}'.format(i), lowBound=0, cat='Integer')
    variables.append(var)

problema += pulp.lpSum(variables)

problema += pulp.lpDot(variables, monedas) == saldo

problema.solve()

if problema.status == 1:
    for i in range(len(monedas)):
        if variables[i].value() > 0:
            print('{} moneda(s) de {}.'.format(variables[i].value(), monedas[i]))
else:
    print('No se pudo encontrar una solución óptima.')


print("=======================================================================")
print("1) Infeasible: esto significa que el problema no tiene solución debido a restricciones conflictivas. En este caso, el solver no puede encontrar una solución que cumpla todas las restricciones.")
print("2) Unbounded : esto significa que el problema tiene solución, pero no hay límite superior o inferior para la función objetivo. En este caso, el solver puede seguir aumentando o disminuyendo la función objetivo sin límite, por lo que no se puede encontrar una solución óptima.")
print("3) Undefined : esto significa que el solver no pudo encontrar una solución en un tiempo razonable o se encontró un error interno en el solver.")