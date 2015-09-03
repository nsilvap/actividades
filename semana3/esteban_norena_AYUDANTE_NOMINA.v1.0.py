# AyudanteNomina v1.0
# Desarrollado por Esteban Norena
# Septiembre 3 de 2015
# Valores de porcentajes para liquidacion de nomina tomados de http://www.gerencie.com/liquidacion-de-la-nomina.html.
import sys

#Inicializacion de variables constantes

auxilio_trans = 74000
salario_minimo = 644350
tope_aux = 2*salario_minimo
tope_fondo_solidaridad = 4*salario_minimo
porcentaje_fondo_solidaridad = 0.01
porcentaje_riesgos = 0.00814048


cantidad_arg = len(sys.argv)

# Proceso de validacion

if cantidad_arg != 3:
	while (True):
		sal = raw_input("Ingrese su salario: ")
		try:
			sal = int(sal)
			if sal > 0:
				break
			else:
				print "Por favor ingrese un salario positivo"
		except ValueError:
			print "ATENCION: Debe ingresar un numero entero."
	
	while (True):
		tipo = raw_input("Ingrese 1 para calcular el costo de la empresa o 2 para calcular salario neto del empleado: ")
		try:
			tipo = int(tipo)
			if tipo == 1 or tipo == 2:
				break
			else:
				print "Por favor ingrese 1 o 2"
		except ValueError:
			print "ATENCION: Debe ingresar el numero 1 o el numero 2"
else:
	sal = sys.argv[1]
	try:
		sal = int(sal)
		if sal <= 0:
			print "El salario debe ser positivo, el programa se cerrara"
			sys.exit()
	except ValueError:
		print "El argumento del salario debe ser un numero entero, el programa se cerrara"
		sys.exit()
	tipo = int(sys.argv[2])
	try:
		tipo=int(tipo)
		if tipo != 1 and tipo != 2:
			print "Debe ingresar un tipo valido, sea 1 o 2, el programa se cerrara"
			sys.exit()
	except ValueError:
		print "El argumento del tipo debe ser un numero entero, el programa se cerrara"
		sys.exit()

#Proceso de calculos de porcentajes

print "\n"
print "-------------------------------------------------------------------"
print "                       AYUDANTE NOMINA v1.0"
print "-------------------------------------------------------------------"
print "\n"

if sal <= tope_aux:
	aux_trans_efec = auxilio_trans
else:
	aux_trans_efec = 0

debitar_fondo = False
if sal >= tope_fondo_solidaridad:
	debitar_fondo = True

sal_total = sal + aux_trans_efec

if tipo == 1:
# Seguridad Social
	salud_empresa = 0.085*sal
	pension_empresa = 0.12*sal
	arp_empresa = porcentaje_riesgos*sal
	seguridad_social = salud_empresa + pension_empresa + arp_empresa
# Parafiscales
	sena = 0.02*sal
	icbf = 0.03*sal
	cajas = 0.04*sal
	parafiscales = sena + icbf + cajas
# Prestaciones
	cesantias = 0.0833*sal_total
	int_cesantias = 0.01*cesantias
	prima = 0.0833*sal_total
	vacaciones = 0.0833*sal
	prestaciones = cesantias + int_cesantias + prima + vacaciones
# Apropiaciones
	apropiaciones = seguridad_social + parafiscales + prestaciones
# Nomina total
	nomina_empresa = apropiaciones + sal_total
	print "-------------------------------------------------------------------"
	print "                       APROPIACIONES"
	print "-------------------------------------------------------------------"
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       1. SEGURIDAD SOCIAL"
	print "-------------------------------------------------------------------"
	print ("\tPension 12%% = %.2f" % (pension_empresa)) 
	print ("\tSalud 8.5%% = %.2f" % (salud_empresa)) 
	print ("\tRiesgos (ARL) %.6f%% = %.2f" % (porcentaje_riesgos*100, arp_empresa)) 
	print ("\n\t---> Total Seguridad Social = %.2f" % (seguridad_social))
	print "-------------------------------------------------------------------"
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       2. PARAFISCALES"
	print "-------------------------------------------------------------------"
	print ("\tSENA 2%% = %.2f" % (sena)) 
	print ("\tICBF 3%% = %.2f" % (icbf)) 
	print ("\tCajas de Compensacion = %.2f" % (cajas)) 	
	print ("\n\t---> Total Parafiscales = %.2f" % (parafiscales))
	print "-------------------------------------------------------------------"
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       3. PRESTACIONES SOCIALES"
	print "-------------------------------------------------------------------"
	print ("\tCesantias 8.33%% = %.2f" % (cesantias)) 
	print ("\tIntereses sobre Cesantias 1%% = %.2f " % (int_cesantias)) 
	print ("\tPrima de Servicios 8.33%% = %.2f" % (prima)) 	
	print ("\tVacaciones 4.17%% = %.2f" % (vacaciones)) 	
	print ("\n\t---> Total Prestaciones Sociales = %.2f" % (prestaciones))
	print "-------------------------------------------------------------------"
	print "\n"
	
	# --------------- Mostrar en pantalla el costo total para la empresa --------------- #
	
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       COSTO TOTAL PARA LA EMPRESA"
	print "-------------------------------------------------------------------"
	print ("\tSalario Base = %.2f" % (sal)) 
	print ("\tAuxilio de Transporte = %.2f" % (aux_trans_efec))
	print ("\tTotal Apropiaciones = %.2f" % (apropiaciones))
	print ("\n\t---> Costo total para la empresa = %.2f" % (nomina_empresa))
	print "-------------------------------------------------------------------"
	print "\n"
else:
	fondo_solidaridad = 0
# Deducciones
	if (debitar_fondo):
		fondo_solidaridad = porcentaje_fondo_solidaridad*sal
	pension_empleado = 0.04*sal
	salud_empleado = 0.04*sal
	deducciones = pension_empleado + salud_empleado + fondo_solidaridad
# Salario neto
	salario_neto = sal_total - deducciones
	print "-------------------------------------------------------------------"
	print "                       DEDUCCIONES"
	print "-------------------------------------------------------------------"	
	print ("\tPension 4%% = %.2f" % (pension_empleado)) 
	print ("\tSalud 4%% = %.2f" % (salud_empleado))
	if(debitar_fondo):
		print ("\tFondo de solidaridad Pensional %d%% = %.2f" % (porcentaje_fondo_solidaridad*100, fondo_solidaridad))
	print "-------------------------------------------------------------------"
	print "\n"
	
	# --------------- Mostrar en pantalla el salario neto para el empleado --------------- # 
		
	print "-------------------------------------------------------------------"
	print "                       SALARIO NETO PARA EL EMPLEADO"
	print "-------------------------------------------------------------------"
	print ("\tSalario Base = %.2f" % (sal))
	print ("\tAuxilio de Transporte = %.2f" % (aux_trans_efec))
	
	if(debitar_fondo):
		print ("\tPaga fondo de solidaridad ... ")
			
	print ("\tTotal Deducciones = %.2f" % (deducciones))
	print ("\n\t---> Salario neto para el empleado = %.2f" % (salario_neto))
	print "-------------------------------------------------------------------"
	print "\n"