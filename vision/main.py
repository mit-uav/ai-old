import numpy as np
import cv2
import cv2.cv as cv

img = cv2.imread('test2.jpg', cv2.CV_LOAD_IMAGE_COLOR)

cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cimg = cv2.medianBlur(cimg,5)

circles = cv2.HoughCircles(cimg,cv.CV_HOUGH_GRADIENT,1,20, param1=50,param2=59, minRadius=5,maxRadius=330)
circles = np.uint16(np.around(circles))
for c in circles[0,:]:
    # draw the outer circle
    cv2.circle(img,(c[0],c[1]),c[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(c[0],c[1]),2,(0,0,255),3)

cv2.imshow('Detected Circles',img)
cv2.waitKey(0)
cv2.destroyAllWindows()