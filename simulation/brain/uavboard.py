from math import sin, cos, pi
from random import random
from graphics import *
from roomba import *
from spike import *
from UAV import *
from vector import *
from timeMultiplier import *
import time

class Board:
    # rCount = roomba count, sCount = spike roomba count
    def __init__(self, width, height, rData, sData):
        self.width = width      # width of board in meters
        self.height = height    # width of board in meters
        self.rC = []            # roomba list
        self.srC = []           # spike roomba list
        pixelspermeter = 30     # number of pixels per meter
        theta = 2*pi/rCount
        boardCenter = (width/2)*pixelspermeter+25
        for x in range(rCount): # initialize roombas
            pos = Vector(boardCenter + 30*sin(theta*x), boardCenter + 30*cos(theta*x), 0)                   # put roombas in diagonal
            vel = Vector(sin(theta*x)/3, cos(theta*x)/3, 0)                # random velocities (magnitude 1 m/s)
            rCircle = Circle(Point(pos.x, pos.y), 9.0/2)                   # creating circle object for roomba
            rLine = Line(Point(pos.x,pos.y), Point(pos.x+vel.x*50, pos.y+vel.y*50)) # velcoity vector line
            self.rC.append(uavRoomba(pos, vel, rCircle, rLine, self.boardTime))       # add new Roomba object to list
        for i in range(sCount): # initialize spike roombas at theta = 0, pi/2, pi, and 3pi/2
            pos = Vector(30 * width / 2 + 25 + cos(i*pi/2) * 5 * 30,30 * height / 2 + 25 + sin(i*pi/2) * 5 * 30, 0) 
            vel = Vector(-sin(i*pi/2)/3, cos(i*pi/2)/3, 0)
            rCircle = Circle(Point(pos.x, pos.y), 9.0/2)                   # creating spike roomba circle object
            self.srC.append(uavSpike(pos, vel, rCircle, i, self.boardTime))   # add new Spike object to list
        self.rCsrC = self.rC + self.srC

        #UAV initialization
        pos = Vector(boardCenter,boardCenter,0)
        vel = Vector(0,0,0)
        rCircle = Circle(Point(pos.x,pos.y), 6.0)
        maxSpeed = 2            # in m/s
        self.uav = UAV(pos, vel, rCircle, maxSpeed, self.boardTime, self.rC, self.srC)       

            
    

    # Collision check: if distance between roomba centers is less than a threshold, they've collided
    # 1 for collision, 0 for no collision
    def collision(self, r, otherPos):
        threshold = 64
        x = r.pos.x + r.vel.x*12
        y = r.pos.y + r.vel.y*12
        dx = x - otherPos.x
        dy = y - otherPos.y
        if threshold > dx*dx + dy*dy:
            return True
        else:
            return False

    # the primary method for running the simulation
    def run(self):
        self.draw()
        lastTime = self.boardTime.getTime()
        while len(self.srC) > 0:   # while there are still roombas left, keep running
            timeInterval = self.boardTime.getTime()-lastTime
            lastTime = self.boardTime.getTime()
            
            for r in self.rC:
                if r.d == 1:        # if the roomba is dead, remove it
                    r.circle.undraw()
                    self.rC.remove(r)
                    self.rCsrC.remove(r)
            if self.uav.d == 1:     # remove dead UAV
                self.uav.circle.undraw()

            cDetect = []                    # list of roombas pairs
            for x in range(len(self.rCsrC)):   # generates all possible unique pairs of roombas
                d = range(x, len(self.rCsrC))
                e = [d.pop(0)] * len(d)
                cDetect = cDetect + zip(e, d)
            for x in cDetect:
                if self.collision(self.rCsrC[x[0]], self.rCsrC[x[1]].pos): # if there is a collision, reverse directions of both roombas
                    if self.rCsrC[x[0]] in self.rC and self.rCsrC[x[0]].turning == False:
                        self.rC[x[0]].flip()
                if self.collision(self.rCsrC[x[1]], self.rCsrC[x[0]].pos):
                    if self.rCsrC[x[1]] in self.rC and self.rCsrC[x[1]].turning == False:
                        self.rC[x[1]].flip()
            for r in self.rCsrC :  # draw updated roombas
                # moves roombas with move function - uses less processing time
                #r.circle.move(timeInterval*r.vel.x*30, timeInterval*r.vel.y*30)
                
                # moves roombas by drawing and undrawing - laggy
                r.circle.undraw()
                r.circle.draw(self.win)
                if r in self.rC:
                    r.velVect.undraw()
                    r.velVect.draw(self.win)

                r.step()
                #Point(r.pos.x,r.pos.y).draw(self.win)   # traces roomba path - laggy
            
            # draw updated UAV
            #self.uav.circle.move(timeInterval*self.uav.vel.x*30, timeInterval*self.uav.vel.y*30)
            
            self.uav.circle.undraw()
            self.uav.circle.draw(self.win)
            #Point(self.uav.pos.x,self.uav.pos.y).draw(self.win)
            
            #self.uav.update(self.rC,self.srC)
            self.uav.step()




            self.win.update()
        self.stop()                 # quit the simulation

    def stop(self):
        self.win.getMouse()

rCount = 10
sCount = 4
for x in range(rCount): # initialize roombas
    pos = Vector(boardCenter + 30*sin(theta*x), boardCenter + 30*cos(theta*x), 0)                   # put roombas in diagonal
    vel = Vector(sin(theta*x)/3, cos(theta*x)/3, 0)                # random velocities (magnitude 1 m/s)
    self.rC.append(uavRoomba(x, pos, vel, self.boardTime))       # add new Roomba object to list
for i in range(sCount): # initialize spike roombas at theta = 0, pi/2, pi, and 3pi/2
    pos = Vector(30 * width / 2 + 25 + cos(i*pi/2) * 5 * 30,30 * height / 2 + 25 + sin(i*pi/2) * 5 * 30, 0) 
    vel = Vector(-sin(i*pi/2)/3, cos(i*pi/2)/3, 0)
    self.srC.append(uavSpike(pos, vel, i, self.boardTime))   # add new Spike object to list

roombaPos
myboard = Board(20, 20, 10, 4)
myboard.run()
