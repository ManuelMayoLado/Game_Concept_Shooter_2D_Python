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

def colision(circulo,lista):
	lista_r = []
	for r in lista:
		if c_circulo_rect(circulo,r):
			lista_r.append(r)
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
		
def borrado_proyectiles(lista,ancho_v,alto_v):	
	indice = 0
	lista_r = lista
	while indice < (len(lista)):
		if lista[indice][0].punto.x < 0 or lista[indice][0].punto.x > ancho_v or lista[indice][0].punto.y < 0 or lista[indice][0].punto.y > alto_v:
			del lista_r[indice]
		else:
			indice += 1
	return lista_r
