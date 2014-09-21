import numpy as np
import cv2
import cv2.cv as cv

# 0 for webcam
cap = cv2.VideoCapture('data/low.avi')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cimg = cv2.medianBlur(gray,5)
    circles = cv2.HoughCircles(cimg,cv.CV_HOUGH_GRADIENT,1,200, param1=50,param2=90, minRadius=5,maxRadius=330)
    try:
        circles = np.uint16(np.around(circles))
    except AttributeError:
        continue

    for c in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(c[0],c[1]),c[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(c[0],c[1]),2,(0,0,255),3)
    # Display the resulting frame
    cv2.imshow('Image Processing',cimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
