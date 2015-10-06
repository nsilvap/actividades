# AyudanteNomina v1.0
# Desarrollado por Melqui Camacho Espitia
# Septiembre 05 de 2015
# Valores de porcentajes para liquidacion de nomina tomados de http://www.gerencie.com/liquidacion-de-la-nomina.html.

import sys
def leer_numerico_entero( mensaje_a_mostrar ):
	valor_numerico_entero = 0
	while (True):	
		try:
			valor_numerico_entero = int(raw_input(mensaje_a_mostrar))
			break
		except ValueError:
			print "Lo que acaba de ingresar no se puede convertir a un valor numerico entero, por favor, vuelva a ingresar ...\n"
   
	return valor_numerico_entero

cantidad_argumentos = len(sys.argv)
salario_minimo = 644350
auxilio_transporte = 74000
tope_auxilio_transporte = 2*salario_minimo
tope_fondo_solidaridad_pensional = 4*salario_minimo
porcentaje_fondo_solidaridad_pensional = 0.01
porcentaje_riesgos = 0.0814014
salario_base = 0
tipo_consulta = 1
if (cantidad_argumentos != 3):	
	salario_base = leer_numerico_entero("\nIngrese salario base: ")
	
	while (True):
		tipo_consulta = leer_numerico_entero("\nDado el salario base, ingrese 1 para consultar costo total para la empresa \n o ingrese 2 para consultar el salario neto para el empleado: ")
		
		if(tipo_consulta != 1 and tipo_consulta != 2):
			print "\nTipo de consulta no valido. Solo se permiten los valores 1 y 2. Vuelva a ingresar ...\n"
		else:
			break
else:
	try:
		salario_base = int(sys.argv[1])
	except ValueError:
		print "\nSalario base no valido. Solo se permiten valores numericos. Por favor cambie el valor del argumento ...\n"
		
		# Terminar el programa
		sys.exit()

	tipo_consulta = int(sys.argv[2])
	
	if(tipo_consulta != 1 and tipo_consulta != 2):
		print "\nTipo de consulta no valido. Solo se permiten los valores 1 y 2. Por favor cambie el valor del argumento ...\n"
		
		# Terminar el programa
		sys.exit()

print "\n"
print ""
print "                 AYUDANTE NOMINA v1.0"
print "                ----------------------"
print ""
dar_auxilio_transporte = False
auxilio_transporte_efectivo = 0
if(salario_base <= tope_auxilio_transporte):
	dar_auxilio_transporte = True
	
if(dar_auxilio_transporte):
	auxilio_transporte_efectivo = auxilio_transporte
else:
	auxilio_transporte_efectivo = 0
debitar_fondo_solidaridad = False
if(salario_base >= tope_fondo_solidaridad_pensional):
	debitar_fondo_solidaridad = True
		
if(tipo_consulta == 1):
	aporte_salud_empresa = 0.085*salario_base
	aporte_pension_empresa = 0.12*salario_base
	aporte_arl_empresa = porcentaje_riesgos*salario_base
	total_aporte_seguridad_social = aporte_salud_empresa + aporte_pension_empresa + aporte_arl_empresa
	aporte_parafiscales_sena = 0.02*salario_base
	aporte_parafiscales_icbf = 0.03*salario_base
	aporte_parafiscales_cajas = 0.04*salario_base
	total_aporte_parafiscales = aporte_parafiscales_sena + aporte_parafiscales_icbf + aporte_parafiscales_cajas
	aporte_cesantias = 0.0833*(salario_base + auxilio_transporte_efectivo)
	aporte_intereses_cesantias = 0.01*aporte_cesantias
	aporte_prima = 0.0833*(salario_base + auxilio_transporte_efectivo)
	aporte_vacaciones = 0.0833*salario_base
	total_aporte_prestaciones_sociales = aporte_cesantias + aporte_intereses_cesantias + aporte_prima + aporte_vacaciones
	apropiaciones = total_aporte_seguridad_social + total_aporte_parafiscales + total_aporte_prestaciones_sociales
	costo_total_empresa = salario_base + apropiaciones + auxilio_transporte_efectivo
	
	print "  APROPIACIONES"
	print "  ---------------"
	print"\n"
	print "\t1. SEGURIDAD SOCIAL"
	print "\t-------------------"
	print ("\t  Pension 12%% = %.2f" % (aporte_pension_empresa)) 
	print ("\t  Salud 8.5%% = %.2f" % (aporte_salud_empresa)) 
	print ("\t  Riesgos (ARL) %.3f%% = %.2f" % (porcentaje_riesgos*100, aporte_arl_empresa)) 	
	print ("\n\t  ---> Total Seguridad Social = %.2f" % (total_aporte_seguridad_social))
	print "\n"
	print "\t2. PARAFISCALES"
	print "\t---------------"
	print ("\t  SENA 2%% = %.2f" % (aporte_parafiscales_sena)) 
	print ("\t  ICBF 3%% = %.2f" % (aporte_parafiscales_icbf)) 
	print ("\t  Cajas de Compensacion = %.2f" % (aporte_parafiscales_cajas)) 	
	print ("\n\t  ---> Total Parafiscales = %.2f" % (total_aporte_parafiscales))
	print "\n"
	print "\t3. PRESTACIONES SOCIALES"
	print "\t------------------------"
	print ("\t  Cesantias 8.33%% = %.2f" % (aporte_cesantias)) 
	print ("\t  Intereses sobre Cesantias 1%% = %.2f" % (aporte_intereses_cesantias)) 
	print ("\t  Prima de Servicios 8.33%% = %.2f" % (aporte_prima)) 	
	print ("\t  Vacaciones 4.17%% = %.2f" % (aporte_vacaciones)) 	
	print ("\n\t  ---> Total Prestaciones Sociales = %.2f" % (total_aporte_prestaciones_sociales))

	print "\n"
	print "  COSTO TOTAL PARA LA EMPRESA"
	print "  ---------------------------"
	print ("\t  Salario Base = %.2f" % (salario_base)) 
	print ("\t  Auxilio de Transporte = %.2f" % (auxilio_transporte_efectivo))
	print ("\t  Total Apropiaciones = %.2f" % (apropiaciones))	
	print ("\n\t  ---> Costo total para la empresa = %.2f" % (costo_total_empresa))
	print "\n"
	
else:
	aporte_fondo_solidaridad = 0
	aporte_salud_empleado = 0.04*salario_base

	if(debitar_fondo_solidaridad):
		aporte_fondo_solidaridad = porcentaje_fondo_solidaridad_pensional*salario_base
	aporte_pension_empleado = 0.04*salario_base
	deducciones = aporte_salud_empleado + aporte_pension_empleado + aporte_fondo_solidaridad
	salario_neto_empleado = salario_base - deducciones + auxilio_transporte_efectivo

	print "  DEDUCCIONES"
	print "  -----------"	
	print ("\tPension 4%% = %.2f" % (aporte_pension_empleado)) 
	print ("\tSalud 4%% = %.2f" % (aporte_salud_empleado))
	if(debitar_fondo_solidaridad):		
		print ("\tFondo de solidaridad Pensional %d%% = %.2f" % (porcentaje_fondo_solidaridad_pensional*100, aporte_fondo_solidaridad)) 	

	print"\n"	
	print "  SALARIO NETO PARA EL EMPLEADO"
	print "  -----------------------------"
	print ("\tSalario Base = %.2f" % (salario_base))
	print ("\tAuxilio de Transporte = %.2f" % (auxilio_transporte_efectivo))
	
	if(debitar_fondo_solidaridad):
		print ("\tPaga fondo de solidaridad ... ")
			
	print ("\tTotal Deducciones = %.2f" % (deducciones))	
	print ("\n\t---> Salario neto para el empleado = %.2f" % (salario_neto_empleado))
	print "\n"
	

