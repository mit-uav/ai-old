import datetime
import time
import math

class Roomba:
    global startTime
    startTime = datetime.datetime.now()
    #angleChange must be negative bc Roombas turn CW
    global angleChange
    angleChange = -45

    #Attributes of a Roomba: x and y position, velocity, angle,
    # time since start, how many times it's been touched (a collision=4 touches)
    #Initialize Roomba only with x, y position and angle
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.v = .33
        self.theta = theta
        self.timer = 0
        self.touch = 0

    def getTime(self):
        return (datetime.datetime.now()-startTime).total_seconds()

    #Each touch rotates the angle by 45 degrees CW
    def updateAngle(self, touch):
        self.theta = (self.theta + touch*angleChange)%360
        return self.theta

    #Changes position based on time
    def continuousUpdate(self):
        if self.getTime()%20 == 0:
            self.updateAngle(1)
            self.updatePosition()
            print self.getPosition()

    #Updates x, y position based on angle
    def updatePosition(self):
        self.x = self.x + self.v*math.cos(math.radians(self.theta))*self.getTime()
        self.y = self.y + self.v*math.sin(math.radians(self.theta))*self.getTime()

    def getPosition(self):
        return [self.x, self.y]
