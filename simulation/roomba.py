from random import random, uniform
from vector import *
from math import pi

class Roomba:

	def __init__(self, pos, vel, rCircle):
		self.pos = pos
		self.vel = vel
		
		self.tick = 20
		self.size = 9
		self.randang = 5
		self.circle = rCircle
		self.d = 0

	def death(self):
		if self.pos.y <= 25 or self.pos.y >= 625 or self.pos.x <= 25 or self.pos.x >= 625:
			self.d = 1
			print "DEAD"
		print self.pos.x, self.pos.y

	def step(self):
		print "roomba vel magnitude:", self.vel.magnitude()
		self.death()
		if self.randang == 0:
			noise = uniform(-pi/18, pi/18)
			self.vel.update_angle(noise)
			self.randang = 5
		elif self.tick == 0:
			self.vel.update_angle(pi)
			self.tick = 20
		else:
			self.pos.add(self.vel)
		self.tick = self.tick - 1
		self.randang = self.randang - 1

