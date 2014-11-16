from random import random, uniform
from vector import *
from math import cos, sin, pi

class Spike:

	def __init__(self, pos, vel, rCircle, phase):
		self.pos = pos
		self.vel = vel
		self.size = 9
		self.r = 150
		self.circle = rCircle
		self.spike = 1
		self.phase = phase
		self.count = 2 * pi * 1 / (self.vel.magnitude()/self.r) # count = 2pi/omega
		self.t = 0

	def step(self):
		omega = self.vel.magnitude()/self.r
		#print omega
		#print self.count

		dx = self.r * omega * -sin(omega*self.t + self.phase * pi/2)
		dy = self.r * omega * cos(omega*self.t + self.phase * pi/2)
		if self.t >= self.count:
			self.t = 0
		else:
			self.vel.x = dx
			self.vel.y = dy
			self.pos.add(Vector(dx, dy, 0))
			self.t = self.t + 1
