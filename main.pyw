# -*- coding: utf-8 -*-

import pygame
import pygame.gfxdraw
from pygame.locals import *
import math

from funciones import *
from clases import *

#CONSTANTES

ANCHO_VENTANA = 400
ALTO_VENTANA = 400

MARCO = 5

RADIO_BOLA_PJ = 10

VELOCIDADE_PJ = 1
VELOCIDADE_PROYECTIL = 5

lista_proyectiles = []

punto_pj = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)
punto_futuro = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)
	
bola_pj = circulo(punto_pj,RADIO_BOLA_PJ)

bola_futuro = circulo(punto_futuro,RADIO_BOLA_PJ)

#INICIAR PYGAME

pygame.init()

#LISTA DE OBJETOS COLISIONABLES

obj1 = pygame.Rect(int(ANCHO_VENTANA/5),int(ALTO_VENTANA/5),50,50)
obj2 = pygame.Rect(int(ANCHO_VENTANA/1.3),int(ALTO_VENTANA/3),60,30)
obj3 = pygame.Rect(int(ANCHO_VENTANA/1.4),int(ALTO_VENTANA/1.5),30,70)

lista_obj = [obj1,obj2,obj3]
			
#PANTALLA

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

rect_pantalla = pygame.Rect(MARCO,MARCO,ANCHO_VENTANA-(MARCO*2),ALTO_VENTANA-(MARCO*2))

ON = True

#BUCLE

while ON:
	
	reloj = pygame.time.Clock()

	ventana.fill([0,0,0])
	
	#MOVEMENTO
	
		#PJ
	
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
			
		#PROYECTILES
		
		#BORRADO DE PROYECTILES
		
	lista_proyectiles = borrado_proyectiles(lista_proyectiles,ANCHO_VENTANA,ALTO_VENTANA)
	
		#MOV
		
	for i in range(len(lista_proyectiles)):
		lista_proyectiles[i][0].punto += lista_proyectiles[i][1]
		
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
	
	pygame.gfxdraw.aacircle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [50,50,200])
	pygame.gfxdraw.filled_circle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [50,50,200])
	pygame.gfxdraw.aacircle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [0,0,0])
	
		#RECTANGULOS COLISIONABLES
		
	for i in lista_obj:
		pygame.draw.rect(ventana,[150,50,20],i)
		pygame.draw.rect(ventana,[0,0,0],i,3)
		
		#PROYECTILES
	
	for i in lista_proyectiles:
		pygame.gfxdraw.aacircle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [255,0,0])
		pygame.gfxdraw.filled_circle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [255,0,0])
	
	#MOUSE
	
	pos_mouse = pygame.mouse.get_pos()
	punto_mouse = punto(pos_mouse[0],pos_mouse[1])

	#LASER
	
	if not (bola_pj.punto.x == punto_mouse.x and bola_pj.punto.y == punto_mouse.y):
	#	pygame.draw.aaline(ventana, [255,0,0], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2),  punto_fora(bola_pj.punto,punto_mouse))
		pygame.draw.aaline(ventana, [0,0,0], [bola_pj.punto.x,bola_pj.punto.y], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2))
	
	#ACTUALIZAR PANTALLA
		
	pygame.display.update()
	
	#EVENTOS
	
	for e in pygame.event.get():
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE and not (bola_pj.punto.x == punto_mouse.x and bola_pj.punto.y == punto_mouse.y):
				v = punto_mouse - bola_pj.punto
				lista_proyectiles.append([circulo(punto_corte(bola_pj.punto,punto_mouse,bola_pj.radio*2,p=True),bola_pj.radio/3),v * VELOCIDADE_PROYECTIL / v.longitude()])
		if e.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
	
	reloj.tick(120)
	

