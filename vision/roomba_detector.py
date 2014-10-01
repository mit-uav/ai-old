import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from scipy.signal import convolve2d
from scipy.ndimage.filters import gaussian_filter, gaussian_laplace
import os

def disk_mask(n, r):
    '''Creates an nxn matrix with a circle of ones with radius r in its center'''
    m = np.ones((n,n))
    y = np.arange(-n/2+1, n/2+1)[np.newaxis].T
    x = np.arange(-n/2+1, n/2+1)
    mask = x*x+y*y <= r*r
    return mask

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

def test(filename):
    img = imread(filename)
    plt.subplot(241)
    plt.imshow(img)
    plt.subplot(242)
    plt.imshow(img[:,:,0])
    plt.subplot(243)
    plt.imshow(img[:,:,1])
    plt.subplot(244)
    plt.imshow(img[:,:,2])

    # plt.subplot(245)
    # plt.imshow(edges(img))
    plt.subplot(246)
    plt.imshow(edges(img[:,:,0]))
    plt.subplot(247)
    plt.imshow(edges(img[:,:,1]))
    plt.subplot(248)
    plt.imshow(edges(img[:,:,2]))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.show()

if __name__ == '__main__':
    # mask = disk_mask(100,10)
    # plt.imshow(mask, interpolation='nearest')
    # plt.show()
    # plt.imshow(edges('quad1.jpg'))
    # plt.show()
    img = imread('quad2.jpg')[:,:,1]
    layer1 = img - gaussian_filter(img, 3)
    plt.imshow(edges(layer1));plt.show()

    # next_img = gaussian_filter(layer1, 1)[::2, ::2]
    # layer2 = next_img - gaussian_filter(next_img, 3)

    # next_img = gaussian_filter(layer2, 1)[::2, ::2]
    # layer3 = next_img - gaussian_filter(next_img, 3)
    #
    # next_img = gaussian_filter(layer3, 1)[::2, ::2]
    # layer4 = next_img - gaussian_filter(next_img, 3)
    #
    # next_img = gaussian_filter(layer4, 1)[::2, ::2]
    # layer5 = next_img - gaussian_filter(next_img, 3)
    #
    # next_img = gaussian_filter(layer5, 1)[::2, ::2]
    # layer6 = next_img - gaussian_filter(next_img, 3)
    #
    # next_img = gaussian_filter(layer6, 1)[::2, ::2]
    # layer7 = next_img - gaussian_filter(next_img, 3)


    # plt.subplot(221)
    # plt.imshow(layer4)
    # plt.subplot(222)
    # plt.imshow(layer5)
    # plt.subplot(223)
    # plt.imshow(layer6)
    # plt.subplot(224)
    # plt.imshow(layer7)
    # plt.show()

    # e = edges(img[:,:,0])
    # plt.imshow(edges(img[:,:,0]))
    # plt.show()
    # test('quad1.jpg')
