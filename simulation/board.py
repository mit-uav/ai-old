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
    def __init__(self, width, height, rCount, sCount):
        self.width = width      # width of board in meters
        self.height = height    # width of board in meters
        self.rC = []            # roomba list
        self.srC = []           # spike roomba list
        self.boardTime = TimeMultiplier(3)
        pixelspermeter = 30     # number of pixels per meter
        theta = 2*pi/rCount
        boardCenter = (width/2)*pixelspermeter+25
        for x in range(rCount): # initialize roombas
            pos = Vector(boardCenter + 30*sin(theta*x), boardCenter + 30*cos(theta*x), 0)                   # put roombas in diagonal
            vel = Vector(sin(theta*x)/3, cos(theta*x)/3, 0)                # random velocities (magnitude 1 m/s)
            rCircle = Circle(Point(pos.x, pos.y), 9.0/2)                   # creating circle object for roomba
            #rLine = Line()
            self.rC.append(Roomba(pos, vel, rCircle,self.boardTime))       # add new Roomba object to list
        for i in range(sCount): # initialize spike roombas at theta = 0, pi/2, pi, and 3pi/2
            pos = Vector(30 * width / 2 + 25 + cos(i*pi/2) * 5 * 30,30 * height / 2 + 25 + sin(i*pi/2) * 5 * 30, 0) 
            vel = Vector(-sin(i*pi/2)/3, cos(i*pi/2)/3, 0)
            rCircle = Circle(Point(pos.x, pos.y), 9.0/2)                   # creating spike roomba circle object
            self.srC.append(Spike(pos, vel, rCircle, i, self.boardTime))   # add new Spike object to list
        self.rCsrC = self.rC + self.srC

        #UAV initialization
        pos = Vector(boardCenter,boardCenter,0)
        vel = Vector(0,0,0)
        rCircle = Circle(Point(pos.x,pos.y), 6.0)
        maxSpeed = 2            # in m/s
        self.uav = UAV(pos, vel, rCircle, maxSpeed, self.boardTime, self.rC, self.srC)       

            
    # Draws the board and roombas                
    def draw(self):  
        pixelspermeter = 30                         # number of pixels per meter
        self.pxwidth = self.width*pixelspermeter    # pixel width of active board - the 30 is completely arbitrary
        self.pxheight = self.height*pixelspermeter  # pixel height of active board 
        buff = 50                                   # buffer around board
        self.win = GraphWin("My Board", self.pxwidth+buff, self.pxheight+buff, False)   # creating a board w/ a 25 pixel buffer on each side
    
        # Four corner points
        upperleft = Point(buff/2, buff/2)
        upperright = Point(buff/2+self.pxwidth, buff/2)
        lowerright = Point(buff/2+self.pxwidth, buff/2 + self.pxheight)
        lowerleft = Point(buff/2, buff/2 + self.pxheight)  
    
        # entire boundary
        boundary = Rectangle(upperleft, lowerright)   # boundary of the grid
        boundary.setOutline(color_rgb(255, 255, 255)) # white boundary
    
        # grid 
        blockwidth = pixelspermeter
        blockheight = pixelspermeter
        vertarray = [Line(Point(buff/2+i*blockwidth, buff/2), Point(buff/2+i*blockwidth, buff/2+self.pxheight)) for i in range(self.width)]     # vertical lines    
        horizarray = [Line(Point(buff/2, buff/2+j*blockheight), Point(buff/2+self.pxwidth, buff/2+j*blockheight)) for j in range(self.height)]  # horizontal lines
        linearray = vertarray + horizarray  # all lines
        for line in linearray:              # color each line black
            line.setOutline(color_rgb(255, 255, 255))
    
        # upper green line
        topline = Line(upperleft, upperright)
        topline.setOutline(color_rgb(0, 255, 0))
    
        # lower red line 
        botline = Line(lowerleft, lowerright)
        botline.setOutline(color_rgb(255, 0, 0))


    
        # draw the boundary and all lines
        boundary.draw(self.win)
        for line in linearray:   # draw grid lines
            line.draw(self.win)
        topline.draw(self.win)
        botline.draw(self.win)
        
        for r in self.rC:   # draw roombas
            r.circle.setFill(color_rgb(0, 0, 0))
            r.circle.draw(self.win)        
        
        for r in self.srC:  # draw spike roombas
            r.circle.setFill(color_rgb(0,0,150))
            r.circle.draw(self.win)

        # draw UAV
        self.uav.circle.setFill(color_rgb(150,0,0))
        self.uav.circle.draw(self.win)

        self.win.setBackground(color_rgb(150, 150, 150))   # grey background
        #self.win.getMouse() # pause for click in self.window

    # Collision check: if distance between roomba centers is less than a threshold, they've collided
    # 1 for collision, 0 for no collision
    def collision(self, pos1, pos2):
        r = 81
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        if r > dx*dx + dy*dy:
            return 1
        else:
            return 0

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
                if self.collision(self.rCsrC[x[0]].pos, self.rCsrC[x[1]].pos): # if there is a collision, reverse directions of both roombas
                    if self.rCsrC[x[0]] in self.rC and self.rCsrC[x[0]].turning == False:
                        self.rC[x[0]].flip()
                    if self.rCsrC[x[1]] in self.rC and self.rCsrC[x[1]].turning == False:
                        self.rC[x[1]].flip()
            for r in self.rCsrC :  # draw updated roombas
                # moves roombas with move function - uses less processing time
                #r.circle.move(timeInterval*r.vel.x*30, timeInterval*r.vel.y*30)
                
                # moves roombas by drawing and undrawing - laggy
                r.circle.undraw()
                r.circle.draw(self.win)

                r.step()
                #Point(r.pos.x,r.pos.y).draw(self.win)   # traces roomba path - laggy
            
            # draw updated UAV
            #self.uav.circle.move(timeInterval*self.uav.vel.x*30, timeInterval*self.uav.vel.y*30)
            
            self.uav.circle.undraw()
            self.uav.circle.draw(self.win)
            #Point(self.uav.pos.x,self.uav.pos.y).draw(self.win)
            
            self.uav.update(self.rC,self.srC)
            self.uav.step()




            self.win.update()
        self.stop()                 # quit the simulation

    def stop(self):
        self.win.getMouse()
    
myboard = Board(20, 20, 10, 4)
myboard.run()
