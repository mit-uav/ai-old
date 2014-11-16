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
        self.height = height    # height of board in meters
        self.r = []             # roomba/spike list
        pxpermeter = 30         # number of pixels per meter
        initRadius = 1          # initial starting radius in meters
        
        for x in range(rCount): # initialize roombas in a 1 m radius circle around middle, moving outward 
            pos = Vector(30 * width / 2 + 25 + cos(x*pi/5) * initRadius * pxpermeter, 30 * height / 2 + 25 + sin(x*pi/5) * initRadius * pxpermeter, 0) 
            vel = Vector(0.2*cos(x*pi/5), 0.2*sin(x*pi/5), 0)           # random velocities (magnitude 0.33 m/s)
            rCircle = Circle(Point(pos.x, pos.y), 9.0/2)                  # creating circle object for roomba
            self.r.append(Roomba(pos, vel, rCircle))                    # add new Roomba object to list
        
        pathRadius = 5                                                  # path radius, meters
        for i in range(sCount):                                         # initialize spike roombas at theta = 0, pi/2, pi, and 3pi/2
            pos = Vector(30 * width / 2 + 25 + cos(i*pi/2) * pathRadius * pxpermeter, 30 * height / 2 + 25 + sin(i*pi/2) * pathRadius * pxpermeter, 0) 
            vel = Vector(-0.2*sin(i*pi/2), 0.2*cos(i*pi/2), 0)          # moving at 0.33 m/s
            rCircle = Circle(Point(pos.x, pos.y), 9.0/2)                  # creating spike roomba circle object
            self.r.append(Spike(pos, vel, rCircle, i))                  # add new Spike object to list
            
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
        boundary.setWidth(3)
    
        # grid 
        blockwidth = pixelspermeter
        blockheight = pixelspermeter
        vertarray = [Line(Point(buff/2+i*blockwidth, buff/2), Point(buff/2+i*blockwidth, buff/2+self.pxheight)) for i in range(self.width)]     # vertical lines    
        horizarray = [Line(Point(buff/2, buff/2+j*blockheight), Point(buff/2+self.pxwidth, buff/2+j*blockheight)) for j in range(self.height)]  # horizontal lines
        horizarray[self.height/2].setWidth(3)   # bold the center white line
        linearray = vertarray + horizarray  # all lines
        for line in linearray:              # color each line black
            line.setOutline(color_rgb(255, 255, 255))
    
        # upper green line
        topline = Line(upperleft, upperright)
        topline.setOutline(color_rgb(0, 255, 0))
        topline.setWidth(3)
    
        # lower red line 
        botline = Line(lowerleft, lowerright)
        botline.setOutline(color_rgb(255, 0, 0))
        botline.setWidth(3)

    
        # draw the boundary and all lines
        boundary.draw(self.win)
        for line in linearray:   # draw grid lines
            line.draw(self.win)
        topline.draw(self.win)
        botline.draw(self.win)
        
        # draw all the roombas
        for roomba in self.r:
            if roomba.spike:
                roomba.circle.setFill(color_rgb(0,0,150))
            else:
                roomba.circle.setFill(color_rgb(0,0,0))
            roomba.circle.draw(self.win)

        self.win.setBackground(color_rgb(150, 150, 150))   # grey background
        #self.win.getMouse() # pause for click in self.window

    # Collision check: if distance between roomba centers is less than a threshold, they've collided
    # 1 for collision, 0 for no collision
    def collision(self, pos1, pos2):
        r = 81 # square of the minimum distance between roombas
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        #print "distance squared: ", dx*dx+dy*dy
        if r > dx*dx + dy*dy:
            return 1
        else:
            return 0
        

    # the primary method for running the simulation
    def run(self):
        self.draw()
        while len(self.r) > 0:   # while there are still roombas left, keep running
            for r in self.r:
                if r.spike == 0 and r.d == 1:        # if the roomba is dead, remove it
                    r.circle.undraw()
                    self.r.remove(r)
            cDetect = []                    # list of roombas pairs
            for x in range(len(self.r)):   # generates all possible unique pairs of roombas
                d = range(x, len(self.r))
                e = [d.pop(0)] * len(d)
                cDetect = cDetect + zip(e, d)
            for x in cDetect:
                [roomba1, roomba2] = [self.r[x[0]], self.r[x[1]]]
                if self.collision(roomba1.pos, roomba2.pos):
                    if roomba1.spike and not(roomba2.spike):
                        roomba2.vel.update_angle(pi)
                    elif roomba2.spike and not (roomba1.spike):
                        roomba1.vel.update_angle(pi)
                    else:
                        roomba1.vel.update_angle(pi)
                        roomba2.vel.update_angle(pi)
            for r in self.r:  # draw updated roombas
                r.circle.move(r.vel.x, r.vel.y)
                r.step()
            self.win.update()
        print "All roombas dead. Please click the board to quit sim."
        self.stop()                 # quit the simulation

    def stop(self):
        self.win.getMouse()
    
myboard = Board(20, 20, 10, 4)
myboard.run()
