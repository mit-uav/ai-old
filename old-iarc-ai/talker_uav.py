#! /usr/bin/python

# Unused in the current setup: for testing purposes only
# publishes random roomba data to roomba_list topic

import rospy
from uav_msgs.msg import RoombaList
from uav_msgs.msg import RoombaLocation
from uav_msgs.msg import SimpleUavCmd
import random

def talker():
    pub = rospy.Publisher("roombas", RoombaList, queue_size=10)
    rospy.init_node("talker", anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
 	timestamp = rospy.get_rostime()
	roomba_loc = RoombaLocation()
	roomba_list = RoombaList()

	roomba_loc.x = random.randint(0, 1024)
	roomba_loc.y = random.randint(0, 768) 

	roomba_list.roombas.append(roomba_loc)
 	roomba_list.timestamp = timestamp

	pub.publish(roomba_list)
	rate.sleep()

if __name__ == '__main__':
    try:
	talker()
    except rospy.ROSInterruptException:
	pass
