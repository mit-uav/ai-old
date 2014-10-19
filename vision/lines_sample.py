#!/usr/bin/python
'''
This example illustrates how to use Hough Transform to find lines
Usage: ./houghlines.py [<image_name>]
image argument defaults to ../cpp/pic1.png
'''
import cv2
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import numpy as np
import math

try:
	fn = sys.argv[1]
except:
	fn = "arena.jpg"
print __doc__
src = cv2.imread(fn)
red = src[:,:,0]
red[red < 150] = 0
# dst = cv2.Canny(red, 50, 200)
# plt.imshow(dst)
# plt.show()
# cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
# plt.imshow(dst)
# plt.show()
# HoughLines()
# lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
# a,b,c = lines.shape
# for i in range(b):
# rho = lines[0][i][0]
# theta = lines[0][i][1]
# a = math.cos(theta)
# b = math.sin(theta)
# x0, y0 = a*rho, b*rho
# pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
# pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
# cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
lines = cv2.HoughLinesP(red, 1, math.pi/180.0, 100, np.array([]), 50, 20)
print 'Found %d lines', lines.shape[1]

# lines = [[[0,0,100,100]]]
h, w = red.shape
blank = np.zeros((h, w, 3))

lines2 = []
for x1,y1,x2,y2 in lines[0]:
	d = np.cross([x1,y1,1],[x2,y2,1])
	lines2.append(d)

	# angle = math.atan2((y2-y1), (x2-x1))
	# lines2.append(d)
	# dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
	# mag = math.sqrt(np.dot(d,d)) / dist
	# l2.append((mag, angle))
	# plt.plot(mag, angle, 'ro')

	# pt1 = (x1,y1)
	# pt2 = (x2,y2)
	# cv2.line(blank, pt1, pt2, (0,0,1), 1, cv2.CV_AA)

vp = []
for l1 in lines2:
	for l2 in lines2:
		pt = np.cross(l1, l2)
		vp.append(pt)
		x, y, w = pt
		if w > 1:
			plt.plot(x/w, y/w, 'ro')
#
# # plt.hist([a for (d,a) in l2], bins=20)
plt.show()
# plt.xlabel('d')
# plt.ylabel('angle')
# plt.show()
# plt.imshow(blank)
# plt.show()
# a,b,c = lines.shape
# for i in range(b):
# 	cv2.line(blank, (lines[0][i][0], lines[0][i][1]), (lines[0][i][2], lines[0][i][3]), (0, 0, 255), 3, cv2.CV_AA)
# cv2.imshow("source", blank)
# cv2.imshow("detected lines", cdst)
# cv2.waitKey(0)
