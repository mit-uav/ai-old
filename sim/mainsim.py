from quadcopter import Quadcopter
from roomba import Roomba
import random

roomba_list = initRoombas(20)
obstacle_list = initObstacles(4)
quadcopter = Quadcopter()

import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

COLOR_BLACK = pygame.Color(0,0,0)
COLOR_BLUE = pygame.Color(0,0,255)
COLOR_RED = pygame.Color(255,0,0)
COLOR_WHITE = pygame.Color(255,255,255)

COLOR_BG = COLOR_WHITE
COLOR_QUAD = COLOR_BLACK
COLOR_OBS = COLOR_RED
COLOR_SHEEP = COLOR_BLUE

WIN_WIDTH = 640
WIN_HEIGHT = 480
windowSurfaceObj = pygame.display.set_mode((640, 480))
pygame.display.set_caption("IARC UAV Simulator")

# main loop
while True:
    windowSurfaceObj.fill(COLOR_BG)

    #step through all objects
    quadcopter.updatePosition()
    for roomba in roomba_list:
        roomba.updatePosition()
    for obs in obstacle_list:
        obs.updatePosition()

    #render objects as circles and crosses onscreen

    fpsClock.tick(45)

# The following two functions are separate in case of future decisions 
# to distinguish the roombas and obstacles more.
def initRoombas(num = 20):
    return [Roomba(x = random.randrange(WIN_WIDTH),
                   y = random.randrange(WIN_HEIGHT))
                   for i in range(num)]

def initObstacles(num = 4):
    return [Roomba(x = random.randrange(WIN_WIDTH),
                   y = random.randrange(WIN_HEIGHT))
                   for i in range(num)]

def drawRoomba(roomba):
    pass

def drawObstacle(obs):
    pass

def drawQuadcopter(quad):
    pass