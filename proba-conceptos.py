# -*- coding: utf-8 -*-

import pygame
import pygame.gfxdraw
from pygame.locals import *

#CONSTANTES

ANCHO_VENTANA = 500
ALTO_VENTANA = 500

MARCO = 5

RADIO_BOLA_PJ = 12

VELOCIDADE_PJ = 3

#CREAR CLASES

class punto:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
punto_pj = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)

#INICIAR PYGAME

pygame.init()

#LISTA DE OBJETOS COLISIONABLES

obj1 = pygame.Rect(int(ANCHO_VENTANA/5),int(ALTO_VENTANA/5),50,50)
obj2 = pygame.Rect(int(ANCHO_VENTANA/1.3),int(ALTO_VENTANA/3),60,30)
obj3 = pygame.Rect(int(ANCHO_VENTANA/1.5),int(ALTO_VENTANA/1.3),30,70)

lista_obj = [obj1,obj2,obj3]

#FUNCION PARA COLISIONS COS OBJETOS

def colision():
	for r in lista_obj:
		if punto_pj.x+RADIO_BOLA_PJ > r.left and punto_pj.x-RADIO_BOLA_PJ < r.left+r.width and punto_pj.y+RADIO_BOLA_PJ > r.top and punto_pj.y-RADIO_BOLA_PJ < r.top+r.height:
			lista = []
			if punto_pj.x < r.left:
				lista.append("esquerda")
			if punto_pj.x > r.left + r.width:
				lista.append("dereita")
			if punto_pj.y < r.top:
				lista.append("arriba")
			if punto_pj.y > r.top + r.height:
				lista.append("abaixo")
			lista.insert(0,r)
			return lista
	return False
	
#FUNCIONS MATEMATICAS

	#PENDIENTE RECTA
	
def pendiente(p1,p2):
	if p1.x != p2.x:
		return (p2.y - p1.y) / float((p2.x - p1.x))
	else:
		return False
		
	#Y-INTERSECTO
	
def y_intersecto(p1,p2):
	return p1.y - (pendiente(p1,p2)*p1.x)

#PANTALLA

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

rect_pantalla = pygame.Rect(MARCO,MARCO,ANCHO_VENTANA-(MARCO*2),ALTO_VENTANA-(MARCO*2))

ON = True

#BUCLE

while ON:
	
	reloj = pygame.time.Clock()
	
	#DEBUXADO 

	ventana.fill([0,0,0])
	
		#RECT PANTALLA
	
	pygame.draw.rect(ventana, [250,250,250], rect_pantalla)
	
		#BOLA_PJ
	
	pygame.gfxdraw.aacircle(ventana, punto_pj.x, punto_pj.y, RADIO_BOLA_PJ, [0,0,0])
	pygame.gfxdraw.filled_circle(ventana, punto_pj.x, punto_pj.y, RADIO_BOLA_PJ, [0,0,0])
	
		#RECTANGULOS COLISIONABLES
		
	for i in lista_obj:
		pygame.draw.rect(ventana,[100,50,0],i)
	
	#MOVEMENTO
	
	tecla_pulsada = pygame.key.get_pressed()
	
	if tecla_pulsada[K_UP] or tecla_pulsada[K_w]:
		punto_pj.y -= VELOCIDADE_PJ
	elif tecla_pulsada[K_DOWN] or tecla_pulsada[K_s]:
		punto_pj.y += VELOCIDADE_PJ
	if tecla_pulsada[K_RIGHT] or tecla_pulsada[K_d]:
		punto_pj.x += VELOCIDADE_PJ
	elif tecla_pulsada[K_LEFT] or tecla_pulsada[K_a]:
		punto_pj.x -= VELOCIDADE_PJ
		
	#COLISIONS
		
		#MARCO
		
	if punto_pj.x >= ANCHO_VENTANA-MARCO-RADIO_BOLA_PJ:
		punto_pj.x = ANCHO_VENTANA-MARCO-RADIO_BOLA_PJ
	if punto_pj.x <= MARCO+RADIO_BOLA_PJ:
		punto_pj.x = MARCO+RADIO_BOLA_PJ
	if punto_pj.y >= ALTO_VENTANA-MARCO-RADIO_BOLA_PJ:
		punto_pj.y = ALTO_VENTANA-MARCO-RADIO_BOLA_PJ
	if punto_pj.y <= MARCO+RADIO_BOLA_PJ:
		punto_pj.y = MARCO+RADIO_BOLA_PJ
		
		#RECTANGULOS
		
	if colision() and (tecla_pulsada[K_UP] or tecla_pulsada[K_w]) and "abaixo" in colision():
		punto_pj.y = colision()[0].top+colision()[0].height+RADIO_BOLA_PJ
	elif colision() and (tecla_pulsada[K_DOWN] or tecla_pulsada[K_s]) and "arriba" in colision():
		punto_pj.y = colision()[0].top-RADIO_BOLA_PJ
	if colision() and (tecla_pulsada[K_RIGHT] or tecla_pulsada[K_d]) and "esquerda" in colision():
		punto_pj.x = colision()[0].left-RADIO_BOLA_PJ
	elif colision() and (tecla_pulsada[K_LEFT] or tecla_pulsada[K_a]) and "dereita" in colision():
		punto_pj.x = colision()[0].left+colision()[0].width+RADIO_BOLA_PJ
		
	#MOUSE
	
	pos_mouse = pygame.mouse.get_pos()
	punto_mouse = punto(pos_mouse[0],pos_mouse[1])
	
	pygame.draw.aaline(ventana, [0,0,0], [punto_pj.x,punto_pj.y], pos_mouse)
	
	print "pendiente",pendiente(punto_pj,punto_mouse)
	print "y-intersecto",y_intersecto(punto_pj,punto_mouse)

	#ACTUALIZAR PANTALLA
		
	pygame.display.update()
	
	#EVENTOS
	
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
	
	reloj.tick(60)
	

