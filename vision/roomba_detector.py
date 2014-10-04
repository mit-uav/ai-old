import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from scipy.signal import convolve2d, fftconvolve
from scipy.ndimage.filters import gaussian_filter, gaussian_laplace
import os
import cv2

def disk_mask(n, r):
    '''Creates an nxn matrix with a circle of ones with radius r in its center'''
    m = np.ones((n,n))
    y = np.arange(-n/2+1, n/2+1)[np.newaxis].T
    x = np.arange(-n/2+1, n/2+1)
    mask = x*x+y*y <= r*r
    return mask

def circle_mask(n, r):
    mask = np.zeros((n, n))
    return add_circle((int(n/2), int(n/2)), r, mask)

def edges(img):
    '''Shows the edges of the red component of an input file. This seems to filter out glare, which doesn't have sharp edges like robotics vacuums. However, this still misses some roombas. I think we need to take color into consideration too'''
    kernel = [[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]]
    kernel = np.matrix(kernel)
    e1 = convolve2d(img, kernel)
    e2 = convolve2d(img, kernel.T)
    # plt.imshow(e1*e1+e2*e2, interpolation='nearest')
    # plt.show()
    return e1*e1+e2*e2

def runOnImg(func):
    for f in os.listdir('images/fake_roomba'):
        if f.endswith('.jpg'):
            func('images/fake_roomba/'+f)

# def test(filename):
#     img = imread(filename)

def add_circle((i,j), r, img):
    height, width = img.shape
    # don't add pixels multiple times
    pixels = set()
    for theta in np.linspace(0, 2*np.pi, 1000):
        di = int(i + r*np.sin(theta))
        dj = int(j + r*np.cos(theta))

        if 0 <= di < height and 0 <= dj < width:
            if (di, dj) not in pixels:
                img[di, dj] += 1
                pixels.add((di, dj))
    return img

def test(img):
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 10)
    print 'Found %d circles' % len(circles)
    res = img / 1024.
    for (x, y, r) in circles[0]:
        print (x, y, r)
        res = add_circle((y, x), r, res)
        res = add_circle((y, x), r+1, res)
        res = add_circle((y, x), r+2, res)
    plt.imshow(res)
    plt.show()



if __name__ == '__main__':
    # plt.imshow(circle_mask(100, 10))
    # plt.show()
    im = np.mean(imread('quad1.jpg'), axis=2).astype('uint8')
    im = gaussian_filter(im, 1)
    test(im)
    # e = edges(im)
    # e_min = np.min(e)
    # e_max = np.max(e)
    # e = (255 * (e - e_min)/(e_max-e_min)).astype('uint8')
    #
    # _, res = cv2.threshold(e,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # circles = np.zeros(im.shape)
    # for (i, j) in zip(*np.where(res == 255)):
    #     print (i,j)
    #     circles = add_circle((i, j), 10, circles)

    # plt.imshow(res)
    # plt.show()
