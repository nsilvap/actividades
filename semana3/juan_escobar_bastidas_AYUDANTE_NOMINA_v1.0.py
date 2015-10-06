# AyudanteNomina v1.0
# Desarrollado por Juan Sebastian Lopez Villa
# Agosto 30 de 2015
# Valores de porcentajes para liquidacion de nomina tomados de http://www.gerencie.com/liquidacion-de-la-nomina.html.

# Importar libreria sys para manejo de argumentos de linea de comandos
import sys

# Definicion de funciones empleadas 

# Funcion para solicitar una entrada numerica validando que sea numerica. Si se ingresa 
# algo que no sea numerico, vuelve a preguntar
def leer_numerico_entero( mensaje_a_mostrar ):
	valor_numerico_entero = 0
	while (True):	
		try:
			valor_numerico_entero = int(raw_input(mensaje_a_mostrar))
			break
		except ValueError:
			print "Lo que acaba de ingresar no se puede convertir a un valor numerico entero, por favor, vuelva a ingresar ...\n"
   
	return valor_numerico_entero

# Obtener numero de argumentos de linea de comandos
cantidad_argumentos = len(sys.argv)

# Definicion de variables globales para calculo de prestaciones, ya sea apropiaciones para la empresa o 
# deducciones para el empleado

# Constantes validas para el anio 2015

# Salario Minimo Legal Vigente (SMLV) 2015
salario_minimo = 644350

# Auxilio de Transporte 2015
auxilio_transporte = 74000

# El auxilio de transporte solo se da si gana igual o menor a 2 SMLV
tope_auxilio_transporte = 2*salario_minimo

# Quienes ganes igual o mas de 4 SMLV contribuyen 1% al fondo de solidaridad pensional
tope_fondo_solidaridad_pensional = 4*salario_minimo
porcentaje_fondo_solidaridad_pensional = 0.01

# Modifcar porcentaje segun el tipo de riesgo definido en: https://www.positiva.gov.co/ARL/Paginas/default.aspx
porcentaje_riesgos = 0.0814021

# Variable para almacenar el salario base para el calculo de las apropiaciones y las deducciones.
salario_base = 0

# Variable para el tipo de consulta. 1 para consultar las apropiaciones y el costo total para la 
# empresa, 2 para consultar las deducciones y el salario neto. Por defecto es 1, es decir,
# por defecto se muestra el total de apropiaciones y el costo para la empresa.
tipo_consulta = 1

# Validar que el numero de argumentos sea igual a 3, garantizando que se hayan suministrado tanto si
# desea consultar las apropiaciones o las deducciones asi como el salario base.
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
		
# Despues de realizar las lecturas y validaciones de los dos argumentos o variables del problema,
# se procede a realizar los calculos y procesamientos.

# Se imprime titulo del programa
print "\n"
print "-------------------------------------------------------------------"
print "                       AYUDANTE NOMINA v1.0"
print "-------------------------------------------------------------------"
print "\n"

# Variable booleana (True|False) que indica si tiene derecho a auxilio de transporte. True para Si, False para No.
# Valor por defecto False, es decir, no se le dar auxilio de transporte.
dar_auxilio_transporte = False

# Variable para almacenar el auxilio de transporte a aplicar. Por defecto es 0.
auxilio_transporte_efectivo = 0

# Validar si tiene derecho a auxilio de transporte
if(salario_base <= tope_auxilio_transporte):
	dar_auxilio_transporte = True
	
if(dar_auxilio_transporte):
	auxilio_transporte_efectivo = auxilio_transporte
else:
	auxilio_transporte_efectivo = 0

# Variable booleana (True|False) que indica si debe pagar fondo de solidaridad pensional. True para Si, False para No.
# Valor por defecto False, es decir, no se debe pagar fondo de solidaridad pensional.
debitar_fondo_solidaridad = False

# Validar si debe pagar fondo de solidaridad pensional
if(salario_base >= tope_fondo_solidaridad_pensional):
	debitar_fondo_solidaridad = True
		
if(tipo_consulta == 1): # Calculo de costo total para la empresa

	# --------------- Calculo de apropiaciones de nomina --------------- #
		
	# ----- Seguridad Social ----- #
	# Porcentaje aporte de salud realizado por la empresa 8.5%
	aporte_salud_empresa = 0.085*salario_base

	# Porcentaje aporte de salud realizado por la empresa 12%
	aporte_pension_empresa = 0.12*salario_base

	# Porcentaje aporte de riesgos laborales realizado por la empresa.
	aporte_arl_empresa = porcentaje_riesgos*salario_base

	# Variable para acumular el aporte de seguridad social
	total_aporte_seguridad_social = aporte_salud_empresa + aporte_pension_empresa + aporte_arl_empresa

	# ----- Aportes Parafiscales ----- #
	# Porcentaje aporte parafiscal para SENA realizado por la empresa 2%
	aporte_parafiscales_sena = 0.02*salario_base

	# Porcentaje aporte parafiscal para ICBF realizado por la empresa 3%
	aporte_parafiscales_icbf = 0.03*salario_base

	# Porcentaje aporte parafiscal para Cajas de Compensacion realizado por la empresa 4%
	aporte_parafiscales_cajas = 0.04*salario_base

	# Variable para acumular el aporte a parafiscales
	total_aporte_parafiscales = aporte_parafiscales_sena + aporte_parafiscales_icbf + aporte_parafiscales_cajas

	# ----- Prestaciones Sociales ----- #	
	# Porcentaje aporte cesantias realizado por la empresa 8.33%. Se debe tener en cuenta el auxilio de transporte.
	aporte_cesantias = 0.0833*(salario_base + auxilio_transporte_efectivo)

	# Porcentaje aporte intereses sobre cesantias realizado por la empresa 1%
	aporte_intereses_cesantias = 0.01*aporte_cesantias

	# Porcentaje aporte prima de servicios realizado por la empresa 8.33%. Se debe tener en cuenta el auxilio de transporte.
	aporte_prima = 0.0833*(salario_base + auxilio_transporte_efectivo)

	# Porcentaje aporte vacaciones realizado por la empresa 4.17%
	aporte_vacaciones = 0.0833*salario_base

	# Variable para acumular los aportes de prestaciones sociales
	total_aporte_prestaciones_sociales = aporte_cesantias + aporte_intereses_cesantias + aporte_prima + aporte_vacaciones

	# --------------- Calculo de costo total para la empresa --------------- #

	# Variable para acumular las apropiaciones de la empresa
	apropiaciones = total_aporte_seguridad_social + total_aporte_parafiscales + total_aporte_prestaciones_sociales
	
	# Costo total para la empresa
	costo_total_empresa = salario_base + apropiaciones + auxilio_transporte_efectivo
	
	# --------------- Mostrar en pantalla las diferentes apropiaciones --------------- #
	print "-------------------------------------------------------------------"
	print "                       APROPIACIONES"
	print "-------------------------------------------------------------------"
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       1. SEGURIDAD SOCIAL"
	print "-------------------------------------------------------------------"
	print ("\tPension 12%% = %.2f" % (aporte_pension_empresa)) 
	print ("\tSalud 8.5%% = %.2f" % (aporte_salud_empresa)) 
	print ("\tRiesgos (ARL) %.3f%% = %.2f" % (porcentaje_riesgos*100, aporte_arl_empresa)) 	
	print ("\n\t---> Total Seguridad Social = %.2f" % (total_aporte_seguridad_social))
	print "-------------------------------------------------------------------"
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       2. PARAFISCALES"
	print "-------------------------------------------------------------------"
	print ("\tSENA 2%% = %.2f" % (aporte_parafiscales_sena)) 
	print ("\tICBF 3%% = %.2f" % (aporte_parafiscales_icbf)) 
	print ("\tCajas de Compensacion = %.2f" % (aporte_parafiscales_cajas)) 	
	print ("\n\t---> Total Parafiscales = %.2f" % (total_aporte_parafiscales))
	print "-------------------------------------------------------------------"
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       3. PRESTACIONES SOCIALES"
	print "-------------------------------------------------------------------"
	print ("\tCesantias 8.33%% = %.2f" % (aporte_cesantias)) 
	print ("\tIntereses sobre Cesantias 1%% = %.2f" % (aporte_intereses_cesantias)) 
	print ("\tPrima de Servicios 8.33%% = %.2f" % (aporte_prima)) 	
	print ("\tVacaciones 4.17%% = %.2f" % (aporte_vacaciones)) 	
	print ("\n\t---> Total Prestaciones Sociales = %.2f" % (total_aporte_prestaciones_sociales))
	print "-------------------------------------------------------------------"
	print "\n"
	
	# --------------- Mostrar en pantalla el costo total para la empresa --------------- #
	
	print "\n"
	print "-------------------------------------------------------------------"
	print "                       COSTO TOTAL PARA LA EMPRESA"
	print "-------------------------------------------------------------------"
	print ("\tSalario Base = %.2f" % (salario_base)) 
	print ("\tAuxilio de Transporte = %.2f" % (auxilio_transporte_efectivo))
	print ("\tTotal Apropiaciones = %.2f" % (apropiaciones))	
	print ("\n\t---> Costo total para la empresa = %.2f" % (costo_total_empresa))
	print "-------------------------------------------------------------------"
	print "\n"
	
else: # Calculo de salario neto para el empleado	

	# Variable para guardar el aporte al fondo de solidaridad pensional. Por defecto es 0.
	aporte_fondo_solidaridad = 0
	
	# --------------- Calculo de deducciones --------------- #
	# Porcentaje aporte de salud realizado por el empleado 4%
	aporte_salud_empleado = 0.04*salario_base

	if(debitar_fondo_solidaridad):
		aporte_fondo_solidaridad = porcentaje_fondo_solidaridad_pensional*salario_base		
	
	# Porcentaje aporte de salud realizado por el empleado 4%
	aporte_pension_empleado = 0.04*salario_base
	
	# --------------- Calculo de salario neto para el empleado --------------- #
	
	# Variable para acumular las deducciones al empleado
	deducciones = aporte_salud_empleado + aporte_pension_empleado + aporte_fondo_solidaridad
	
	# Salario neto que percibe el empleado
	salario_neto_empleado = salario_base - deducciones + auxilio_transporte_efectivo

	# --------------- Mostrar en pantalla las diferentes deducciones --------------- #	
	print "-------------------------------------------------------------------"
	print "                       DEDUCCIONES"
	print "-------------------------------------------------------------------"	
	print ("\tPension 4%% = %.2f" % (aporte_pension_empleado)) 
	print ("\tSalud 4%% = %.2f" % (aporte_salud_empleado))
	if(debitar_fondo_solidaridad):		
		print ("\tFondo de solidaridad Pensional %d%% = %.2f" % (porcentaje_fondo_solidaridad_pensional*100, aporte_fondo_solidaridad)) 	
	print "-------------------------------------------------------------------"
	print "\n"
	
	# --------------- Mostrar en pantalla el salario neto para el empleado --------------- # 
		
	print "-------------------------------------------------------------------"
	print "                       SALARIO NETO PARA EL EMPLEADO"
	print "-------------------------------------------------------------------"
	print ("\tSalario Base = %.2f" % (salario_base))
	print ("\tAuxilio de Transporte = %.2f" % (auxilio_transporte_efectivo))
	
	if(debitar_fondo_solidaridad):
		print ("\tPaga fondo de solidaridad ... ")
			
	print ("\tTotal Deducciones = %.2f" % (deducciones))	
	print ("\n\t---> Salario neto para el empleado = %.2f" % (salario_neto_empleado))
	print "-------------------------------------------------------------------"
	print "\n"