consulta = " \
	SELECT \
		r.'Unidad Ejecutora', \
		r.'cuenta', \
		r.'tipo_de_pago', \
		r.'Folio' as 'r.Folio', \
		(SELECT SUM(r2.'Monto Vigente') FROM disponibilidadRequerimientos r2 WHERE r2.'cuenta' = r.'cuenta' AND r2.'CodRegion' = '2111001') as 'DisponibleNacional', \
		r.'Monto Vigente' as 'r.MontoVigente', \
		r.'Monto Disponible' as 'r.MontoDisponible', \
		r.'Monto Consumido' as 'r.MontoConsumido', \
		c.'rut' as 'c.rut', \
		c.'Folio' as 'c.Folio', \
		c.'Monto Vigente' as 'c.MontoVigente', \
		c.'Monto Disponible' as 'c.MontoDisponible', \
		c.'Monto Consumido' as 'c.MontoConsumido' \
	FROM \
		(SELECT disponibilidadCompromiso.* FROM disponibilidadCompromiso) c \
		LEFT JOIN(SELECT disponibilidadRequerimientos.* FROM disponibilidadRequerimientos) r \
			ON c.'unico' = r.'unico' \
			AND c.'CodRegion' = r.'CodRegion' \
			AND c.'cuenta' = r.'cuenta' \
			AND c.'tipo_de_pago' = r.'tipo_de_pago' \
	WHERE \
		c.'CodRegion' = '"+row['CodRegion']+"' \
		AND c.'cuenta' LIKE '2401%' \
		AND c.'CodRegion' = r.'CodRegion' \
		AND c.'cuenta' = r.'cuenta' \
		AND c.'tipo_de_pago' = r.'tipo_de_pago' \
"
df2 = pd.read_sql_query(consulta, cnx)


df1agrupado = df.groupby(['Unidad Ejecutora', 'cuenta', 'tipo_de_pago', 'r.Folio']).sum().reset_index()


df2_pivot_table = pd.pivot_table(df2,
					index = ["Unidad Ejecutora", "cuenta", "DisponibleNacional", "tipo_de_pago", "r.Folio", "r.MontoVigente", "r.MontoDisponible", "r.MontoConsumido", "c.rut", "c.Folio", "c.MontoVigente", "c.MontoDisponible", "c.MontoConsumido"],
					#values = ["monto"],
					#columns = ["proyecto"],
					aggfunc = [np.sum],
					fill_value = 0,
					margins = True
					)