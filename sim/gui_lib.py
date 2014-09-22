from Quadcopter import Quadcopter
from Roomba import Roomba
import random

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
COLOR_ROOMBA = COLOR_BLUE

WIN_WIDTH = 640
WIN_HEIGHT = 480
windowSurfaceObj = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("IARC UAV Simulator")

# The following two functions are separate in case of future decisions 
# to distinguish the roombas and obstacles more.
def initRoombas(num = 20):
    return [Roomba(x = random.randrange(WIN_WIDTH),
                   y = random.randrange(WIN_HEIGHT),
                   theta = random.uniform(0,360))
                   for i in range(num)]

def initObstacles(num = 4):
    return [Roomba(x = random.randrange(WIN_WIDTH),
                   y = random.randrange(WIN_HEIGHT),
                   theta = random.uniform(0,360))
                   for i in range(num)]


def drawRoomba(roomba):
    pygame.draw.circle(windowSurfaceObj, COLOR_ROOMBA, (int(roomba.x), int(roomba.y)), 20)

def drawObstacle(roomba):
    pygame.draw.circle(windowSurfaceObj, COLOR_ROOMBA, (int(roomba.x), int(roomba.y)), 20)

def drawQuadcopter(quad):
    length_line = 20
    pygame.draw.line(windowSurfaceObj, COLOR_QUAD, 
                     (quad.x - length_line/2, quad.y - length_line/2),
                     (quad.x + length_line/2, quad.y + length_line/2))
    pygame.draw.line(windowSurfaceObj, COLOR_QUAD, 
                     (quad.x - length_line/2, quad.y + length_line/2),
                     (quad.x + length_line/2, quad.y - length_line/2))