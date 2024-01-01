SELECT
	DisponibilidadCompromiso.['Unidad Ejecutora'],
	DisponibilidadCompromiso.['folio'],
	DisponibilidadCompromiso.['Número Identificación'],
	DisponibilidadCompromiso.['principal'], 
	DisponibilidadCompromiso.['Concepto Presupuesto'],
	DisponibilidadCompromiso.['Monto Vigente'],
	DisponibilidadCompromiso.['CodRegion'],
	DisponibilidadCompromiso.['unico']
FROM
	DisponibilidadCompromiso
WHERE
	DisponibilidadCompromiso.'Concepto Presupuesto' like '2401%'
	and DisponibilidadCompromiso.'Catálogo 04'  != 'MetasAdicionales - 01 META 80 BIS'
GROUP BY
	DisponibilidadCompromiso.'Concepto Presupuesto'
HAVING
	Sum(DisponibilidadCompromiso.'Monto Vigente')