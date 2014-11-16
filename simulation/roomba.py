from random import random, uniform
from vector import *
from math import pi
from timeMultiplier import *
import time

class Roomba:

	def __init__(self, pos, vel, rCircle, boardTime):
		self.pos = pos
		self.vel = vel
		self.turning = False
		self.turningTime = 0
		
		self.size = 9
		self.circle = rCircle
		self.d = 0
		self.boardTime = boardTime
		self.lastAngle = self.boardTime.getTime()
		self.lastTurn = self.boardTime.getTime()
		self.lastTime = self.boardTime.getTime()
		

	def death(self):
		if self.pos.y <= 25 or self.pos.y >= 625 or self.pos.x <= 25 or self.pos.x >= 625:
			self.d = 1
			print "DEAD"



	def step(self):
	#	print 'Time'
	#	print self.boardTime.getTime() - self.lastAngle
	#	print self.boardTime.getTime() - self.lastTurn
		print self.boardTime.getTime()

		self.death()

		if self.boardTime.getTime() - self.lastAngle >= 5:
			noise = uniform(-pi/9, pi/9)
			self.vel.update_angle(noise)
			self.lastAngle = self.boardTime.getTime()
		if self.boardTime.getTime() - self.lastTurn >= 20:
			self.flip()
			self.lastTurn = self.boardTime.getTime()

		timeInterval = self.boardTime.getTime()-self.lastTime
		self.lastTime = self.boardTime.getTime()
		if self.turning == True:
			self.turningTime -= timeInterval
			if self.turningTime < 0:
				self.turning = False
		else:
			self.pos.add(Vector(timeInterval*self.vel.x*30, timeInterval*self.vel.y*30,0))


		self.circle.updatePosition(self.pos)


	def turn(self):
		self.vel.update_angle(pi/4)
		#self.turning = True
		self.turningTime += 1.0

	def flip(self):
		self.vel.update_angle(pi)
		#self.turning = True
		self.turningTime += 3.5

