from random import random, uniform
from vector import *
from math import cos, sin, pi
import time

class Spike:

	def __init__(self, pos, vel, rCircle, phase,boardTime):
		self.pos = pos
		self.vel = vel
		self.size = 9
		self.r = 5
		self.circle = rCircle
		self.phase = phase
		self.boardTime = boardTime

		self.circum = self.r*2*pi
		self.period = self.circum/vel.magnitude()

		self.lastTime = self.boardTime.getTime()

	def death(self):
		if self.pos.y <= 25 or self.pos.y >= 625 or self.pos.x <= 25 or self.pos.x >= 625:
			self.d = 1


	def step(self):
		timeInterval = self.boardTime.getTime()-self.lastTime
		self.lastTime = self.boardTime.getTime()
		fraction = timeInterval/self.period
		
		self.vel.update_angle(fraction*2*pi)
		
		self.pos.add(Vector(timeInterval*self.vel.x*30, timeInterval*self.vel.y*30,0))
		self.circle.updatePosition(self.pos)