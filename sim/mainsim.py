from quadcopter import Quadcopter
from roomba import Roomba

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

windowSurfaceObj = pygame.display.set_mode((640, 480))
pygame.display.set_caption("IARC UAV Simulator")

# TODO: Store roomba circles and obstacles

# main loop
while True:
	windowSurfaceObj.fill(COLOR_BG)

	# TODO: Render roomba circles and obstacles

	fpsClock.tick(45)