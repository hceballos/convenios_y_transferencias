if ( (ANTICIPO[row.name]) & ~(emg[row.name]) & (antes[row.name]) & (ahora[row.name]) ):
	pagar_messages.append("PAGAR : ANTICIPO - No es EMERGENCIA - NO Presenta mes antes - NO Presenta mes ahora")


if ( ~(ANTICIPO[row.name]) & (emg[row.name]) & (antes[row.name]) & (ahora[row.name]) ):
	pagar_messages.append("PAGAR : NO ES ANTICIPO - SI es EMERGENCIA - NO Presenta mes antes - NO Presenta mes ahora")


if ( ~(ANTICIPO[row.name]) & ~(emg[row.name]) & (dias_transcurridos[row.name]) & (antes[row.name]) & (ahora[row.name]) ):
	pagar_messages.append("PAGAR : Proyecto Crecien creado - NO Presenta mes antes - NO Presenta mes ahora - No es EMERGENCIA - No es ANTICIPO")


if ( ~(ANTICIPO[row.name]) & ~(emg[row.name]) & ~(dias_transcurridos[row.name]) & (antes[row.name]) & (ahora[row.name]) ):
	retener_messages.append("RETENER :  NO es ANTICIPO - NO es EMERGENCIA - Proyecto Viejo - NO Presenta mes antes - NO Presenta mes ahora")


if ( ~(ANTICIPO[row.name]) & ~(emg[row.name]) & ~(dias_transcurridos[row.name]) & ~(antes[row.name]) & (ahora[row.name]) ):
	retener_messages.append("RETENER :  NO es ANTICIPO - NO es EMERGENCIA - Proyecto Viejo - SI Presenta mes antes - NO Presenta mes ahora")


if ( ~(ANTICIPO[row.name]) & ~(emg[row.name]) & ~(dias_transcurridos[row.name]) & ~(antes[row.name]) & ~(ahora[row.name]) ):
	pagar_messages.append("PAGAR :  NO es ANTICIPO - NO es EMERGENCIA - Proyecto Viejo - SI Presenta mes antes - SI Presenta mes ahora")


if ( (ANTICIPO[row.name]) & (emg[row.name]) & (dias_transcurridos[row.name]) & (antes[row.name]) & (ahora[row.name]) ):
	retener_messages.append("RETENER :  NO es ANTICIPO - NO es EMERGENCIA - Proyecto Viejo - NO Presenta mes antes - NO Presenta mes ahora")


if ( (ANTICIPO[row.name]) & (emg[row.name]) & (dias_transcurridos[row.name]) & (antes[row.name]) & (ahora[row.name]) ):
	retener_messages.append("RETENER : SI Presenta mes antes - NO Presenta mes ahora - Proyecto Viejo - No es EMERGENCIA - No es ANTICIPO")







RETENER :  NO es ANTICIPO - NO es EMERGENCIA - Proyecto Viejo - NO Presenta mes antes - NO Presenta mes ahora, 
RETENER :  NO es ANTICIPO - NO es EMERGENCIA - Proyecto Viejo - NO Presenta mes antes - NO Presenta mes ahora	


"RETENER: No se trata de un ANTICIPO, ni de una EMERGENCIA. Se refiere a un Proyecto vigente hace mas de 70 dias, sin presentación de Rendicion de cuentas el mes anterior, pero con presentación este mes."






