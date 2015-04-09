from vector import *
from math import pi, cos, sin, atan2
from timeMultiplier import *
from random import random, randrange
from graphics import Point

class UAV:

    def __init__ (self, pos, vel, rCircle, maxSpeed, boardTime, roombaList, spikeList):
        self.pos = pos
        self.vel = vel
        self.circle = rCircle
        self.maxSpeed = maxSpeed
        self.boardTime = boardTime
        self.d = 0
        self.lastTime = self.boardTime.getTime()

        self.roombaList = roombaList
        self.spikeList = spikeList

        self.targetNum = -1
        self.targetList = [0]
        self.BoardCenter = Point(325.0,200.0)
        
    def death(self):
        if self.pos.y <= 25 or self.pos.y >= 625 or self.pos.x <= 25 or self.pos.x >= 625:
                    self.d = 1
        print "DEAD"

    def update(self, newRoobaList, newSpikeList):
        self.roombaList = newRoobaList
        self.spikeList = newSpikeList

    def step(self):
        self.death()

        # controller (choosing target)
        if self.targetNum != -1 and self.targetNum < len(self.roombaList):
            self.target = self.roombaList[self.targetNum].pos
        else:
            self.target = self.BoardCenter
        
        # plant (motion of quad)
        distanceToTarget = (self.pos.x-self.target.x)**2 + (self.pos.x-self.target.x)**2
        directiontoTarget = Vector(self.target.x-self.pos.x, self.target.y-self.pos.y, 0)
        self.vel = directiontoTarget
        self.vel.scale(self.maxSpeed/(self.vel.magnitude()+.01))



        if distanceToTarget < 8:
        # unresolved: can you turn the roomba if the roomba is currently turning?
        # controller when close to target
            print "distance to target", distanceToTarget
            if self.target !=self.BoardCenter:
                self.roombaList[self.targetNum].turn() 
            if len(self.targetList) > 0:
                self.targetNum = self.targetList.pop(0)
            else:
                #self.targetNum = -1
                self.targetList+=findTarget(self.roombaList)
        
            # plant (motion of quad)
            timeInterval = self.boardTime.getTime()-self.lastTime
            self.lastTime = self.boardTime.getTime()
            #if self.vel.magnitude > self.maxSpeed*30:
            #	self.vel.scale(self.maxSpeed/self.vel.magnitude())
            self.pos.add(Vector(timeInterval*self.vel.x*30, timeInterval*self.vel.y*30,0))
            self.circle.updatePosition(self.pos)

def priority(r):
    return r.pos.y/30 + (r.vel.y/abs(r.vel.x))*20

def sort(roombaList):
    return sorted(roombaList, key = lambda roomba : roomba.pos.y)

def findTarget(roombaList):
    #y = [r.pos.y for r in roombaList]
    #roombaList = [roombaList for (y,roombaList) in sorted(zip(y,roombaList))]
    sortedRoombaList = sort(roombaList)
    # there is now a major bug where UAV struggles to evaluate a currently turning roomba
    for r in sortedRoombaList:
        if -1*r.vel.y <= abs(r.vel.x):
            theta = atan2(-1*r.vel.y, r.vel.x)
            turn = 1
            accountforposition = 0
            if pi/4>theta>0:
                    turn = 7
            if 0>theta> -pi/4:
                    turn = 6
            if -1*pi/4>theta> -1*pi/2:
                    turn = 5
            if -1*pi/2>theta>-3*pi/4:
                    turn = 4
            if -1*3*pi/4>theta> -1*pi:
                    turn = 3
            if pi>theta> 3*pi/4:
                    turn = 2
            if r.pos.x > 450:
                    accountforposition = -1
            if r.pos.x < 200:
                    accountforposition = 1
            return [roombaList.index(r)]*(turn-1+ accountforposition)
    return [-1]
