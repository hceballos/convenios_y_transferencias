condicion = 
		(str(row['Cod. Proyecto']) in Proyecto) and 
		(str(row['MesAtencion']) == MesdeAtencion) and 
		(str(row['Plazas Atendidas']) == Convenidas)
		(str(row['Plazas Atendidas']) == Convenidas) and
		(abs(MontoaPago - row['Monto Total']) < 100)


if condicion:
	resultado = "si"
else:
	resultado = "no"

print("****************************** condicion: ", condicion)

if str(row['Cod. Proyecto']) in Proyecto:
	print(">>>>>>>>>>> : if str(row['Cod. Proyecto']) in Proyecto:")
	if str(row['MesAtencion']) ==  MesdeAtencion:
		print(">>>>>>>>>>> : if str(row['MesAtencion']) ==  MesdeAtencion:")
		print("ANTES : if num_rows ==  1:", num_rows)
		if num_rows < 2:
			print("DESPUES : if num_rows ==  1:", num_rows)
			if row['Plazas Atendidas'] == Convenidas:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>> : ", MontoaPago - row['Monto Total'])
				if abs(MontoaPago - row['Monto Total']) < 100: