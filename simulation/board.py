from math import sin, cos, pi
from random import random
from graphics import *
from roomba import *
from spike import *
from vector import *
import time

class Board:
    # rCount = roomba count, sCount = spike roomba count
    def __init__(self, width, height, rCount, sCount):
        self.width = width      # width of board in meters
        self.height = height    # width of board in meters
        self.rC = []            # roomba list
        self.srC = []           # spike roomba list
        pixelspermeter = 30     # number of pixels per meter
        for x in range(rCount): # initialize roombas
            randnum1 = random()
            pos = Vector(50 + 30 * x, 50 + 30 * x, 0)                   # put roombas in diagonal
            # pos = Vector(50 + randnum1 * 550, 50 + randnum1 * 550, 0)   # random x and y positions within active part of board
            vel = Vector(cos(randnum1*2*pi), sin(randnum1*2*pi), 0)     # random velocities (magnitude 1 m/s)
            rCircle = Circle(Point(pos.x, pos.y), 9/2)                  # creating circle object for roomba
            self.rC.append(Roomba(pos, vel, rCircle))                   # add new Roomba object to list
        for i in range(sCount): # initialize spike roombas at theta = 0, pi/2, pi, and 3pi/2
            pos = Vector(30 * width / 2 + 25 + cos(i*pi/2) * 5 * 30,30 * height / 2 + 25 + sin(i*pi/2) * 5 * 30, 0) 
            vel = Vector(-sin(i*pi/2), cos(i*pi/2), 0)
            rCircle = Circle(Point(pos.x, pos.y), 9/2)                  # creating spike roomba circle object
            self.srC.append(Spike(pos, vel, rCircle, i))                   # add new Spike object to list
        self.rsrC = self.rC + self.srC                                  # new list w/ all types of roombas
            
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
        while len(self.rsrC) > 0:   # while there are still roombas left, keep running
            for r in self.rC:
                if r.d == 1:        # if the roomba is dead, remove it
                    r.circle.undraw()
                    self.rC.remove(r)
            cDetect = []                    # list of roombas pairs
            for x in range(len(self.rC)):   # generates all possible unique pairs of roombas
                d = range(x, len(self.rC))
                e = [d.pop(0)] * len(d)
                cDetect = cDetect + zip(e, d)
            for x in cDetect:
                if self.collision(self.rC[x[0]].pos, self.rC[x[1]].pos): # if there is a collision, reverse directions of both roombas
                    self.rC[x[0]].vel.update_angle(pi)
                    self.rC[x[1]].vel.update_angle(pi)
            for r in self.rsrC:  # draw updated roombas
                r.circle.move(r.vel.x, r.vel.y)
                r.step()
            self.win.update()
        self.stop()                 # quit the simulation

    def stop(self):
        self.win.getMouse()
    
myboard = Board(20, 20, 5, 4)
myboard.run()
