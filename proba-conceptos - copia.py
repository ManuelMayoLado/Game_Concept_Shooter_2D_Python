# -*- coding: utf-8 -*-

import pygame
import pygame.gfxdraw
from pygame.locals import *
import math

#CONSTANTES

ANCHO_VENTANA = 400
ALTO_VENTANA = 400

MARCO = 5

RADIO_BOLA_PJ = 10

VELOCIDADE_PJ = 1

#CREAR CLASES

class punto:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __add__(self,other):
		return punto(self.x + other.x, self.y + other.y)
	def __neg__(self):
		return punto(-self.x,-self.y)
	def __sub__(self,other):
		return self + (-other)
	def longitude(self):
		return math.sqrt(self.x**2 + self.y**2)
	def __mul__(self,n):
		return punto(self.x*n,self.y*n)
	def __div__(self,n):
		return punto(self.x/n,self.y/n)
	__truediv__ = __div__
		
punto_pj = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)
punto_futuro = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)

class circulo:
	def __init__(self,punto,radio):
		self.punto = punto
		self.radio = radio
	
bola_pj = circulo(punto_pj,RADIO_BOLA_PJ)

bola_futuro = circulo(punto_futuro,RADIO_BOLA_PJ)

#INICIAR PYGAME

pygame.init()

#LISTA DE OBJETOS COLISIONABLES

obj1 = pygame.Rect(int(ANCHO_VENTANA/5),int(ALTO_VENTANA/5),50,50)
obj2 = pygame.Rect(int(ANCHO_VENTANA/1.3),int(ALTO_VENTANA/3),60,30)
obj3 = pygame.Rect(int(ANCHO_VENTANA/1.4),int(ALTO_VENTANA/1.5),30,70)

lista_obj = [obj1,obj2,obj3]

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
		return False
		
	#Y-INTERSECTO
	
def y_intersecto(p1,p2):
	return p1.y - (pendiente(p1,p2)*p1.x)
	
	#PUNTO INTERSECCION CIRCUNFERENCIA
	
def punto_corte(p1,p2,radio):
	v = (p2-p1)
	punto = p1 + v * radio / v.longitude()
	return [punto.x,punto.y]
	
	#PUNTO FORA PARA LASER
	
def punto_fora(p1,p2):
	if p2.x < p1.x:
		py = pendiente(p1,p2)*MARCO + y_intersecto(p1,p2)
		px = MARCO
		return [px,py]
	elif p2.x > p1.x:
		py = pendiente(p1,p2)*ANCHO_VENTANA-MARCO + y_intersecto(p1,p2)
		px = ANCHO_VENTANA-MARCO
		return [px,py]
	elif p2.y > p1.y:
		return [p1.x,ALTO_VENTANA-MARCO]
	else:
		return [p1.x,MARCO]
	
	
	#if p2.x < p1.x:
	#	return [MARCO,y_intersecto(p1,p2)+MARCO]
	#elif p2.x > p1.x:
	#	return [ANCHO_VENTANA-MARCO,-y_intersecto(p1,p2)]
	

#PANTALLA

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

rect_pantalla = pygame.Rect(MARCO,MARCO,ANCHO_VENTANA-(MARCO*2),ALTO_VENTANA-(MARCO*2))

ON = True

#BUCLE

while ON:
	
	reloj = pygame.time.Clock()

	ventana.fill([0,0,0])
	
	#MOVEMENTO
	
	tecla_pulsada = pygame.key.get_pressed()
	
	if tecla_pulsada[K_UP] or tecla_pulsada[K_w]:
		bola_futuro.punto.y -= VELOCIDADE_PJ
	if tecla_pulsada[K_DOWN] or tecla_pulsada[K_s]:
		bola_futuro.punto.y += VELOCIDADE_PJ
	if tecla_pulsada[K_RIGHT] or tecla_pulsada[K_d]:
		bola_futuro.punto.x += VELOCIDADE_PJ
	if tecla_pulsada[K_LEFT] or tecla_pulsada[K_a]:
		bola_futuro.punto.x -= VELOCIDADE_PJ
	
	if colision(bola_futuro,lista_obj):
		if colision(circulo(punto(bola_futuro.punto.x,bola_pj.punto.y),RADIO_BOLA_PJ),lista_obj):
			bola_futuro.punto.x = bola_pj.punto.x
		if colision(circulo(punto(bola_pj.punto.x,bola_futuro.punto.y),RADIO_BOLA_PJ),lista_obj):	
			bola_futuro.punto.y = bola_pj.punto.y
		
	#COLISIONS
		
		#MARCO
		
	if bola_futuro.punto.x >= ANCHO_VENTANA-MARCO-bola_pj.radio:
		bola_futuro.punto.x = ANCHO_VENTANA-MARCO-bola_pj.radio
	if bola_futuro.punto.x <= MARCO+bola_pj.radio:
		bola_futuro.punto.x = MARCO+bola_pj.radio
	if bola_futuro.punto.y >= ALTO_VENTANA-MARCO-bola_pj.radio:
		bola_futuro.punto.y = ALTO_VENTANA-MARCO-bola_pj.radio
	if bola_futuro.punto.y <= MARCO+bola_pj.radio:
		bola_futuro.punto.y = MARCO+bola_pj.radio
		
	bola_pj.punto.x = bola_futuro.punto.x
	bola_pj.punto.y = bola_futuro.punto.y
		
	#DEBUXADO
	
		#RECT PANTALLA
	
	pygame.draw.rect(ventana, [240,240,240], rect_pantalla)
	
		#BOLA_PJ
	
	pygame.gfxdraw.aacircle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [50,50,50])
	pygame.gfxdraw.filled_circle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [50,50,50])
	pygame.gfxdraw.aacircle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [0,0,0])
	
		#RECTANGULOS COLISIONABLES
		
	for i in lista_obj:
		pygame.draw.rect(ventana,[150,50,20],i)
		pygame.draw.rect(ventana,[0,0,0],i,3)
	
	#MOUSE
	
	pos_mouse = pygame.mouse.get_pos()
	punto_mouse = punto(pos_mouse[0],pos_mouse[1])

	if not (bola_pj.punto.x == punto_mouse.x and bola_pj.punto.y == punto_mouse.y):
		pygame.draw.aaline(ventana, [255,0,0], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2),  punto_fora(bola_pj.punto,punto_mouse))
		pygame.draw.aaline(ventana, [0,0,0], [bola_pj.punto.x,bola_pj.punto.y], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2))
	
	#vertical_line = pygame.Surface((1,ALTO_VENTANA),pygame.SRCALPHA)
	#vertical_line.fill([220,0,0,100])
	#ventana.blit(vertical_line, (punto_mouse.x,0))
	
	#horizontal_line = pygame.Surface((ANCHO_VENTANA,1),pygame.SRCALPHA)
	#horizontal_line.fill([220,0,0,100])
	#ventana.blit(horizontal_line, (0,punto_mouse.y))
	
	#ACTUALIZAR PANTALLA
		
	pygame.display.update()
	
	#EVENTOS
	
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
	
	reloj.tick(120)
	

