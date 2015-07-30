# -*- coding: utf-8 -*-

import math

#CLASES

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
	def distancia(self,other):
		return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
	def __mul__(self,n):
		return punto(self.x*n,self.y*n)
	def __div__(self,n):
		if n != 0:
			return punto(self.x/n,self.y/n)
		else:
			return punto(self.x/0.00001,self.y/0.00001)
	def __getitem__(self,n):
		if n == 0:
			return self.x
		elif n == 1:
			return self.y
		else:
			raise IndexError(n)
	__truediv__ = __div__
	
class circulo:
	def __init__(self,punto,radio):
		self.punto = punto
		self.radio = radio