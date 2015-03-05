from vector import *
from math import pi, cos, sin, tan, atan2
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
        self.NeutralTarget = Point(325.0,325.0)   # default to board center
        
    def death(self):
        if self.pos.y <= 25 or self.pos.y >= 625 or self.pos.x <= 25 or self.pos.x >= 625:
        	self.d = 1

    def update(self, newRoobaList, newSpikeList):
        self.roombaList = newRoobaList
        self.spikeList = newSpikeList

    def step(self):
        self.death()

        # controller (choosing target)
        if self.targetNum != -1 and self.targetNum < len(self.roombaList):
            self.target = self.roombaList[self.targetNum].pos
        else:
			xlist = [r.pos.x for r in self.roombaList if not(r.d)]
			ylist = [r.pos.y for r in self.roombaList if not(r.d)]
			avgX = sum(xlist)/len(xlist)
			avgY = sum(ylist)/len(ylist)	
            		self.NeutralTarget = Point(avgX, avgY)
			self.target = self.NeutralTarget
        
        # plant (motion of quad)
        distanceToTarget = (self.pos.x-self.target.x)**2 + (self.pos.x-self.target.x)**2
        directiontoTarget = Vector(self.target.x-self.pos.x, self.target.y-self.pos.y, 0)
        self.vel = directiontoTarget
        self.vel.scale(self.maxSpeed/(self.vel.magnitude()+.01))



        if distanceToTarget < 8:
        # unresolved: can you turn the roomba if the roomba is currently turning?
        # controller when close to target
            print "distance to target", distanceToTarget
            if self.target !=self.NeutralTarget:
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

def angleCost(r):
    actualX = r.pos.x-25
    actualY = r.pos.y-25
    [TL, BL] = [atan2(actualX, actualY) + pi/2, atan2(600-actualY, actualX) + pi]
    [BR, TR] = [atan2(600-actualX, 600-actualY) + 3*pi/2, atan2(actualY, 600-actualX)]
    angle = (atan2(-r.vel.y, r.vel.x) + 2*pi) % 2*pi

    print "TL, BL, BR, TR: ", TL, BL, BR, TR

    print "angle: ", angle
    if TR <= angle < TL:
	C = 10
	return C / (actualY/sin(angle))
    elif TL <= angle < BL:
	C = 10000
	return C / (actualX/abs(cos(angle)))
    elif BL <= angle < BR:
	C = 10000
	return C / ((600-actualY)/abs(sin(angle)))
    elif BL <= angle < 2*pi or 0 <= angle < TR:
	C = 10000
	return C / ((600-actualX)/cos(angle))
    return -1
	
	
def sort(roombaList):
    return sorted(roombaList, key = lambda roomba : angleCost(roomba))

def findTargetOld(roombaList):
    #y = [r.pos.y for r in roombaList]
    #roombaList = [roombaList for (y,roombaList) in sorted(zip(y,roombaList))]
    sortedRoombaList = sort(roombaList)
    print [angleCost(r) for r in sortedRoombaList]
    # there is now a major bug where UAV struggles to evaluate a currently turning roomba
    for r in sortedRoombaList:
	actualX = r.pos.x - 25
	actualY = r.pos.y - 25
	[TL, BL] = [atan2(actualX, actualY) + pi/2, atan2(600-actualY, actualX) + pi]
	[BR, TR] = [atan2(600-actualX, 600-actualY) + 3*pi/2, atan2(actualY, 600-actualX)]
    	angle = (atan2(-r.vel.y, r.vel.x) + 2*pi) % 2*pi
	print 'angle: ', angle*(180/pi)

        if not TR <= angle <= TL:
	    turn_guess = math.floor((((angle + 2*pi) - pi/2) % 2*pi)/(pi/4))
	    new_angle = (((angle - turn_guess*pi/4) + 2*pi) % 2*pi) 
	    if TR <= new_angle <= TL:
		print "ALREADY GOOD CASE" 
		turn = int(turn_guess)
		print 'turns: ', turn
		return [roombaList.index(r)]*(turn)			
	    else:
		if new_angle > TL:
		    print "UNDERSHOT"
		    turn = int(turn_guess + 1)
		    print 'turns: ', turn
		    return [roombaList.index(r)]*(turn)
		if new_angle < TR:
		    print "OVERSHOT"
		    turn = int(turn_guess - 1)
		    print 'turns: ', turn
		    return [roombaList.index(r)]*(turn)

    return [-1]
