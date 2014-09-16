import numpy as np
import cv2

img = cv2.imread('test.jpg', cv2.CV_LOAD_IMAGE_COLOR)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()