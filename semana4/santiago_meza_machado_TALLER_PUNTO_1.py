﻿# AyudanteNomina v2.1
'''
Programa para calcular la nomina de una empresa. Lee los nombres y salarios desde dos archivos de texto
que se suministran como argumentos de linea de comandos. Al final guarda la liquidacion en el archivo
liquidacion.txt, el registro de errores en errores.txt y el registro de operacion en log.txt.
'''
# Desarrollado por Santiago Meza Machado
# Septiembre 22 de 2015
# Valores de porcentajes para liquidacion de nomina tomados de http://www.gerencie.com/liquidacion-de-la-nomina.html.

# Importar libreria sys para manejo de argumentos de linea de comandos
import sys
import os
# ------------------ Inicio de definicion de constantes y parametros ------------------ #

# Nombre archivo de errores
nombre_archivo_errores = "errores.txt"

# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log.txt"

# Nombre archivo que contendra la liquidacion de la nomina
nombre_archivo_liquidacion = "liquidacion.txt"

# Numero minimo de lineas para archivo de nomina
numero_minimo_lineas = 2

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
porcentaje_riesgos = 0.00522

# ------------------ Fin de definicion de constantes y parametros ------------------ #

# ------------------ Inicio de definicion de funciones empleadas ------------------ #

# Funcion que crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True

# Funcion que lee las lineas de un archivo de texto y las devuelve en una lista.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 

# Funcion que guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.
def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True
	
# Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")
	
# Funcion que guarda un registro de operacion en el archivo log.txt
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")

# Funcion para validar una linea del archivo que contiene los nombres.
# Devuelve un array de tamanio 2. La primera posicion indica si es valido, con True y si es invalido con False.
# La segunda posicion contiene el nombre completo en caso de ser valida la linea, de lo contrario vacio.
def validar_linea_nombres(linea_por_validar, numero_linea):
	array_respuesta = [0 for x in range(2)]
		
	# Validar la estructura de cada linea.
	nombre_por_validar = linea_por_validar
	
	nombre_por_validar = nombre_por_validar[0:len(nombre_por_validar)-1]
	
	arreglo_nombre =  nombre_por_validar.split(" ")
	
	# Validar el numero de palabras del nombre
	# Validacion 5 (Va5)
	if (len(arreglo_nombre) < 2 or len(arreglo_nombre) > 5):
		guardar_error("El nombre " + linea_por_validar + " no cumple con la longitud requerida! Revisar linea numero " + str(numero_linea) + " de archivo de nomina.")
		array_respuesta[0] = False
		return array_respuesta	
	
	array_respuesta[1] = nombre_por_validar
	array_respuesta[0] = True
	return array_respuesta

# Funcion para validar una linea del archivo que contiene los salarios.
# Devuelve un array de tamanio 2. La primera posicion indica si es valido, con True y si es invalido con False.
# La segunda posicion contiene el salario en caso de ser valida la linea, de lo contrario vacio.
def validar_linea_salarios(linea_por_validar,numero_linea):
	array_respuesta = [0 for x in range(2)]
	
	# Validar el salario, que sea entero y que sea mayor que 0
	
	try:
		salario = int(linea_por_validar)
		if salario <= 0:
			array_respuesta[0] = False
			guardar_error("El salario de la linea " + str(numero_linea) + " es menor que 0")
			return array_respuesta
		array_respuesta[1] = salario
	except ValueError:
		guardar_error("El salario de la linea " + str(numero_linea) + " no es un valor entero")
		array_respuesta[0] = False
		return array_respuesta
	
	array_respuesta[0] = True
	return array_respuesta
	
# Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	try:
		os.remove(nombre_archivo_liquidacion)
	except WindowsError:
		a=0
	# Terminar el programa
	sys.exit()
	
# ------------------ Fin de definicion de funciones empleadas ------------------ #

# Inicializacion de archivos

# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo log.txt para almacenar el registro de operacion del programa.
crear_archivo("log.txt")

guardar_log("Creados archivos errores.txt y log.txt")

# Validaciones

# Obtener numero de argumentos de linea de comandos
cantidad_argumentos = len(sys.argv)

# Validar que el numero de argumentos sea igual a 2, garantizando que se haya el nombre del archivo de nomina.
# Validacion 1 (Va1)
if (cantidad_argumentos != 3):	
	terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con el nombre de archivo de nomina.")

guardar_log("Numero de argumentos OK")

nombre_archivo_nombres = sys.argv[1]
nombre_archivo_salarios = sys.argv[2]
extension_salarios = nombre_archivo_salarios.endswith(".txt")

# Validar que el archivo de nomina suministrado como argumento tenga extension .txt.
# Validacion 2 (Va2)
if (nombre_archivo_nombres.endswith(".txt") == False):
	if (extension_salarios == False):
		terminar_programa("Ambos archivos tienen extension erronea")
	else: 
		terminar_programa("El archivo nombres no tiene la extension correcta")
else:
	if (extension_salarios == False):
		terminar_programa("El archivo salarios no tiene la extension correcta")

guardar_log("Extension de archivos OK")

# Variable que almacena las lineas del archivo, su contenido como tal.
lineas_archivo_nombres = tuple(leer_lineas_archivo(nombre_archivo_nombres))
lineas_archivo_salarios = tuple(leer_lineas_archivo(nombre_archivo_salarios))

# Variable que almacena el numero de lineas del archivo
numero_lineas_nombres = len(lineas_archivo_nombres)
numero_lineas_salarios = len(lineas_archivo_salarios)

guardar_log("Archivo de nomina leido OK")

# Validar que el archivo tenga el minimo numero de lineas.
# Validacion 3 (Va3)
if (numero_lineas_nombres != numero_lineas_salarios):
	terminar_programa("Los archivos no tienen el mismo numero de lineas")
elif (numero_lineas_nombres < numero_minimo_lineas): 
	 terminar_programa("Los archivos tienen menos de 2 lineas")
guardar_log("Numero de lineas de ambos archivos OK")

# ------------------ Inicio de logica de programa ------------------ #
	
# Despues de realizar las lecturas y validaciones de los dos argumentos o variables del problema,
# se procede a realizar los calculos y procesamientos.

# Arrays que contendran la informacion de nomina y liquidacion.
# Se crea array nomina con dimensiones 2 columnas y tantas filas como empleados o numero de lineas en el archivo de nombres.txt, es decir, numero_lineas_nombres
# o numero_lineas_salarios, igualmente ambos tienen el mismo numero de lineas porque ya pasaron por tal validacion.
# nomina[indice][0] -> Nombre completo empleado
# nomina[indice][1] -> Salario empleado
nomina = [[columnas for columnas in range(2)] for filas in range(numero_lineas_nombres)]

# Se crea array liquidacion con dimensiones 13 columnas y tantas filas como empleados o numero de lineas en el archivo de nombres.txt, es decir, numero_lineas_nombres
# o numero_lineas_salarios, igualmente ambos tienen el mismo numero de lineas porque ya pasaron por tal validacion.
# liquidacion[indice][0] -> Aporte auxilio de transporte efectivo.
# liquidacion[indice][1] -> Aporte cesantias 
# liquidacion[indice][2] -> Aporte intereses sobre cesantias
# liquidacion[indice][3] -> Aporte prima
# liquidacion[indice][4] -> Aporte vacaciones
# liquidacion[indice][5] -> Aporte arl
# liquidacion[indice][6] -> Aporte salud empresa
# liquidacion[indice][7] -> Aporte pension empresa
# liquidacion[indice][8] -> Aporte salud empleado
# liquidacion[indice][9] -> Aporte pension empleado
# liquidacion[indice][10] -> Aporte fondo de solidaridad
# liquidacion[indice][11] -> Costo total para la empresa
# liquidacion[indice][12] -> Salario neto para el empleado
liquidacion = [[columnas for columnas in range(13)] for filas in range(numero_lineas_nombres)]

# Ciclo 1 para almacenar la informacion en el array de nomina
guardar_log("Cargando nomina en memoria...");
for x in range(0, numero_lineas_nombres):
	linea_validada_nombres = validar_linea_nombres(lineas_archivo_nombres[x], x+1)
	linea_validada_salarios = validar_linea_salarios(lineas_archivo_salarios[x], x+1)
	
	if(linea_validada_nombres[0] == False):
		if(linea_validada_salarios[0] == False):
			terminar_programa("Error en ambos archivos")
		else:
			terminar_programa("Error en archivo de nombres!")
	else:
		if(linea_validada_salarios[0] == False):
			terminar_programa("Error en archivo de salarios!")
	
	
	guardar_log("Procesando linea " + str(x+1));
	
	# Se almacena nombre completo
	nomina[x][0] = linea_validada_nombres[1]
	
	# Se almacena salario
	nomina[x][1] = linea_validada_salarios[1]

guardar_log("Nomina cargada en memoria!");
# Fin de ciclo 1

# Ciclo 2 para realizar el calculo de la liquidacion
guardar_log("Calculando liquidacion...");
for z in range(0, numero_lineas_nombres):
	# Se almacena salario base para realizar calculos
	salario_base = int(nomina[z][1])

	guardar_log("Calculando liquidacion para empleado " + str(z+1));	
	
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

	# --------------- Calculo de apropiaciones de nomina --------------- #
			
	# ----- Seguridad Social ----- #
	# Porcentaje aporte de salud realizado por la empresa 8.5%
	guardar_log("Calculando aporte salud empresa ...");	
	aporte_salud_empresa = 0.085*salario_base

	# Porcentaje aporte de salud realizado por la empresa 12%
	guardar_log("Calculando aporte pension empresa ...");
	aporte_pension_empresa = 0.12*salario_base

	# Porcentaje aporte de riesgos laborales realizado por la empresa.
	guardar_log("Calculando aporte ARL con porcentaje " + ("%.3f" % porcentaje_riesgos) + " ...");
	aporte_arl_empresa = porcentaje_riesgos*salario_base

	# Variable para acumular el aporte de seguridad social	
	total_aporte_seguridad_social = aporte_salud_empresa + aporte_pension_empresa + aporte_arl_empresa

	# ----- Aportes Parafiscales ----- #
	# Porcentaje aporte parafiscal para SENA realizado por la empresa 2%
	guardar_log("Calculando aporte parafiscales sena ...");
	aporte_parafiscales_sena = 0.02*salario_base

	# Porcentaje aporte parafiscal para ICBF realizado por la empresa 3%
	guardar_log("Calculando aporte parafiscales ICBF ...");
	aporte_parafiscales_icbf = 0.03*salario_base

	# Porcentaje aporte parafiscal para Cajas de Compensacion realizado por la empresa 4%
	guardar_log("Calculando aporte parafiscales cajas de compensacion ...");
	aporte_parafiscales_cajas = 0.04*salario_base

	# Variable para acumular el aporte a parafiscales
	total_aporte_parafiscales = aporte_parafiscales_sena + aporte_parafiscales_icbf + aporte_parafiscales_cajas

	# ----- Prestaciones Sociales ----- #	
	# Porcentaje aporte cesantias realizado por la empresa 8.33%. Se debe tener en cuenta el auxilio de transporte.
	guardar_log("Calculando aporte cesantias ...");
	aporte_cesantias = 0.0833*(salario_base + auxilio_transporte_efectivo)

	# Porcentaje aporte intereses sobre cesantias realizado por la empresa 1%
	guardar_log("Calculando aporte intereses sobre cesantias ...");
	aporte_intereses_cesantias = 0.01*aporte_cesantias

	# Porcentaje aporte prima de servicios realizado por la empresa 8.33%. Se debe tener en cuenta el auxilio de transporte.
	guardar_log("Calculando aporte prima de servicios ...");
	aporte_prima = 0.0833*(salario_base + auxilio_transporte_efectivo)

	# Porcentaje aporte vacaciones realizado por la empresa 4.17%
	guardar_log("Calculando aporte vacaciones ...");
	aporte_vacaciones = 0.0833*salario_base

	# Variable para acumular los aportes de prestaciones sociales
	total_aporte_prestaciones_sociales = aporte_cesantias + aporte_intereses_cesantias + aporte_prima + aporte_vacaciones

	# --------------- Calculo de costo total para la empresa --------------- #

	# Variable para acumular las apropiaciones de la empresa
	guardar_log("Calculando apropiaciones para la empresa ...");
	apropiaciones = total_aporte_seguridad_social + total_aporte_parafiscales + total_aporte_prestaciones_sociales

	# Costo total para la empresa
	guardar_log("Calculando costo total para la empresa ...");
	costo_total_empresa = salario_base + apropiaciones + auxilio_transporte_efectivo

	# Variable para guardar el aporte al fondo de solidaridad pensional. Por defecto es 0.
	aporte_fondo_solidaridad = 0
	
	# --------------- Calculo de deducciones --------------- #
	# Porcentaje aporte de salud realizado por el empleado 4%
	guardar_log("Calculando aporte salud empleado ...");
	aporte_salud_empleado = 0.04*salario_base

	if(debitar_fondo_solidaridad):
		guardar_log("Empleado paga fondo solidaridad pensional ...");
		aporte_fondo_solidaridad = porcentaje_fondo_solidaridad_pensional*salario_base		

	# Porcentaje aporte de salud realizado por el empleado 4%
	guardar_log("Calculando aporte pension empleado ...");
	aporte_pension_empleado = 0.04*salario_base

	# --------------- Calculo de salario neto para el empleado --------------- #

	# Variable para acumular las deducciones al empleado
	guardar_log("Calculando deducciones para el empleado ...");
	deducciones = aporte_salud_empleado + aporte_pension_empleado + aporte_fondo_solidaridad

	# Salario neto que percibe el empleado
	guardar_log("Calculando salario neto para el empleado ...");
	salario_neto_empleado = salario_base - deducciones + auxilio_transporte_efectivo
	
	# liquidacion[indice][0] -> Aporte auxilio de transporte efectivo.
	liquidacion[z][0] = auxilio_transporte_efectivo
	
	# liquidacion[indice][1] -> Aporte cesantias 
	liquidacion[z][1] = aporte_cesantias
	
	# liquidacion[indice][2] -> Aporte intereses sobre cesantias
	liquidacion[z][2] = aporte_intereses_cesantias
	
	# liquidacion[indice][3] -> Aporte prima
	liquidacion[z][3] = aporte_prima
	
	# liquidacion[indice][4] -> Aporte vacaciones
	liquidacion[z][4] = aporte_vacaciones
	
	# liquidacion[indice][5] -> Aporte arl
	liquidacion[z][5] = aporte_arl_empresa
	
	# liquidacion[indice][6] -> Aporte salud empresa
	liquidacion[z][6] = aporte_salud_empresa
	
	# liquidacion[indice][7] -> Aporte pension empresa
	liquidacion[z][7] = aporte_pension_empresa
	
	# liquidacion[indice][8] -> Aporte salud empleado
	liquidacion[z][8] = aporte_salud_empleado
	
	# liquidacion[indice][9] -> Aporte pension empleado
	liquidacion[z][9] = aporte_pension_empleado
	
	# liquidacion[indice][10] -> Aporte fondo de solidaridad
	liquidacion[z][10] = aporte_fondo_solidaridad
	
	# liquidacion[indice][11] -> Costo total para la empresa
	liquidacion[z][11] = costo_total_empresa
	
	# liquidacion[indice][12] -> Salario neto para el empleado
	liquidacion[z][12] = salario_neto_empleado	

guardar_log("Liquidacion calculada!");
# Fin de ciclo 2

guardar_log("Creando archivo " + nombre_archivo_liquidacion + " ...");
crear_archivo(nombre_archivo_liquidacion)

# Ciclo 3 para guardar liquidacion en archivo liquidacion.txt.
guardar_log("Guardando liquidacion...");

for w in range(0, numero_lineas_salarios):
	contenido_linea = (
		nomina[w][0], 
		int(nomina[w][1]), 
		liquidacion[w][0],
		liquidacion[w][1],
		liquidacion[w][2],
		liquidacion[w][3],
		liquidacion[w][4],
		liquidacion[w][5],
		liquidacion[w][6],
		liquidacion[w][7],
		liquidacion[w][8],
		liquidacion[w][9],
		liquidacion[w][10],
		liquidacion[w][11],
		liquidacion[w][12]
	)
	
	formato_linea = "%s*%.2f|%.2f|%.2f*%.2f*%.2f*%.2f|%.2f*%.2f*%.2f|%.2f*%.2f*%.2f|%.2f|%.2f\n"
	
	escribir_linea_archivo(nombre_archivo_liquidacion, formato_linea % (contenido_linea))

guardar_log("Liquidacion guardada...");
# Fin de ciclo 3