#Programa para el cáculo del costo de un empleado para una empresa.
#Creado por Juan Camilo López Yusty
#20 Agosto 2015

print "\n		Calculadora de costos de un empleado.\n"
while True:#Ingreso de la variable salario
	try:
		salario = int(raw_input('Ingrese el salario que desea liquidar: '))
		break
	except ValueError:
		print("\nIngreso mal el salario.\nPor favor ingrese un valor numerico sin comas o letras.\n")

while True: #Ingreso de la variabe 
	print "\n Le proporciona auxilio de transporte."
	transporte= raw_input("Ingrese si o no, 1 o 2, s o n segun corresponda: \n	")
	if transporte == "1" or transporte == "S" or transporte == "s" or transporte == "si":
		auxtransporte = int(74000)
		saltotal = auxtransporte+salario
		break
	elif transporte== "2" or transporte == "N" or transporte == "n" or transporte == "no":
		auxtransporte = int(0)
		saltotal = auxtransporte+salario
		break
	else:
		print "\nEl valor ingresado fue incorrecto. \nIngrese 1 o 2, segun corresponda su categoria."

while True:
	print "\n Le proporciona ARP (Administradora de Riesgos Profesionales)"
	validarp= raw_input("Ingrese si o no, 1 o 2, s o n segun corresponda: \n	")
	if validarp == "1" or validarp == "S" or validarp == "s" or validarp == "si":
		arp=salario*0.0052
		break
	elif validarp== "2" or validarp == "N" or validarp == "n" or validarp == "no":
		arp=0
		break
	else:
		print "\nEl valor ingresado fue incorrecto. \nIngrese 1 o 2, segun corresponda su categoria."

#Codigo para la mascara del salario, para que salga por ejemplo: $ xx,xxx
from decimal import *# Inicio

def moneyfmt(value, places=2, curr='', sep=',', dp='.', pos='', neg='-', trailneg=''):
	q = Decimal(10) ** -places      # 2 places --> '0.01'
	sign, digits, exp = value.quantize(q).as_tuple()
	result = []
	digits = list(map(str, digits))
	build, next = result.append, digits.pop
	if sign:
		build(trailneg)
	for i in range(places):
		build(next() if digits else '0')
	if places:
		build(dp)
	if not digits:
		build('0')
	i = 0
	while digits:
		build(next())
		i += 1
		if i == 3 and digits:
			i = 0
			build(sep)
	build(curr)
	build(neg if sign else pos)
	return ''.join(reversed(result))
#Fin del codigo de mascara

#Prestaciones sociales que paga la empresa
cesantias,prima,vacaciones=saltotal*0.0833,saltotal*0.0833,salario*0.0417
interescesan=cesantias*0.01
prestaciones_sociales = cesantias + prima + vacaciones + interescesan

#Parafiscales que paga la empresa
cajacompensacion=salario*0.04

#Seguridad social que paga la empresa
pension,salud=salario*0.12,salario*0.085
seguridad_social = pension + salud

#Prestaciones y deduccion que pagan el empleado
salud_empleado,pension_empleado,icbf_emp,sena_emp = salario * 0.04,salario * 0.04,salario*0.03,salario*0.02
prestad = salud_empleado + pension_empleado + icbf_emp + sena_emp
libre_empleado = salario - prestad

#Valor total que paga la empresa
vlrtotal = saltotal+prestaciones_sociales+cajacompensacion+seguridad_social+arp

a=moneyfmt(Decimal(vlrtotal),2,"$",",")#Codig para convertir el salario en formato de moneda
b=moneyfmt(Decimal(libre_empleado),2,"$",",")#Codig para convertir el salario en formato de moneda

print "\n\nAl empleado le queda un salario neto de:", "\n	", b

print "\n\nLa empresa debe pagar por los servicios del empleado un total de:","\n	",a