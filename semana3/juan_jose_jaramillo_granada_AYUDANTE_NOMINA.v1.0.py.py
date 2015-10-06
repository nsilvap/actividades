# Programa para calcular prestaciones de servicios en Colombia 2015

descuento = 0
descuento_seguridad_social = 0
descuento_parafiscales = 0
descuento_sociales = 0
salario_minimo = 644350
auxilio_transporte = 74000

print ""
print "CALCULADORA DE PRESTACIONES"
print ""
print "Salario Minimo Legal Vigente: $644350\n"
while True:
	try:
		salario = int(raw_input('Ingrese un salario para calcular su descuento de prestaciones: '))
		opcion = int(raw_input('Desea calcular costo total para la empresa(1) o salario neto del empleador(2)?'))
		break
	except ValueError:
		print('------------Intente nuevamente ingresando un caracter valido------------')
print "\n"

avi_prestaciones_seguridad_social= ['Salud(8,5%)','Pension(12%)','ARP(0,52%)']
prestaciones_seguridad_social = [0.085,0.12,0.0052]
avi_prestaciones_parafiscales = ['Cajas de Compensacion Familiar(4%)','ICBF(3%)','Sena(2%)']
prestaciones_parafiscales = [0.04,0.03,0.02]
avi_prestaciones_sociales = ['Prima de Servicios(8.33%)','Cesatias(8.33%)','Intereses sobre Cesantias(1%)','vacaciones(4.17%)']
prestaciones_sociales = [0.0833,0.0833,0.01,0.0417]

if salario >= (2*salario_minimo):
	auxilio_transporte = 0
else:
	auxilio_transporte = auxilio_transporte

print 'Ayudante Nomina v1.0'
	
if opcion == 1:
	print '\nSEGURIDAD SOCIAL\n'
	for i in range(len(prestaciones_seguridad_social)):
		p = salario*prestaciones_seguridad_social[i]
		descuento_seguridad_social = descuento_seguridad_social + p
		print avi_prestaciones_seguridad_social[i], ' = '+str(p)
		descuento = descuento + p
	print '--->Descuento Seguridad Social = $'+str(descuento_seguridad_social)
	print '\nPARAFISCALES\n'
	for i in range(len(prestaciones_parafiscales)):
		p = salario*prestaciones_parafiscales[i]
		print avi_prestaciones_parafiscales[i], ' = '+str(p)
		descuento_parafiscales = descuento_parafiscales + p
		descuento = descuento + p
	print '--->Descuento Parafiscales = $'+str(descuento_parafiscales)
	print '\nPRESTACIONES SOCIALES\n'
	for i in range(len(prestaciones_sociales)):
		if prestaciones_sociales[i]==0.01 and prestaciones_sociales[i-1]==0.0833:
			p = (salario*0.0833)*prestaciones_sociales[i]
		elif prestaciones_sociales[i]==0.0833:
			p = prestaciones_sociales[i]*(salario+auxilio_transporte)
		else:
			p = salario*prestaciones_sociales[i]
		descuento_sociales = descuento_sociales + p
		print avi_prestaciones_sociales[i], ' = '+str(p)
		descuento = descuento + p
	print '--->Descuento Prestaciones Sociales = $'+str(descuento_seguridad_social)
	print '\n\nLas prestaciones de este trabajador cuestan:','$'+str(descuento)
	print 'Salario Base','$'+str(salario)
	print 'Auxilio de Transporte:','$'+str(auxilio_transporte)
	print 'El costo del trabajador es:','$'+str(descuento+salario+auxilio_transporte)+'\n'
else:
	print '\nSalud(4%)'+' = $'+str(salario*0.04)
	print 'Pension(4%)'+' = $'+str(salario*0.04)
	trabajador = salario*(0.08)
	print '\nSalario Base','$'+str(salario)
	print 'Auxilio de Transporte:','$'+str(auxilio_transporte)
	print 'Al empleado le quedan libres: '+'$'+str(auxilio_transporte+salario-trabajador)