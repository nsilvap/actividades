# AyudanteNomina v2.0.6
# Programa para calcular la nomina de una empresa. Lee los nombres y salarios desde un archivo de texto
# que se suministra como argumento de linea de comandos, las apropiaciones y deducciones
# las lee desde dos archivos diferentes como argumento de linea de comandos. Al final guarda la liquidacion
# en el archivo liquidacion.txt, el registro de errores en errores.txt y el registro de operacion en log.txt.

# Desarrollado por Angela Giovanna Espinosa Restrepo
# Septiembre 21 de 2015
# Valores de porcentajes para liquidacion de nomina tomados de http://www.gerencie.com/liquidacion-de-la-nomina.html.

# Importar libreria sys para manejo de argumentos de linea de comandos
import sys

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

# Funcion para validar una linea del archivo que contiene las apropiaciones.
# Devuelve un array de tamanio 2. La primera posicion indica si es valido, con True y si es invalido con False.
# La segunda posicion contiene las apropiaciones en caso de ser valida la linea, de lo contrario vacio.
def validar_linea_apr(linea_por_validar, numero_linea):	
	array_respuesta_ap = [0 for x in range(3)]
	
	# Separar la linea por el simbolo (token) *
	arreglo_campos_ap = linea_por_validar.split("*")
	
	# Validar la estructura de cada linea.
	# Validacion 4 (Va4)
	if (len(arreglo_campos_ap) != 2):
		guardar_error("La linea " + str(numero_linea) + " del archivo de apropiaciones cumple con la estructura requerida! Revisarla!")
		array_respuesta_ap[0] = False
		return array_respuesta_ap
		
	arr_apropiaciones = arreglo_campos_ap[0]
	
	
	array_respuesta_ap[1] = arr_apropiaciones
	
	# Validar que la apropiacion sea numerica
	try:
		porcentaje_apropiaciones = float(arreglo_campos_ap[1])								
		array_respuesta_ap[2] = porcentaje_apropiaciones
	except ValueError:	
		guardar_error("El valor de apropiacion " + arreglo_campos_ap[1] + " no puede convertirse a entero! Revisar linea numero " + str(numero_linea) + " de archivo de apropiaciones.")
		array_respuesta_ap[0] = False
		return array_respuesta_ap
		
	array_respuesta_ap[0] = True
	return array_respuesta_ap
	
# Funcion para validar una linea del archivo que contiene las deducciones.
# Devuelve un array de tamanio 2. La primera posicion indica si es valido, con True y si es invalido con False.
# La segunda posicion contiene las deducciones en caso de ser valida la linea, de lo contrario vacio.	
def validar_linea_ded(linea_por_validar, numero_linea):	
	array_respuesta_ded = [0 for x in range(3)]
	
	# Separar la linea por el simbolo (token) *
	arreglo_campos_ded = linea_por_validar.split("*")
	
	# Validar la estructura de cada linea.
	# Validacion 4 (Va4)
	if (len(arreglo_campos_ded) != 2):
		guardar_error("La linea " + str(numero_linea) + " de archivo de deducciones no cumple con la estructura requerida! Revisarla!")
		array_respuesta_ded[0] = False
		return array_respuesta_ded
		
	arr_deducciones = arreglo_campos_ded[0]
	
	array_respuesta_ded[1] = arr_deducciones
	
	# Validar que la deduccion sea de tipo numerico
	try:
		porcentaje_deducciones = float(arreglo_campos_ded[1])								
		array_respuesta_ded[2] = porcentaje_deducciones
	except ValueError:	
		guardar_error("El valor de salario " + arreglo_campos_ded[1] + " no puede convertirse a entero! Revisar linea numero " + str(numero_linea) + " de archivo de deducciones.")
		array_respuesta_ded[0] = False
		return array_respuesta_ded
		
	array_respuesta_ded[0] = True
	return array_respuesta_ded
	
# Funcion para validar una linea del archivo que contiene la nomina.
# Devuelve un array de tamanio 3. La primera posicion indica si es valido, con True y si es invalido con False.
# La segunda posicion contiene el nombre completo en caso de ser valida la linea, de lo contrario vacio.
# La tercera posicion contiene el salrio en caso de ser valida la linea, de lo contrario vacio.
def validar_linea(linea_por_validar, numero_linea):	
	array_respuesta = [0 for x in range(3)]
	
# Separar la linea por el simbolo (token) *
	arreglo_campos = linea_por_validar.split("*")
	
	# Validar la estructura de cada linea.
	# Validacion 4 (Va4)
	if (len(arreglo_campos) != 2):
		guardar_error("La linea " + str(numero_linea) + " no cumple con la estructura requerida! Revisarla!")
		array_respuesta[0] = False
		return array_respuesta
		
	nombre_por_validar = arreglo_campos[0]
	
	arreglo_nombre =  nombre_por_validar.split(" ")
	
	# Validar el numero de palabras del nombre
	# Validacion 5 (Va5)
	if (len(arreglo_nombre) < 2 or len(arreglo_nombre) > 5):
		guardar_error("El nombre " + arreglo_campos[0] + " no cumple con la longitud requerida! Revisar linea numero " + str(numero_linea) + " de archivo de nomina.")
		array_respuesta[0] = False
		return array_respuesta
	
	array_respuesta[1] = arreglo_nombre
	
	# Validar que el salario sea de tipo numerico
	# Validacion 6 (Va6)
	try:
		salario_base = int(arreglo_campos[1])								
		array_respuesta[2] = salario_base
	except ValueError:	
		guardar_error("El valor de salario " + arreglo_campos[1] + " no puede convertirse a entero! Revisar linea numero " + str(numero_linea) + " de archivo de nomina.")
		array_respuesta[0] = False
		return array_respuesta
		
	array_respuesta[0] = True
	return array_respuesta
	
# Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
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

# Validar que el numero de argumentos sea igual a 4, garantizando que se haya el nombre del archivo de nomina, de apropiaciones y de deducciones
# Validacion 1 (Va1)
if (cantidad_argumentos != 4):	
	terminar_programa("Numero de argumentos incorrecto. Debe suministrar un argumento con el nombre de archivo de nomina, archivo de apropiaciones y archivo de deducciones.")

guardar_log("Numero de argumentos OK")

nombre_archivo_nomina = sys.argv[1]

nombre_archivo_apropiaciones = sys.argv[2]

nombre_archivo_deducciones = sys.argv[3]

# Validar que los archivos suministrado como argumentos tengan extension .txt.
# Validacion 2 (Va2)
if (nombre_archivo_nomina.endswith(".txt") == False):
	terminar_programa("El archivo de nomina no tiene extension .txt!")
	
guardar_log("Extension de archivo de nomina OK")

if (nombre_archivo_apropiaciones.endswith(".txt") == False):
	terminar_programa("El archivo de apropiaciones no tiene extension .txt!")
	
guardar_log("Extension de archivo de apropiaciones OK")

if (nombre_archivo_deducciones.endswith(".txt") == False):
	terminar_programa("El archivo de deducciones no tiene extension .txt!")
	
guardar_log("Extension de archivo de deducciones OK")

# Variable que almacena las lineas del archivo nomina, su contenido como tal.
lineas_archivo_nomina = tuple(leer_lineas_archivo(nombre_archivo_nomina))

# Variable que almacena el numero de lineas del archivo nomina
numero_lineas_nomina = len(lineas_archivo_nomina)

guardar_log("Archivo de nomina leido OK")

# Variable que almacena las lineas del archivo apropiaciones, su contenido como tal.
lineas_archivo_apropiaciones = tuple(leer_lineas_archivo(nombre_archivo_apropiaciones))

# Variable que almacena el numero de lineas del archivo apropiaciones
numero_lineas_apropiaciones = len(lineas_archivo_apropiaciones)

guardar_log("Archivo de apropiaciones leido OK")

# Variable que almacena las lineas del archivo deducciones, su contenido como tal.
lineas_archivo_deducciones = tuple(leer_lineas_archivo(nombre_archivo_deducciones))

# Variable que almacena el numero de lineas del archivo deducciones
numero_lineas_deducciones = len(lineas_archivo_deducciones)

guardar_log("Archivo de deducciones leido OK")

# Validar que el archivo de nomina tenga el minimo numero de lineas.
# Validacion 3 (Va3)
if (numero_lineas_nomina < numero_minimo_lineas):
	terminar_programa("El archivo de nomina debe contener como minimo " + str(numero_minimo_lineas) + " lineas!")

# ------------------ Inicio de logica de programa ------------------ #
	
# Despues de realizar las lecturas y validaciones de los dos argumentos o variables del problema,
# se procede a realizar los calculos y procesamientos.

# Arrays que contendran la informacion de nomina, apropiaciones, deducciones y liquidacion.
# Se crea array nomina con dimensiones 2 columnas y tantas filas como empleados o numero de lineas en el archivo de nomina.txt, es decir, numero_lineas_nomina
# nomina[indice][0] -> Nombre completo empleado
# nomina[indice][1] -> Salario empleado
nomina = [[columnas for columnas in range(2)] for filas in range(numero_lineas_nomina)]

#Se crea un array apropiaciones con dimension 1 columna x tantas filas como apropiaciones o numero de lineas tenga el archivo de apropiaciones.txt
#apropiaciones[indice][0] -> Porcentaje de apropiacion
apropiaciones = [[columnas for columnas in range(1)] for filas in range(numero_lineas_apropiaciones)]

#Se crea un array deducciones con dimension 1 columna x tantas filas como deducciones o numero de lineas tenga el archivo de deducciones.txt
#deducciones[indice][0] -> Porcentaje de deduccion
deducciones = [[columnas for columnas in range(1)] for filas in range(numero_lineas_deducciones)]

# Se crea array liquidacion con dimensiones 13 columnas y tantas filas como empleados o numero de lineas en el archivo de nombres.txt, es decir, numero_lineas_nomina
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
liquidacion = [[columnas for columnas in range(13)] for filas in range(numero_lineas_nomina)]

# Ciclo 1 para almacenar la informacion en el array de nomina
guardar_log("Cargando nomina en memoria...");
for x in range(0, numero_lineas_nomina):
	linea_validada = validar_linea(lineas_archivo_nomina[x], x+1)
	
	if(linea_validada[0] == False):
		terminar_programa("Error en archivo de nomina!")

	guardar_log("Procesando linea " + str(x+1));
	
	# Se almacena nombre completo
	nomina[x][0] = linea_validada[1]
	
	# Se almacena salario
	nomina[x][1] = linea_validada[2]

guardar_log("Nomina cargada en memoria!");
# Fin de ciclo 1

# Ciclo 2 para almacenar la informacion en el array de apropiaciones
guardar_log("Cargando apropiaciones en memoria...");
for m in range(0, numero_lineas_apropiaciones):
	linea_validada_apr = validar_linea_apr(lineas_archivo_apropiaciones[m], m+1)
	
	if(linea_validada_apr[0] == False):
		terminar_programa("Error en archivo de apropiaciones!")

	guardar_log("Procesando linea " + str(m+1));
	

	# Se almacenan apropiaciones
	apropiaciones[m][0] = linea_validada_apr[2]

guardar_log("apropiaciones cargada en memoria!");

#Definicion de porcentaje de apropiaciones

apr_salud = apropiaciones[0][0]
apr_pension = apropiaciones[1][0]
apr_arl = apropiaciones[2][0]
apr_sena = apropiaciones[3][0]
apr_ICBF = apropiaciones[4][0]
apr_cajascomp = apropiaciones[5][0]
apr_cesantias =  apropiaciones[6][0]
apr_intcesant = apropiaciones[7][0]
apr_prima =  apropiaciones[8][0]
apr_vacaciones =  apropiaciones[9][0]

# Fin de ciclo 2

# Ciclo 3 para almacenar la informacion en el array de deducciones

guardar_log("Cargando deducciones en memoria...");
for n in range(0, numero_lineas_deducciones):
	linea_validada_ded = validar_linea_ded(lineas_archivo_deducciones[n], n+1)
	
	if(linea_validada_ded[0] == False):
		terminar_programa("Error en archivo de deducciones!")

	guardar_log("Procesando linea " + str(n+1));
	
	# Se almacena deducciones
	deducciones[n][0] = linea_validada_ded[2]

guardar_log("Nomina cargada en memoria!");

#Definicion de porcentaje de deducciones

ded_salud = deducciones[0][0]
ded_solidaridad = deducciones[1][0]
ded_pension = deducciones[2][0]

# Fin de ciclo 3

# Ciclo 4 para realizar el calculo de la liquidacion
guardar_log("Calculando liquidacion...");
for z in range(0, numero_lineas_nomina):
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
	aporte_salud_empresa = apr_salud*salario_base

	# Porcentaje aporte de salud realizado por la empresa 12%
	guardar_log("Calculando aporte pension empresa ...");
	aporte_pension_empresa = apr_pension*salario_base

	# Porcentaje aporte de riesgos laborales realizado por la empresa.
	guardar_log("Calculando aporte ARL con porcentaje " + ("%.3f" % apr_arl) + " ...");
	aporte_arl_empresa = apr_arl*salario_base

	# Variable para acumular el aporte de seguridad social	
	total_aporte_seguridad_social = aporte_salud_empresa + aporte_pension_empresa + aporte_arl_empresa

	# ----- Aportes Parafiscales ----- #
	# Porcentaje aporte parafiscal para SENA realizado por la empresa 2%
	guardar_log("Calculando aporte parafiscales sena ...");
	aporte_parafiscales_sena = apr_sena*salario_base

	# Porcentaje aporte parafiscal para ICBF realizado por la empresa 3%
	guardar_log("Calculando aporte parafiscales ICBF ...");
	aporte_parafiscales_icbf = apr_ICBF*salario_base

	# Porcentaje aporte parafiscal para Cajas de Compensacion realizado por la empresa 4%
	guardar_log("Calculando aporte parafiscales cajas de compensacion ...");
	aporte_parafiscales_cajas =apr_cajascomp*salario_base

	# Variable para acumular el aporte a parafiscales
	total_aporte_parafiscales = aporte_parafiscales_sena + aporte_parafiscales_icbf + aporte_parafiscales_cajas

	# ----- Prestaciones Sociales ----- #	
	# Porcentaje aporte cesantias realizado por la empresa 8.33%. Se debe tener en cuenta el auxilio de transporte.
	guardar_log("Calculando aporte cesantias ...");
	aporte_cesantias = apr_cesantias*(salario_base + auxilio_transporte_efectivo)

	# Porcentaje aporte intereses sobre cesantias realizado por la empresa 1%
	guardar_log("Calculando aporte intereses sobre cesantias ...");
	aporte_intereses_cesantias =apr_intcesant*aporte_cesantias

	# Porcentaje aporte prima de servicios realizado por la empresa 8.33%. Se debe tener en cuenta el auxilio de transporte.
	guardar_log("Calculando aporte prima de servicios ...");
	aporte_prima = apr_prima*(salario_base + auxilio_transporte_efectivo)

	# Porcentaje aporte vacaciones realizado por la empresa 4.17%
	guardar_log("Calculando aporte vacaciones ...");
	aporte_vacaciones =apr_vacaciones*salario_base

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
	aporte_salud_empleado = ded_salud*salario_base

	if(debitar_fondo_solidaridad):
		guardar_log("Empleado paga fondo solidaridad pensional ...");
		aporte_fondo_solidaridad = ded_solidaridad*salario_base		

	# Porcentaje aporte de salud realizado por el empleado 4%
	guardar_log("Calculando aporte pension empleado ...");
	aporte_pension_empleado = ded_pension*salario_base

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
# Fin de ciclo 4

guardar_log("Creando archivo " + nombre_archivo_liquidacion + " ...");
crear_archivo(nombre_archivo_liquidacion)

# Ciclo 5 para guardar liquidacion en archivo liquidacion.txt.
guardar_log("Guardando liquidacion...");
for w in range(0, numero_lineas_nomina):
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
# Fin de ciclo 5 
