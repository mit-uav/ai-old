#!/usr/bin/env python

# Bayes dummy node to echo circles_node output

import rospy
from uav_msgs.msg import RoombaLocation, RoombaList, LineSegment, LineList

def callback(data):
    print data

def bayesMain():
    rospy.init_node('bayesDummy', anonymous=True)
    rospy.Subscriber("roombas", RoombaList, callback)
    rospy.Subscriber("lines", LineList, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

# PyRos stuff
if __name__ == '__main__':
    bayesMain()