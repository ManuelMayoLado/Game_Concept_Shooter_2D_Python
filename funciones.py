# -*- coding: utf-8 -*-

#FUNCION PARA COLISIONS COS OBJETOS

def c_circulo_rect(circulo,rectangulo):
	c_distancia_x = abs(circulo.punto.x - rectangulo.left - rectangulo.width/2)
	c_distancia_y = abs(circulo.punto.y - rectangulo.top -  rectangulo.height/2)
	if c_distancia_x > (rectangulo.width/2 + circulo.radio) or c_distancia_y > (rectangulo.height/2 + circulo.radio):
		return False
	if c_distancia_x <= rectangulo.width/2 or c_distancia_y <= rectangulo.height/2:
		return True
	corner_distancia = (c_distancia_x - rectangulo.width/2)**2 + (c_distancia_y - rectangulo.height/2)**2
	return corner_distancia <= circulo.radio**2
	
def c_circulo_cir(circulo1,circulo2):
	return circulo1.radio + circulo2.radio > circulo1.punto.distancia(circulo2.punto)

def colision(circulo,lista,c=False):
	lista_r = []
	for i in lista:
		if not c and c_circulo_rect(circulo,i):
			lista_r.append(i)
		elif c and c_circulo_cir(circulo,i):
			lista_r.append(i)
	return lista_r
	
#FUNCIONS MATEMATICAS

	#PENDIENTE RECTA
	
def pendiente(p1,p2):
	if p1.x != p2.x:
		return (p2.y - p1.y) / float((p2.x - p1.x))
	else:
		return 0
		
	#Y-INTERSECTO
	
def y_intersecto(p1,p2):
	return p1.y - (pendiente(p1,p2)*p1.x)
	
	#PUNTO INTERSECCION CIRCUNFERENCIA
	
def punto_corte(p1,p2,radio,p=False):
	v = (p2-p1)
	punto = p1 + v * radio / v.longitude()
	if not p:
		return [punto.x,punto.y]
	else: 
		return punto
		
def borrado_proyectiles(lista,lista_rec,lista_cir,ancho_v,alto_v,marco,radio):	
	indice = 0
	lista_r = lista
	lista_borrados = []
	while indice < (len(lista)):
		if lista[indice][0].punto.x < marco+radio or lista[indice][0].punto.x > ancho_v-(marco+radio) or lista[indice][0].punto.y < marco+radio or lista[indice][0].punto.y > alto_v-(marco+radio) or colision(lista[indice][0],lista_rec) or colision(lista[indice][0],lista_cir,c=True):
			lista_borrados.append([lista_r[indice][0],15])
			del lista_r[indice]
		else:
			indice += 1
	return [lista_r, lista_borrados]
