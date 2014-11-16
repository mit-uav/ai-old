import math
from Roomba import Roomba
class CollisionRoomba(Roomba):
    #Theta is in degrees until you update the position
    def updatePosition(self):
        #Convert to radians to use in next calculation
        self.theta = math.radians(self.theta)
        #Convert to degrees to stay consistent when calling self.theta
        self.theta = math.degrees(self.theta + self.v/5.0*self.getTime())
        #New variable theta is in radians
        theta = math.radians(self.theta)
        currentangle = math.atan(self.y/self.x)
        temptheta = currentangle - theta
        self.x = 5.0*math.cos(temptheta)
        self.y = 5*math.sin(temptheta)


