#!/usr/bin/python

# receives data from CV/Modeling team, publishes desired roomba location to simple_uav_cmd topic

import rospy
from uav_msgs.msg import RoombaList
from uav_msgs.msg import RoombaLocation
from uav_msgs.msg import SimpleUavCmd

def callback(data):
    pub = rospy.Publisher("simple_uav_cmd", SimpleUavCmd, queue_size=10) 

    x = 1024
    y = 768
    center = [x/2, y/2]
    list_directions = []

    simple_uav_cmd = SimpleUavCmd()

    for roomba_loc in data.roombas:
	room_x = roomba_loc.x
	room_y = roomba_loc.y
	list_directions.append([room_x-center[0], room_y-center[1]])

    if len(list_directions) > 0:
        simple_uav_cmd.x_dir = list_directions[0][0]
	simple_uav_cmd.y_dir = list_directions[0][1]

    simple_uav_cmd.timestamp = data.timestamp

    rospy.loginfo(simple_uav_cmd)
    rospy.loginfo("all data: %s", data.roombas)

    pub.publish(simple_uav_cmd)
    
def listener():
    rospy.init_node("listener")
    rospy.Subscriber("roombas", RoombaList, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
