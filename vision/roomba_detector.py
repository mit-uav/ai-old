import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from scipy.signal import convolve2d
import os

def disk_mask(n, r):
    '''Creates an nxn matrix with a circle of ones with radius r in its center'''
    m = np.ones((n,n))
    y = np.arange(-n/2+1, n/2+1)[np.newaxis].T
    x = np.arange(-n/2+1, n/2+1)
    mask = x*x+y*y <= r*r
    return mask

def edges(f):
    '''Shows the edges of the red component of an input file. This seems to filter out glare, which doesn't have sharp edges like robotics vacuums. However, this still misses some roombas. I think we need to take color into consideration too'''
    img = imread('images/fake_roomba/'+f)
    gray = img[:,:,0]
    kernel = [[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]]
    kernel = np.matrix(kernel)
    e1 = convolve2d(gray, kernel)
    e2 = convolve2d(gray, kernel.T)
    # plt.imshow(e1*e1+e2*e2, interpolation='nearest')
    # plt.show()
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(e1*e1+e2*e2)
    plt.show()

def main():
    for f in os.listdir('images/fake_roomba'):
        if f.endswith('.jpg'):
            edges(f)

if __name__ == '__main__':
    # mask = disk_mask(100,10)
    # plt.imshow(mask, interpolation='nearest')
    # plt.show()
    main()
