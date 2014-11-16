from random import random, uniform
from vector import *
from math import pi
import time

class Quadcopter:

    def __init__(self, pos, vel, rCircle):
        self.pos = pos
        self.vel = vel

        self.size = 9     # pixels, where 30 pixels is a meter
        self.square = qSquare

    # update position, velocity, angle as necessary
    
    # for quad, need to update x,y position based on keystrokes
    # z position too? that's gonna be pretty tricky
    # need to print out z position maybe on the right 
    # hmm hard to simulate quad behavior
    
    
    def step(self):
        current = time.time()
        if current-self.randang > 5:   # time elapsed since last random angle change > 5 sec
            noise = uniform(-pi/9, pi/9)   # maximum noise is 20 degrees  
            self.vel.update_angle(noise)
            self.randang = current

        if current-self.tick > 20: # time elapsed since last directional change > 20 sec
            print "about to reverse"
            self.vel.update_angle(pi)
            self.tick = current
        else:
            self.pos.add(self.vel)

