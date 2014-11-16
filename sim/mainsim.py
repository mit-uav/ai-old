# you need pygame to run this file
# sudo apt-get install python-pygame

from gui_lib import *

roomba_list = initRoombas(20)
obstacle_list = initObstacles(4)
quadcopter = Quadcopter()

# main loop
while True:
    windowSurfaceObj.fill(COLOR_BG)
    #step through all objects
    quadcopter.updatePosition()
    drawQuadcopter(quadcopter)
    for roomba in roomba_list:
        roomba.updatePosition()
        drawRoomba(roomba)
    for obs in obstacle_list:
        obs.updatePosition()
        drawObstacle(obs)
    
    fpsClock.tick(45)