from random import random, uniform
from vector import *
from math import pi
from timeMultiplier import *
from graphics import *
import time

class Roomba:

	def __init__(self, pos, vel, rCircle, rLine, boardTime):
		self.pos = pos
		self.vel = vel
		self.turning = False
		self.turningTime = 0.0
		
		self.size = 20
		self.circle = rCircle
		self.velVect = rLine
		self.d = 0
		self.boardTime = boardTime
		self.lastAngle = self.boardTime.getTime()
		self.lastTurn = self.boardTime.getTime()
		self.lastTime = self.boardTime.getTime()
		

	def death(self):
		if self.pos.y <= 25 or self.pos.y >= 625 or self.pos.x <= 25 or self.pos.x >= 625:
			self.d = 1
			print "DEAD ROOMBA"


	def step(self):
	#	print 'Time'
	#	print self.boardTime.getTime() - self.lastAngle
	#	print self.boardTime.getTime() - self.lastTurn
		#print self.boardTime.getTime()

		self.death()

		if self.boardTime.getTime() - self.lastAngle >= 5:
			noise = uniform(-pi/9, pi/9)
			self.vel.update_angle(noise)
			#self.turningTime += 0.1

			self.lastAngle = self.boardTime.getTime()
		if self.boardTime.getTime() - self.lastTurn >= 20:
			self.flip()
			self.lastTurn = self.boardTime.getTime()

		timeInterval = self.boardTime.getTime()-self.lastTime
		self.lastTime = self.boardTime.getTime()
		if self.turningTime > 0:
			self.turningTime -= timeInterval
			if self.turningTime < 0:
				timeInterval += self.turningTime
				self.turningTime = 0
			self.vel.update_angle(timeInterval*pi/2)
			self.turning = True
		else:
			self.pos.add(Vector(timeInterval*self.vel.x*30, timeInterval*self.vel.y*30,0))
			self.turning = False
		

		self.circle.updatePosition(self.pos)
		self.velVect.updatePosition(self.pos, self.vel)

	def turn(self):
		#self.vel.update_angle(pi/4)
		if self.turning == False:
			self.turningTime += .5
			if self.turningTime > 4:
				self.turningTime = 4

	def flip(self):
		#self.vel.update_angle(pi)
		self.turningTime += 2
		if self.turningTime > 4:
			self.turningTime = 4

