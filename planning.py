#!/usr/bin/env python

import time

from Simulator import Simulator
from GoalPlanner import GoalPlanner
from PathPlanner import PathPlanner

if __name__ == '__main__':

    # Initialize the components
    simulator = Simulator()
    goalPlanner = GoalPlanner()
    pathPlanner = PathPlanner()

    timestep = 0.1

    try:
        while True:
            now = time.time()

            # Run all of the components
            world = simulator.step()
            goal = goalPlanner.step(world)
            path = pathPlanner.step(goal)

            # Wait for the next timestep
            elapsed = time.time() - now
            if (elapsed < timestep):
                time.sleep(timestep - elapsed)
            else:
                print "Main loop took too long!"

    # Stop on ctrl-C
    except KeyboardInterrupt:
        pass

