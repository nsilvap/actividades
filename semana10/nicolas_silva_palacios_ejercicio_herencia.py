'''
Ejercicio herencia v.0.0.1

El programa es capaz de detectar el tipo de vehiculo leyendo la primera linea y segun el tipo, 
save la informacion en un objeto de la clase correspondiente. Despues de leer la informacion y savela en el objeto, 
imprime la informacion del archivo en pantalla leyendo los campos desde el objeto creado.

Desarrollado por:
Nicolas Silva Palacios
Fecha Ultima Edicion:
12/10/2015

'''

# Importar libreria sys para manejo de argumentos en la linea de comandos
import sys

# Obtener numero de argumentos de linea de comandos
cantidad_argumentos = len(sys.argv)

#-------------------Definicion de funciones ---------------------------------------

# Funcion que lee las lineas de un archivo de texto y las devuelve en una lista.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		save_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 
	print lineas

def save_info(linea_a_save, numero_linea):
	array_respuesta = [0 for x in range(2)]
	
	arreglo_campos = linea_a_save.split("=")
	
	caracteristica_save = arreglo_campos[0]
	
	arreglo_caracteristicas = caracteristica_save
	
	array_respuesta[0] = caracteristica_save
	
	parametro_caracteristica = str(arreglo_campos[1])	
	
	array_respuesta[1] = parametro_caracteristica
	
	return array_respuesta
#---------------------------------------------Definicion de clases ------------------------------------------------------
class vehiculo (object):
	def __init__ (self,modelo,c_motor,n_ejes):
		self.modelo=modelo
		self.c_motor=c_motor
		self.n_ejes=n_ejes
	def mostrar_detalles(self):
		print "Se ha registrado un vehiculo"
		print"---------------------------------------"
		return "Los datos del vehiculo son:"+ str(self.modelo)+"  "+str(self.c_motor)+"  "+str(self.n_ejes)
	def arrancar(self):
		return "El vehiculo acaba de arrancar"
	def apagar(self):
		return "El carro se apagara por fallas"
	

class vehiculo_aereo(vehiculo):
	def __init__ (self,modelo,c_motor,n_ejes,n_alas,n_alerones):
		vehiculo.__init__(self,modelo,c_motor,n_ejes)
		self.n_alas=n_alas
		self.n_alerones=n_alerones
	def especificaciones(self):
		print "Se ha registrado un vehiculo"
		print"---------------------------------------"
		return "El vehiculo aereo tiene: "+str(self.n_alas)+" "+"alas"+" , "+str(self.n_alerones)+" alerones"
	def despegar (self):
		return "Estamos listos para el despegue"
	def aterrizar(self):
		return "Aterrizaremos en 2 horas"
	def combustible (self):
		return "Tenemos combustible para 100.000 km"

class vehiculo_espacial (vehiculo_aereo):
	def __init__ (self,modelo,c_motor,n_ejes,n_alas,n_alerones,n_cohetes):
		vehiculo_aereo.__init__(self,modelo,c_motor,n_ejes,n_alas,n_alerones)
		self.n_cohetes=n_cohetes
	def especificaciones(self):
		print "Se ha registrado un vehiculo"
		print"---------------------------------------"
		return "El vehiculo espacial tiene: "+str(self.n_alas)+" "+"alas"+" , "+str(self.n_alerones)+" alerones"+", "+str(self.n_cohetes) +" Cohetes"
	def despegar (self):
		return "Estamos listos para el despegue"
	def aterrizar(self):
		return "Aterrizaremos en 10 meses"
	def combustible (self):
		return "Tenemos combustible para ir a marte mas no para volver"
#----------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------Logica Del Programa-------------------------------------------------------------------#

#Introducir archivo en la linea de comandos
archivo_vehiculo = sys.argv[1]

#Variable que almacena las lineas del archivo y su contenido como tal
lineas_archivo_vehiculo = tuple(leer_lineas_archivo(archivo_vehiculo))

#Variable que almacena el numero de lineas de archivo
numero_lineas_vehiculo = len(leer_lineas_archivo(archivo_vehiculo))

# Array que contendran la informacion de las caracteristicas del vehiculo
# Se crea array caracteristicas con dimensiones 2 columnas y tantas filas como caracteristicas o numero de lineas en el archivo de vehiculoX.txt
# caracteristica[indice][0] -> Caracteristica del vehiculo
# caracteristica[indice][1] -> Valor Caracteristica
caracteristicas_vehiculo = [[columnas for columnas in range(2)] for filas in range(numero_lineas_vehiculo)]

# Almacenar informacion de las caracteristicas del vehiculo en array caracteristicas
for x in range (0,numero_lineas_vehiculo):
	linea_guardada = save_info(lineas_archivo_vehiculo[x], x+1)
	
	caracteristicas_vehiculo[x][0] = linea_guardada[0]
	caracteristicas_vehiculo[x][1] = linea_guardada[1]


	
#Variable que almacena el tipo de vehiculo

tipo_n = str(caracteristicas_vehiculo[0][1])
tipo = tipo_n.replace("\n","")

#Variables que almacenan informacion que sera heredada
modelo_n = str(caracteristicas_vehiculo[1][1])
modelo = modelo_n.replace('\n', ' ' )

c_motor = int(caracteristicas_vehiculo[2][1])
n_ejes = int(caracteristicas_vehiculo[3][1])

#Si el tipo de vehiculo es vehiculo
if (tipo == "vehiculo"):
	print "\n---------El vehiculo es de tipo: Vehiculo---------\n" 
	v1 = vehiculo (modelo,c_motor,n_ejes)
	print v1.mostrar_detalles() + "\n"
	print v1.arrancar() + "\n"
	print v1.apagar()

#Si el tipo de vehiculo es aereo, heredara caracteristicas de vehiculo.	
if (tipo == "vehiculo_aereo"):
	print "\n-------El vehiculo es de tipo: Aereo---------\n" 
	
	n_alas = int(caracteristicas_vehiculo[4][1])
	n_alerones = int(caracteristicas_vehiculo[5][1])
	v1 = vehiculo(modelo,c_motor,n_ejes)
	va1 = vehiculo_aereo(v1.modelo,v1.c_motor,v1.n_ejes, n_alas,n_alerones)
	
	print va1.especificaciones() + '\n'
	print va1.despegar() + '\n'
	print va1.aterrizar() + '\n'
	print va1.combustible() + '\n'

#Si el tipo de vehiuclo es espacial, heredara caracteristicas de vehiculo aereo y de vehiculo.
if (tipo == "vehiculo_espacial"):
	print "\n---------El vehiculo es de tipo: Espacial---------\n"
	
	n_alas = int(caracteristicas_vehiculo[4][1])
	n_alerones = int(caracteristicas_vehiculo[5][1])
	n_cohetes = int(caracteristicas_vehiculo[6][1])

	v1 = vehiculo(modelo,c_motor,n_ejes)
	va1 = vehiculo_aereo(v1.modelo,v1.c_motor,v1.n_ejes, n_alas,n_alerones)
	ve1 = vehiculo_espacial(v1.modelo,v1.c_motor,v1.n_ejes,va1.n_alas,va1.n_alerones,n_cohetes)
	print ve1.especificaciones() + '\n'
	print ve1.despegar() + '\n'
	print ve1.aterrizar() + '\n'
	print ve1.combustible() + '\n'
