#!/usr/bin/env python

# Bayes dummy node to echo circles_node output

import numpy as np
import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

def callback(data):
    print data

def bayesMain():
    rospy.init_node('bayesDummy', anonymous=True)
    rospy.Subscriber("roombas", numpy_msg(Floats), callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

# PyRos stuff
if __name__ == '__main__':
    bayesMain()