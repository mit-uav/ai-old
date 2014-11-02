#!/usr/bin/python
import cv2
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import numpy as np
import math
import rospy
from uav_msgs.msg import LineSegment, LineList


EPSILON = 1e-2
ANGLE_EPSILON = .1

def norm(x):
    return math.sqrt(sum([y*y for y in x]))

def equals(l1,l2):
    return norm(np.cross(l1,l2))<EPSILON

def angle(l):
    if len(l)==3:
        return math.atan2(l[1],l[0])
    return math.atan2(l[3]-l[1],l[2]-l[0])

def parallel(l1,l2):
    return abs(abs(abs((angle(l1)-angle(l2))%(2*math.pi))-math.pi)-math.pi)<ANGLE_EPSILON

def dist(x1,x2):
    return math.sqrt((x2[0]-x1[0])**2+(x2[1]-x1[1])**2)

def get_segments(src):
    '''Line segments from image. Returns [x1,y1,x2,y2], indexed from the top left of the image'''
    red = src[:,:,0]
    red[red < 150] = 0
    lines = cv2.HoughLinesP(red, 1, math.pi/180.0, 50, np.array([]), 50, 20)
    print 'Found %d lines' % lines.shape[1]

    # lines = [[[0,0,100,100]]]
    h, w = red.shape
    blank = np.zeros((h, w, 3))

    lines2 = []
    segs = []
    for x1,y1,x2,y2 in lines[0]:
        d = np.cross([x1,y1,1],[x2,y2,1])
        lines2.append(d)
        segs.append([x1,y1,x2,y2])

    while True:
        br = False
        for i in xrange(len(segs)):
            if br:
                break
            for j in xrange(i+1,len(segs)):
                if br:
                    break
                if parallel(segs[i],segs[j]):
                    a=segs[i][:2]+segs[j][2:]
                    b=segs[j][:2]+segs[i][2:]
                    if parallel(a,b):
                        x0=segs[i][:2]
                        x1=segs[i][2:]
                        x2=segs[j][:2]
                        x3=segs[j][2:]
                        if dist(x1,x2)>dist(x1,x0):
                            x0,x2 = x2,x0
                        if dist(x1,x3)>dist(x1,x0):
                            x0,x3 = x3,x0
                        if dist(x0,x2)>dist(x0,x1):
                            x1,x2 = x2,x1
                        if dist(x0,x3)>dist(x0,x1):
                            x1,x3 = x3,x1
                        #print '%s and %s became %s with angles %f and %f' % (segs[i],segs[j],x0+x1,angle(segs[i])-angle(segs[j]),angle(a)-angle(b))
                        segs[i] = x0 + x1
                        segs.pop(j)
                        br = True
        if br:
            continue
        break
    return segs

# A lot of this is copied from circles_node
def main():
    # 0 for webcam
    cap = cv2.VideoCapture('/home/marcus/Documents/MIT/ExtraCurricular/UAV Team/iarc/iarc/vision/data/PICT0036.AVI')
    # ROS init stuff
    pub = rospy.Publisher('lines', LineList, queue_size = 10)
    rospy.init_node('linesNode', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        segs = get_segments(frame)
        # c[0],c[1] is center, c[2] is radius
        message = LineList(lines = [LineSegment(x1=s[0], y1=s[1], x2=s[2], y2=s[3]) for s in segs], timestamp = rospy.Time.now())
        pub.publish(message)
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
