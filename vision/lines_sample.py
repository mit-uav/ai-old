#!/usr/bin/python
import cv2
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import numpy as np
import math


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

def get_segments(fn):
	'''Line segments from image. Returns [x1,y1,x2,y2], indexed from the top left of the image'''
	src = cv2.imread(fn)
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


def main():
	try:
		fn = sys.argv[1]
	except:
		fn = "arena.jpg"
	segs = get_segments(fn)
	for [x1,y1,x2,y2] in segs:
		plt.plot([x1, x2], [-y1, -y2])
	plt.show()

if __name__ == '__main__':
	main()
