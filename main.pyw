# -*- coding: utf-8 -*-

import pygame
import pygame.gfxdraw
from pygame.locals import *
import math
import random

from funciones import *
from clases import *

#CONSTANTES

ANCHO_VENTANA = 450
ALTO_VENTANA = 450

MARCO_INICIAL = 0
MARCO = MARCO_INICIAL

RADIO_BOLA_PJ = 10
RADIO_PROYECTILES = RADIO_BOLA_PJ/5

VELOCIDADE_PJ = 2
VELOCIDADE_PROYECTIL = 10

lista_proyectiles = []
lista_explosions = []
lista_enemigos = []
lista_enemigos_despistados = []
lista_sangre = []

temporizador_enemigos = 80

rango_temp_min = 40
rango_temp_max = 100

VELOCIDADE_ENEMIGOS = 2.5

tempo_recarga = 0

punto_pj = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)
punto_futuro = punto(ANCHO_VENTANA/2 + MARCO, ALTO_VENTANA/2 + MARCO)
	
bola_pj = circulo(punto_pj,RADIO_BOLA_PJ)

bola_futuro = circulo(punto_futuro,RADIO_BOLA_PJ)

#INICIAR PYGAME

pygame.init()

#LISTA DE OBJETOS COLISIONABLES       random.randint(0, ALTO_VENTANA)

obj1 = pygame.Rect(int(ANCHO_VENTANA/4.5),int(ALTO_VENTANA/5),70,40)
obj2 = pygame.Rect(int(ANCHO_VENTANA/1.3),int(ALTO_VENTANA/3),65,35)
obj3 = pygame.Rect(int(ANCHO_VENTANA/1.4),int(ALTO_VENTANA/1.5),35,75)
obj4 = pygame.Rect(int(ANCHO_VENTANA/5),int(ALTO_VENTANA/1.2),60,40)

lista_obj = [obj1,obj2,obj3,obj4]
			
#PANTALLA

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Conceptos")

game_over = False

#FONTES DE TEXTO

font_punt = pygame.font.SysFont("System", ANCHO_VENTANA/20)
font_over = pygame.font.SysFont("System", ANCHO_VENTANA/10)

tamanho_texto_time = 0

puntuacion = 0
time_dec = -1
time_seg = 0

time_reducir_bloques = 0

ON = True

#BUCLE ------------------------------------ XOGO

while ON:

	rect_pantalla = pygame.Rect(int(MARCO),int(MARCO),ANCHO_VENTANA-(int(MARCO)*2),ALTO_VENTANA-(int(MARCO)*2))

	if not game_over:
		time_dec += 1
		if time_dec == 60:
			time_dec = 0
			time_seg += 1
	
	reloj = pygame.time.Clock()


	ventana.fill([0,0,0])
	
	#TEMPORIZADORES
	
	if tempo_recarga > 0:
		tempo_recarga -= 1
		
	if temporizador_enemigos > 0:
		temporizador_enemigos -= 1
		
	#CREACION DE ENEMIGOS

	if temporizador_enemigos == 0 and len(lista_enemigos) < 15:
		numero_random = random.randint(0,3)
		if numero_random == 0:
			lista_enemigos.append(circulo(punto(random.randint(0, ANCHO_VENTANA),ALTO_VENTANA+RADIO_BOLA_PJ),RADIO_BOLA_PJ))
		if numero_random == 1:
			lista_enemigos.append(circulo(punto(random.randint(0, ANCHO_VENTANA),-RADIO_BOLA_PJ),RADIO_BOLA_PJ))
		if numero_random == 2:
			lista_enemigos.append(circulo(punto(-RADIO_BOLA_PJ,random.randint(0, ALTO_VENTANA)),RADIO_BOLA_PJ))
		if numero_random == 3:
			lista_enemigos.append(circulo(punto(ANCHO_VENTANA+RADIO_BOLA_PJ,random.randint(0, ALTO_VENTANA)),RADIO_BOLA_PJ))
		temporizador_enemigos = random.randint(int(rango_temp_min), int(rango_temp_max))
		
	if rango_temp_max > 10:
		rango_temp_max -= 0.01
		
	if rango_temp_min > 5:
		rango_temp_min -= 0.01
	
	#MOUSE
	
	pos_mouse = pygame.mouse.get_pos()
	punto_mouse = punto(pos_mouse[0],pos_mouse[1])
	
	#MOVEMENTO MARCO E RECTANGULOS
	
	'''
	if not game_over and MARCO < 30:
		MARCO += 0.01
	
	time_reducir_bloques += 1
	
	if not game_over and time_reducir_bloques >= 150:
		for i in lista_obj:
			i.left += 1
			i.top += 1
			i.height -= 1
			i.width -= 1
		time_reducir_bloques = 0 #/
	

	lista_obj_ant = lista_obj[:]
	
	for i in range(len(lista_obj)):
		if lista_obj_ant[i].height <= 0 or lista_obj_ant[i].width <= 0:
			lista_obj.remove(lista_obj_ant[i])
	'''
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
			
		#MOVEMENTO PROYECTILES
		
	for i in range(len(lista_proyectiles)):
		lista_proyectiles[i][0].punto += lista_proyectiles[i][1]
		
		#MOVEMENTO ENEMIGOS
	
	lista_enemigos_gardada = []
	
	for i in lista_enemigos:
		lista_enemigos_gardada.append(circulo(punto(i.punto.x,i.punto.y),i.radio))
	
	for i in lista_enemigos:
		v = (bola_pj.punto - i.punto)
		i.punto = i.punto + v * VELOCIDADE_ENEMIGOS / v.longitude()
			
	#MOVEMENTO ERRATICO DOS ENEMIGOS
	
	for i in range(len(lista_enemigos)):
		if i in lista_enemigos_despistados:
			v = (punto(random.randint(MARCO,ANCHO_VENTANA-MARCO),random.randint(MARCO,ALTO_VENTANA-MARCO)) - lista_enemigos[i].punto)
			lista_enemigos[i].punto = lista_enemigos[i].punto + v * VELOCIDADE_ENEMIGOS / v.longitude()

		#COLISIONS ENTRE ENEMIGOS
	
	for i in range(len(lista_enemigos)):
		lista_enemigos_colisionable = lista_enemigos[:]
		lista_enemigos_colisionable.remove(lista_enemigos[i])
		if colision(lista_enemigos[i],lista_obj) or colision(lista_enemigos[i],lista_enemigos_colisionable,c=True):
			circulo_enemigo_cam_x = circulo(punto(lista_enemigos[i].punto.x,lista_enemigos_gardada[i].punto.y),lista_enemigos[i].radio)
			if colision(circulo_enemigo_cam_x,lista_obj) or colision(circulo_enemigo_cam_x,lista_enemigos_colisionable,c=True):
				lista_enemigos[i].punto.x = lista_enemigos_gardada[i].punto.x
			circulo_enemigo_cam_y = circulo(punto(lista_enemigos_gardada[i].punto.x,lista_enemigos[i].punto.y),lista_enemigos[i].radio)
			if colision(circulo_enemigo_cam_y,lista_obj) or colision(circulo_enemigo_cam_y,lista_enemigos_colisionable,c=True):
				lista_enemigos[i].punto.y = lista_enemigos_gardada[i].punto.y
			
		#LISTA PARA MOVEMENTO ERRATICO
		
	lista_enemigos_despistados = []
		
	for i in range(len(lista_enemigos)):
		if lista_enemigos[i].punto.distancia(lista_enemigos_gardada[i].punto) < 0.1:
			lista_enemigos_despistados.append(i)
		
				
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
	
	'''
	if colision(bola_pj,lista_obj):
		if not colision(circulo(punto(bola_pj.punto.x + 1,bola_pj.punto.y),bola_pj.radio),lista_obj):
			bola_pj.punto.x += 1
		if not colision(circulo(punto(bola_pj.punto.x - 1,bola_pj.punto.y),bola_pj.radio),lista_obj):
			bola_pj.punto.x -= 1
		if not colision(circulo(punto(bola_pj.punto.x,bola_pj.punto.y + 1),bola_pj.radio),lista_obj):
			bola_pj.punto.x += 1
		if not colision(circulo(punto(bola_pj.punto.x,bola_pj.punto.y - 1),bola_pj.radio),lista_obj):
			bola_pj.punto.x -= 1
	'''
	
		#BALA CONTRA ENEMIGOS

	for i in lista_proyectiles+lista_explosions:
		lista_col = colision(i[0],lista_enemigos,c=True)
		if lista_col:
			for x in lista_col:
				#lista_sangre.append(x)
				puntuacion += 10
				lista_enemigos.remove(x)
				
		#ENEMIGOS CONTRA PJ
		
	if colision(bola_pj,lista_enemigos,c=True):
		game_over = True
		
	#DEBUXADO
	
		#RECT PANTALLA
	
	pygame.draw.rect(ventana, [245,245,245], rect_pantalla)
	
		#SANGRE
		
	for i in lista_sangre:
		pygame.gfxdraw.aacircle(ventana, int(i.punto.x), int(i.punto.y), i.radio, [240,0,0])
		pygame.gfxdraw.filled_circle(ventana, int(i.punto.x), int(i.punto.y), i.radio, [240,0,0])
	
		#RECTANGULOS COLISIONABLES
		
	for i in lista_obj:
		pygame.draw.rect(ventana,[150,50,20],i)
		pygame.draw.rect(ventana,[100,20,0],i,3)
		
		#LASER E CANHON
	
	if not game_over and not (bola_pj.punto.x == punto_mouse.x and bola_pj.punto.y == punto_mouse.y):
		#pygame.draw.aaline(ventana, [255,0,0], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2),  punto_fora(bola_pj.punto,punto_mouse))
		pygame.draw.aaline(ventana, [0,0,0], [bola_pj.punto.x,bola_pj.punto.y], punto_corte(bola_pj.punto,punto_mouse,RADIO_BOLA_PJ*2))
	
		#BOLA_PJ
	
	if not game_over:
		pygame.gfxdraw.aacircle(ventana, int(bola_pj.punto.x), int(bola_pj.punto.y), RADIO_BOLA_PJ, [50,50,150])
		pygame.gfxdraw.filled_circle(ventana, int(bola_pj.punto.x), int(bola_pj.punto.y), RADIO_BOLA_PJ, [50,50,150])
	if game_over:
		pygame.gfxdraw.aacircle(ventana, int(bola_pj.punto.x), int(bola_pj.punto.y), RADIO_BOLA_PJ, [240,0,0])
		pygame.gfxdraw.filled_circle(ventana, int(bola_pj.punto.x), int(bola_pj.punto.y), RADIO_BOLA_PJ, [240,0,0])
		
	#pygame.gfxdraw.aacircle(ventana, int(bola_pj.punto.x), int(bola_pj.punto.y), RADIO_BOLA_PJ, [0,0,0])
	
		#ENEMIGOS
	
	for i in lista_enemigos:
		pygame.gfxdraw.aacircle(ventana, int(i.punto.x), int(i.punto.y), i.radio, [0,80,0])
		pygame.gfxdraw.filled_circle(ventana, int(i.punto.x), int(i.punto.y), i.radio, [0,80,0])
	
		#PROYECTILES
	
	for i in lista_proyectiles:
		pygame.gfxdraw.aacircle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [0,0,255])
		pygame.gfxdraw.filled_circle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [0,0,255])
		
		#PROYECTILES EXPLOTANDO

	for i in lista_explosions:
		i[0].radio = RADIO_PROYECTILES * (abs(15-i[1])+1)/2
		i[1] -= 1
		pygame.gfxdraw.aacircle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [0,0,255])
		if i[1] > 8:
			pygame.gfxdraw.filled_circle(ventana, int(i[0].punto.x), int(i[0].punto.y), i[0].radio, [0,0,0])
			
	#PUNTUACION
	
	if time_seg < 10:
		time_seg_str = "0"+str(time_seg)
	else:
		time_seg_str = str(time_seg)
	
	if time_dec < 10:
		time_dec_str = "0"+str(time_dec)
	else:
		time_dec_str = str(time_dec)
	
	text_punt = font_punt.render(("SCORE: "+str(puntuacion)),True,[0,0,0])
	ventana.blit(text_punt,[MARCO,MARCO])
	text_time = font_punt.render(("TIME: "+time_seg_str+":"+time_dec_str),True,[0,0,0])
	
	if game_over:
		color_over = [random.randint(70,150),random.randint(70,150),random.randint(70,150)]
		text_game_over = font_over.render("GAME OVER", True, color_over)
		ventana.blit(text_game_over,[(ANCHO_VENTANA-MARCO*2)/2-text_game_over.get_width()/2,(ALTO_VENTANA-MARCO*2)/2-text_game_over.get_height()/2])
	
	
	
	if time_dec == 0:
		tamanho_texto_time = text_time.get_width()
	
	ventana.blit(text_time,[ANCHO_VENTANA-(MARCO+tamanho_texto_time),MARCO])
	
	
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
				tempo_recarga = 15
	
	for e in pygame.event.get():
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE and game_over:
				lista_enemigos = []
				temporizador_enemigos = 80
				puntuacion = 0
				time_dec = 0
				time_seg = 0
				rango_temp_min = 40
				rango_temp_max = 100
				game_over = False
		if e.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
	
	reloj.tick(60)
	

