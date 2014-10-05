To run the simulation: python board.py
Modules imported: math.py, graphics.py, random.py

board.py  -> Program that simulates the arena board and the roombas
          -> init method takes width and height (in meters) of the board, rCount is the regular roomba count, sCount is the spike roomba count
          -> draw() draws the initial state of the board and roombas; uses graphics.py and Tkinter
          -> collision(pos1, pos2) takes the two positions of roombas and detects collision
          -> run() executes the initial draw and updates roombas as necessary, calling collision() and checking for out-of-bounds roombas
          
roomba.py -> Class that contains information about regular roombas
          -> init method takes pos (initial position), vel (initial velocity), rCircle (a Circle object representing the Roomba)
          -> death() checks to see whether the roomba is out of bounds
          -> step() updates the position and velocity of the roomba

spike.py -> Class that contains information about spike roombas
          -> init method takes pos (initial position), vel (initial velocity), rCircle (a Circle object representing the Roomba), phase (initial phase)
          -> death() checks to see whether the roomba is out of bounds
          -> step() updates the position and velocity of the spike roomba to keep it moving in a circle 

vector.py -> Vector functions 
