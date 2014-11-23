MIT UAV Python Simulation Readme

To run the simulation: python board.py

External modules imported: math.py, graphics.py, random.py, time.py


Files:

board.py  -> Program that simulates the arena board and the roombas
          -> init method takes width and height (in meters) of the board, rCount is the regular roomba count, sCount is the spike roomba count
          -> draw() draws the initial state of the board and roombas; uses graphics.py and Tkinter
          -> collision(pos1, pos2) takes the two positions of roombas and detects collision
          -> run() executes the initial draw and updates roombas as necessary, calling collision() and checking for out-of-bounds roombas
          
roomba.py -> Class that contains information about regular roombas
          -> death() checks to see whether the roomba is out of bounds
          -> step() updates the position and velocity of the roomba

spike.py  -> Class that contains information about spike roombas
          -> death() checks to see whether the roomba is out of bounds
          -> step() updates the position and velocity of the spike roomba to keep it moving in a circle 

UAV.py    -> Class that codes for the quadcopter
          -> step() updates the position of the quad (target, position)
          -> findTarget() finds a new target for the quad
          -> priority() is the future location of the AI cost function

timeMultiplier.py   -> scales time by a certain amount

vector.py -> Class for 3D vectors to represent position and velocity
