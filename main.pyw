# -*- coding: utf-8 -*-

import pygame
import pygame.gfxdraw
from pygame.locals import *
import math
import random

from funciones import *
from clases import *

#CONSTANTES

ANCHO_VENTANA = 400
ALTO_VENTANA = 400

MARCO = 5

RADIO_BOLA_PJ = 10
RADIO_PROYECTILES = RADIO_BOLA_PJ/5

VELOCIDADE_PJ = 2
VELOCIDADE_PROYECTIL = 10

lista_proyectiles = []
lista_explosions = []
lista_enemigos = []

temporizador_enemigos = 30
VELOCIDADE_ENEMIGOS = 2.5

tempo_recarga = 0

punto_pj = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)
punto_futuro = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)
	
bola_pj = circulo(punto_pj,RADIO_BOLA_PJ)

bola_futuro = circulo(punto_futuro,RADIO_BOLA_PJ)

#INICIAR PYGAME

pygame.init()

#LISTA DE OBJETOS COLISIONABLES

obj1 = pygame.Rect(int(ANCHO_VENTANA/5),int(ALTO_VENTANA/5),50,50)
obj2 = pygame.Rect(int(ANCHO_VENTANA/1.3),int(ALTO_VENTANA/3),65,35)
obj3 = pygame.Rect(int(ANCHO_VENTANA/1.4),int(ALTO_VENTANA/1.5),35,75)

lista_obj = [obj1,obj2,obj3]
			
#PANTALLA

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

rect_pantalla = pygame.Rect(MARCO,MARCO,ANCHO_VENTANA-(MARCO*2),ALTO_VENTANA-(MARCO*2))

game_over = False

ON = True

#BUCLE ------------------------------------ XOGO

while ON:
	
	reloj = pygame.time.Clock()

	if game_over:
		ventana.fill([255,0,0])
	else:
		ventana.fill([0,0,0])
	
	#TEMPORIZADORES
	
	if tempo_recarga > 0:
		tempo_recarga -= 1
		
	if temporizador_enemigos > 0:
		temporizador_enemigos -= 1
		
	#CREACION DE ENEMIGOS
	
	if temporizador_enemigos == 0 and len(lista_enemigos) < 10:
		lista_enemigos.append(circulo(punto(random.randint(0, ANCHO_VENTANA),-RADIO_BOLA_PJ),RADIO_BOLA_PJ))
		temporizador_enemigos = 30

	#MOUSE
	
	pos_mouse = pygame.mouse.get_pos()
	punto_mouse = punto(pos_mouse[0],pos_mouse[1])
	
	#MOVEMENTO
	
		#PJ
	
	tecla_pulsada = pygame.key.get_pressed()
	
	if not game_over:
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
			
		#MOV
		
	for i in range(len(lista_proyectiles)):
		lista_proyectiles[i][0].punto += lista_proyectiles[i][1]
		
		#ENEMIGOS
	
	if not game_over:
		for i in lista_enemigos:
			v = (bola_pj.punto - i.punto)
			i.punto = i.punto + v * VELOCIDADE_ENEMIGOS / v.longitude()
		
		#BORRADO DE PROYECTILES

	lista_explosions = lista_explosions + borrado_proyectiles(lista_proyectiles,lista_obj,lista_enemigos,ANCHO_VENTANA,ALTO_VENTANA,MARCO,RADIO_PROYECTILES)[1]
	
	lista_proyectiles = borrado_proyectiles(lista_proyectiles,lista_obj,lista_enemigos,ANCHO_VENTANA,ALTO_VENTANA,MARCO,RADIO_PROYECTILES)[0]
		
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
	
		#BALA CONTRA ENEMIGOS

	for i in lista_proyectiles+lista_explosions:
		lista_col = colision(i[0],lista_enemigos,c=True)
		if lista_col:
			for x in lista_col:
				lista_enemigos.remove(x)
				
		#ENEMIGOS CONTRA PJ
		
	if colision(bola_pj,lista_enemigos,c=True):
		game_over = True
		
	#DEBUXADO
	
		#RECT PANTALLA
	
	pygame.draw.rect(ventana, [245,245,245], rect_pantalla)
	
		#RECTANGULOS COLISIONABLES
		
	for i in lista_obj:
		pygame.draw.rect(ventana,[150,50,20],i)
		pygame.draw.rect(ventana,[0,0,0],i,3)
		
		#ENEMIGOS
		
	for i in lista_enemigos:
		pygame.gfxdraw.aacircle(ventana, int(i.punto.x), int(i.punto.y), i.radio, [0,0,0])
		pygame.gfxdraw.filled_circle(ventana, int(i.punto.x), int(i.punto.y), i.radio, [0,0,0])
		
		#LASER E CANHON
	
	if not (bola_pj.punto.x == punto_mouse.x and bola_pj.punto.y == punto_mouse.y):
		#pygame.draw.aaline(ventana, [255,0,0], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2),  punto_fora(bola_pj.punto,punto_mouse))
		pygame.draw.aaline(ventana, [0,0,0], [bola_pj.punto.x,bola_pj.punto.y], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2))
	
		#BOLA_PJ
	
	pygame.gfxdraw.aacircle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [50,50,150])
	pygame.gfxdraw.filled_circle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [50,50,150])
	pygame.gfxdraw.aacircle(ventana, bola_pj.punto.x, bola_pj.punto.y, RADIO_BOLA_PJ, [0,0,0])
		
		#PROYECTILES
	
	for i in lista_proyectiles:
		pygame.gfxdraw.aacircle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [0,0,255])
		pygame.gfxdraw.filled_circle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [0,0,255])
		
		#PROYECTILES EXPLOTANDO

	for i in lista_explosions:
		radio = i[0].radio * (abs(15-i[1])+1)/2
		i[1] -= 1
		pygame.gfxdraw.aacircle(ventana, int(i[0].punto.x), int(i[0].punto.y), radio, [0,0,255])
		if i[1] > 8:
			pygame.gfxdraw.filled_circle(ventana, int(i[0].punto.x), int(i[0].punto.y), radio, [0,0,0])
			
	for i in range(len(lista_explosions)):
		if lista_explosions[i][1] <= 0:
			lista_explosions[i]='eliminar'
	
	while 'eliminar' in lista_explosions:
		lista_explosions.remove('eliminar')

	
	#ACTUALIZAR PANTALLA
		
	pygame.display.update()
	
	#EVENTOS
	
	if pygame.mouse.get_pressed()[0] == 1 and not (bola_pj.punto.x == punto_mouse.x and bola_pj.punto.y == punto_mouse.y) and tempo_recarga == 0 and not game_over:
				v = punto_mouse - bola_pj.punto
				lista_proyectiles.append([circulo(punto_corte(bola_pj.punto,punto_mouse,bola_pj.radio*2,p=True),RADIO_PROYECTILES),v * VELOCIDADE_PROYECTIL / v.longitude()])
				tempo_recarga = 10
	
	for e in pygame.event.get():
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE and game_over:
				lista_enemigos = []
				game_over = False
		if e.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
	
	reloj.tick(60)
	

