import numpy as np
import cv2
import cv2.cv as cv
import sys
import os
from matplotlib import pyplot as plt


def findCircles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #b, gray, r = cv2.split(img)
    ret, gray = cv2.threshold(gray, 205, 200, cv2.THRESH_TOZERO_INV)
    # Wait for a keypress, and quit if it's q
    #if cv2.waitKey(0) & 0xFF == ord('q'):
    #    sys.exit(0)
    #return

    cimg = cv2.medianBlur(gray,5)
    # Want to change param 2
    circles = cv2.HoughCircles(cimg,cv.CV_HOUGH_GRADIENT,1,200, param1=50,param2=40, minRadius=10,maxRadius=75)
    try:
        circles = np.uint16(np.around(circles))
        for c in circles[0,:]:
            # draw the outer circle
            cv2.circle(img,(c[0],c[1]),c[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img,(c[0],c[1]),2,(0,255,0),3)
    except AttributeError:
        print "No circles found!"
    # Display the resulting frame
    #vis = np.concatenate((cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), img1, img2, img3), axis=1)
    cv2.imshow('Image Processing', img)
    # Wait for a keypress, and quit if it's q
    if cv2.waitKey(0) & 0xFF == ord('q'):
        sys.exit(0)

def cannyCircles(img):
   edges = cv2.Canny(img,100,200)

   plt.subplot(121),plt.imshow(img,cmap = 'gray')
   plt.title('Original Image'), plt.xticks([]), plt.yticks([])
   plt.subplot(122),plt.imshow(edges,cmap = 'gray')
   plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
   plt.show()
   cv2.waitKey(0)

"""
for f in os.listdir('images/fake_roomba_scaled'):
    if f.endswith('.png'):
        img = cv2.imread('images/fake_roomba_scaled/' + f, cv2.CV_LOAD_IMAGE_COLOR)
        findCircles(img)
"""

# 0 for webcam
cap = cv2.VideoCapture('data/low.avi')

while(True):
    ret, frame = cap.read()
    findCircles(frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()